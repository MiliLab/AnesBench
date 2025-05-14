import argparse
from tqdm import tqdm
import json
import os
import regex as re
from thefuzz import process
from openai import OpenAI
import openai
import yaml
import concurrent.futures
import queue
import threading

def env_constructor(loader, node):
    value = loader.construct_scalar(node)
    var_name = value.strip('${} ')
    return os.getenv(var_name, value) 

yaml.SafeLoader.add_constructor('!env', env_constructor)

def extract_choice(gen, choice_list):
    choices = [chr(ord("A") + i) for i in range(len(choice_list))]
    choice_pattern = ''.join(choices)
    choice_or = '|'.join(choices)
    
    patterns = [
        rf"(?:答案|选项|正确(?:答案|选项)?|选择)[:：]+\S*({choice_or})\b",
        rf"(?:(?:[Cc]hoose)|(?:(?:[Aa]nswer|[Cc]hoice)(?![^{choice_pattern}]{{0,20}}?(?:n't|not))[^{choice_pattern}]{{0,10}}?\b(?:|is|:|be))\b)[^{choice_pattern}]{{0,20}}?\b({choice_or})\b",
        rf"(?:答案|选项|正确(?:答案|选项)?|选择)[^不|非]?[是为]+\S{{0,8}}({choice_or})",
        rf"\b({choice_or})\b(?![^{choice_pattern}]*?(?:不|非|不是))[^{choice_pattern}]{{0,8}}(?:正确|准确|符合)",
        rf"\b({choice_or})\b(?![^{choice_pattern}]{{0,8}}?(?:n't|not)[^{choice_pattern}]{{0,5}}?(?:correct|right))[^{choice_pattern}]{{0,10}}?\b(?:correct|right)\b",
        rf"^\s*({choice_or})\s*[\.。，,:：]?$",
        rf"^({choice_or})(?:\.|,|:|$)",
        rf"(?<![a-zA-Z])({choice_or})(?![a-zA-Z=])",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, gen)
        if matches:
            return matches[-1].upper()

    best_match = process.extractOne(gen, choice_list)[0]
    return choices[choice_list.index(best_match)]

def process_before_extraction(gen, choice_dict):
    for key, val in sorted(choice_dict.items(), key=lambda x: len(x[1]), reverse=True):
        pattern = re.compile(re.escape(val.rstrip(".")), re.IGNORECASE)
        gen = pattern.sub(key, gen)
    return gen

def extract_answer(response, row):
    choices = [chr(ord("A") + i) for i in range(row["choice_num"])]
    gen = process_before_extraction(
        response, {choice: row[f"en_{choice}"] for choice in choices}
    )
    pred = extract_choice(gen, [row[f"en_{choice}"] for choice in choices])
    return pred

def format_example(line):
    choice_num = line["choice_num"]
    choices = [chr(ord("A") + i) for i in range(choice_num)]
    choice_content = ', '.join(choices[:-1]) + " and " + choices[-1]
    example = (
        line["en_question"]
        + "\n"
    )
    for choice in choices:
        example += f'{choice}. {line[f"en_{choice}"]}\n'

    messages = [
        {"role": "system", "content": f"You are a medical AI assistant specializing in anesthesiology and general medicine. Your goal is to provide accurate and concise answers to medical multiple-choice questions. Always choose the most suitable answer based on medical knowledge and reasoning."},
        {"role": "user", "content": f"The following is a multiple-choice question related to medicine and anesthesiology. Please analyze the question carefully and select the most suitable one choice from {choice_content} as the final answer. Please think step by step. Carefully analyze each option, explain why it is or isn't correct, and then choose the most suitable answer. Do not generate anything after providing the answer. The question and options are as follows:\n" + example}
    ]
    return messages

def eval_benchmark(
    test_content,
    save_result_dir=None,
    config=None,
    **kwargs
):
    api_key = config['llm']['api_key']
    base_url = config['llm']['base_url']+'/v1'
    max_workers = config['max_workers']
    generation_config = config['llm']['generation']
    
    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    if os.path.exists(f"{save_result_dir}/result.json"):
        with open(f"{save_result_dir}/result.json", "r") as f:
            res_dict = json.load(f)
        result = res_dict["model_output"]
        score = res_dict["correctness"]
        responses = res_dict["model_response"]
        print(f"Load result from {save_result_dir} with length of {len(result)}")
    else:
        result = []
        score = []
        responses = []
    test_content = test_content[len(result):][:10]
    
    task_queue = queue.Queue(maxsize=max_workers)
    results_lock = threading.Lock()
    futures = []
    order = [-1] * len(result)
    def process_row(row, idx):
        question = format_example(row)
        
        while True:
            try:
                completion = client.chat.completions.create(
                    model=config['llm']['model_path'],
                    messages=question,
                    stream=False,
                    temperature=generation_config.get('temperature', 0),
                    max_tokens=generation_config.get('max_new_tokens', 2048),
                )
            except (openai.APITimeoutError, openai.APIError) as e:
                print(f"Retrying due to error: {e}")
                continue
            else:
                break
                
        print(question)
        response = completion.choices[0].message.content
        
        pred = extract_answer(response, row)

        correct = 1 if pred == row["answer"] else 0
        
        with results_lock:
            score.append(correct)
            responses.append(response)
            result.append(pred)
            order.append(idx)
                
        return idx, correct, response, pred
    
    def run_and_release(row, idx):
        try:
            return process_row(row, idx)
        finally:
            task_queue.get()
            task_queue.task_done()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, row in enumerate(test_content):
            task_queue.put(1)
            future = executor.submit(run_and_release, row, idx)
            futures.append(future)
            
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=f"Processing"):
            future.result()
            
        task_queue.join()

    sorted_content = sorted(zip(order, result, responses, score), key=lambda x: x[0])
    result = [x[1] for x in sorted_content]
    responses = [x[2] for x in sorted_content]
    score = [x[3] for x in sorted_content]
    
    save_results(save_result_dir, result, responses, score)
    
    return score

def save_results(save_result_dir, result, responses, score):
    res_dict = {}
    if score:
        res_dict["model_score"] = sum(score) / len(score) 
    res_dict["model_output"] = result
    res_dict["model_response"] = responses
    res_dict["correctness"] = score
    
    os.makedirs(save_result_dir, exist_ok=True)
    with open(os.path.join(save_result_dir, "result.json"), "w") as f:
        json.dump(res_dict, f, indent=4, ensure_ascii=False)

def main(args):
    with open(args.config_path, 'r') as f:
        config = yaml.safe_load(f)

    workspace_eval_dir = f"{config['llm']['path']}/eval_result"
    if not os.path.exists(workspace_eval_dir):
        os.makedirs(workspace_eval_dir)
        
    print(f"Benchmarking on {config['benchmark_path']}")
    
    with open(os.path.join(config['benchmark_path']), "r") as f:
        dev_data = json.load(f)
    
    eval_benchmark(
        dev_data,
        save_result_dir=workspace_eval_dir,
        config=config
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test LLM on AnesBench")
    parser.add_argument(
        "--config_path", 
        type=str, 
        required=True,
        help="Path to the YAML configuration file"
    )
    args = parser.parse_args()
    main(args)