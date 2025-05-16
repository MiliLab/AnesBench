
<p align="center">

  <h2 align="center"><strong>AnesBench: Multi-Dimensional Evaluation of LLM Reasoning in Anesthesiology</strong></h2>

<div align="center">
<h5>
<em>Xiang Feng<sup>1 *</sup>, Wentao Jiang<sup>1 *</sup>, Zengmao Wang<sup>1</sup>, Yong Luo<sup>1 †</sup>, Pingbo Xu<sup>2,3</sup>, Baosheng Yu<sup>4</sup>,<br/> Hua Jin<sup>5,6</sup>, Bo Du<sup>1 †</sup>, Jing Zhang<sup>1 †</sup> </em>
    <br><br>
       	<sup>1</sup> School of Computer Science, Wuhan University, China,<br/>
        <sup>2</sup> Department of Anesthesiology, Zhejiang Cancer Hospital, China,<br/> 
        <sup>3</sup> Institute of Medicine, Chinese Academy of Sciences, Hangzhou, Zhejiang, China<br/> 
        <sup>4</sup> Lee Kong Chian School of Medicine, Nanyang Technological University, Singapore<br/> 
        <sup>5</sup> Department of Anesthesiology, First People’s Hospital of Yunnan Province, China<br/> 
        <sup>6</sup> Kunming University of Science and Technology, China<br/> 
</h5>
<h5>
<sup>∗</sup> Equal contribution, <sup>†</sup> Corresponding author
</h5>
</div>



<h5 align="center">
<a href="https://mililab.github.io/anesbench.ai/"> <img src="https://img.shields.io/badge/Project-AnesBench-4183C4.svg?logo=Github"></a> <a href="https://arxiv.org/abs/2504.02404"> <img src="https://img.shields.io/badge/Arxiv-2504.02404-b31b1b.svg?logo=arXiv"></a> <a href="https://huggingface.co/datasets/MiliLab/AnesBench"><img src="https://img.shields.io/badge/🤗%20HuggingFace-AnesBench-FFD43B.svg?logo=huggingface"></a>
</h5>

<figure>
<div align="center">
<img src=figs/logo.png width="20%">
</div>
</figure>

# 🐨  Contents

- [🔥 Update](#-update)
- [🌞 Intro](#-intro)
- [🔍 Overview](#-overview)
- [📖 Datasets](#-datasets)
  - [AnesBench](#anesbench)
    - [AnesBench JSON Example](#json-sample)
    - [Field Explanations](#field-explanations)
    - [AnesBench Recommended Usage](#recommended-usage)
  - [AnesCorpus & AnesQA](#anescorpus--anesqa)
- [🐎 Leaderboard](#-leaderboard)
- [🔨 Evaluation](#-evaluation)
- [🛠️ Training with LLaMA-Factory](#️-training-with-llama-factory)
- [⭐ Citation](#-citation)



# 🔥 Update
**2025.05.14**
- We released the evaluation code along with usage instructions!!!

**2025.05.13**
- We released AnesBench on HuggingFace!!!

**2025.04.04**
- We uploaded our work on [arXiv](https://arxiv.org/abs/2504.02404)!!!

**2025.03.31**
- We released the [AnesBench project page](https://mililab.github.io/anesbench.ai/) !!!.


# 🌞 Intro
This project aims to enhance the reasoning capabilities of large language models in the field of anesthesiology. We focus on two key questions: (1) What model characteristics are associated with stronger anesthetic reasoning abilities? (2) How do training methodologies and test-time scaling influence LLM performance in anesthesiology-specific reasoning tasks?

During the course of the project, we developed three datasets: **AnesBench**, a bilingual benchmark for anesthetic reasoning; **AnesQA**, a supervised fine-tuning dataset; and **AnesCorpus**, a continual pretraining corpus.

This Github repository provides an overview of the datasets, usage examples, and a leaderboard featuring performance results of over 50 state-of-the-art LLMs.

> For dataset access, please refer to our Hugging Face repository: [AnesBench](https://huggingface.co/datasets/MiliLab/AnesBench), [AnesQA](https://huggingface.co/datasets/MiliLab/AnesQA) and [AnesCorpus](https://huggingface.co/datasets/MiliLab/AnesCorpus).

> For key insights and conclusions, please refer to the [AnesBench project page](https://mililab.github.io/anesbench.ai/).

# 🔍 Overview
<figure>
<div align="center">
<img src="figs/overview.png">
</div>
<div align="center">
<figcaption align = "center"><b>Figure 1: Overview of the AnesBench. 
 </b></figcaption>
</div>
</figure>

# 📖 Datasets

## AnesBench

<a href="https://huggingface.co/datasets/MiliLab/AnesBench"> <img src="https://img.shields.io/badge/🤗%20HuggingFace-AnesBench-FFD43B.svg?logo=huggingface"></a>

**AnesBench** is designed to assess anesthesiology-related reasoning capabilities of Large Language Models (LLMs). 
It contains 4,427 anesthesiology questions in English. 
Each question is labeled with a three-level categorization of cognitive demands and includes Chinese-English translations, 
enabling evaluation of LLMs’ knowledge, application, and clinical reasoning abilities across diverse linguistic contexts.

### JSON Sample

```json
    {
        "id": "1bb76e22-6dbf-5b17-bbdf-0e6cde9f9440",
        "choice_num": 4,
        "answer": "A",
        "level": 1,
        "en_question": "english question",
        "en_X": "option X",
        "zh_question": "中文问题",
        "zh_X": "选项X",
    }
```

### Field Explanations

| Field         | Type   | Description                                                                 |
|------------------|----------|-----------------------------------------------------------------------------|
| `id`             | string   | A randomly generated ID using UUID                                          |
| `choice_num`     | int      | The number of options in this question                                      |
| `answer`         | string   | The correct answer to this question                                         |
| `level`          | int      | The cognitive demand level of the question (`1`, `2`, and `3` represent `system1`, `system1.x`, and `system2` respectively) |
| `en_question`    | string   | English description of the question stem                                   |
| `cn_question`    | string   | Chinese description of the question stem                                   |
| `en_X`           | string   | English description of the option (X takes values from A until the total number of options is reached)                                         |
| `cn_X`           | string   | Chinese description of the option (X takes values from A until the total number of options is reached)                                         |


### Recommended Usage

- **Question Answering**: QA in a zero-shot or few-shot setting, where the question is fed into a LLM or other QA system. Accuracy could be used as the evaluation metric.

## AnesCorpus & AnesQA
<a href="https://huggingface.co/datasets/MiliLab/AnesCorpus"> <img src="https://img.shields.io/badge/🤗%20HuggingFace-AnesCorpus-FFD43B.svg?logo=huggingface"></a> <a href="https://huggingface.co/datasets/MiliLab/AnesQA"> <img src="https://img.shields.io/badge/🤗%20HuggingFace-AnesQA-FFD43B.svg?logo=huggingface"></a>

We also provides two domain-specific datasets—**AnesCorpus** and **AnesQA**—designed to support research and development of language models in the field of anesthesiology. These resources are tailored for use in Continuous Pre-training (CPT) and Supervised Fine-Tuning (SFT) of LLMs.

### AnesCorpus

**AnesCorpus** is a large-scale, domain-specific corpus constructed for **Continuous Pre-training (CPT)** in the field of anesthesiology. It is built from two primary sources:

- **Domain-specific filtering** from large-scale corpora such as [FineWeb](https://huggingface.co/datasets/HuggingFaceFW/fineweb), using keyword-based heuristics.
- **PubMed research articles** related to anesthesiology, processed through rigorous cleaning and formatting to ensure high relevance and quality.

| Language | Rows    | Tokens   |
|----------|---------|----------|
| English  | ~1.59M  | ~3B      |
| Chinese  | ~593K   | ~0.2B    |

This curated dataset provides a rich foundation for pretraining language models to understand anesthesiology-related concepts, terminology, and clinical context.


### AnesQA

**AnesQA** is a bilingual **question-answering (QA)** dataset designed for **Supervised Fine-Tuning (SFT)**. The QA pairs are generated and filtered using advanced large language models, then translated to Chinese to support multilingual fine-tuning.

| Language | QA Pairs |
|----------|----------|
| English  | ~20.7K   |
| Chinese  | ~20.6K   |

AnesQA enables the development of instruction-tuned models with robust reasoning and answering capabilities in the anesthesiology domain.

### Recommended Usage

These datasets are compatible with a wide range of instruction-tuned language models and popular training frameworks.

We provide an example below demonstrating how to fine-tune a model using AnesCorpus and AnesQA with [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory). For implementation details, refer to the [**Example Usage**](#️-training-with-llama-factory).

#  🐎 Leaderboard

We maintain a live leaderboard to track model performance on AnesBench, covering both System 1 and System 2 tasks in the anesthesiology domain.

📊 Check out the leaderboard here:
👉 https://mililab.github.io/anesbench.ai/leaderboard/

# 🔨 Evaluation

---

## 📁 0. Clone the Repository & Download Benchmark

Clone Repository:

```bash
git clone https://github.com/MiliLab/AnesBench
cd AnesBench
```

Download Benchmark:
```bash
cd benchmark
huggingface-cli download --repo-type dataset  MiliLab/AnesBench --local-dir ./
```
---

## 🧱 1. Prepare the Runtime Environment

Before starting, ensure that `CUDA` and its compiler `nvcc` are properly installed and accessible.

### Check:
```bash
nvcc --version
```

We recommend separating the SGLang service environment from the inference environment.

### SGLang service environment

```bash
conda create -n sglang_server python==3.10
conda activate sglang_server
```

Then, install the required `sglang` and `flashinfer` packages.

```bash
pip install "sglang[all]"
pip install sglang-router 
```
Download the wheel file for your environment from [https://github.com/flashinfer-ai/flashinfer/releases](https://github.com/flashinfer-ai/flashinfer/releases).

```bash
pip install /path/to/flashinfer-wheel
```

### Inference environment

Create a new environment and install the packages based on the requirements file.

```bash
conda create -n inference python==3.10
conda activate inference
cd eval
pip install -r requirements.txt
```
---

### Environment Variables

Prepare environment variables in the `.env` file.

```bash
export RESULT_SAVE_PATH=/path/to/result_save_dir
export MODEL_PATH=/path/to/model
export BENCHMARK_PATH=/path/to/benchmark
```

and run:

```bash
source .env
```

## ▶️ 2. Run Evaluation

### For SGLang service
```bash
bash sglang_server.sh 
```

### For Inference
```bash
python ./evaluate.py --config ./config.yaml 
```

---

# 🛠️ Training with LLaMA-Factory

To train with **AnesCorpus** (for CPT) and **AnesQA** (for SFT) using [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory), follow the steps below:


## 1️. Install LLaMA-Factory

Follow the [LLaMA-Factory official installation guide](https://llamafactory.readthedocs.io/en/latest/getting_started/installation.html), or use the following scripts:

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

## 2. Convert Data to LLaMA-Factory Format

We provide scripts to convert the raw Parquet files into the required JSON format.

> 📌 The `--split` argument can be set to:
> - `en`: English data only  
> - `cn`: Chinese data only  
> - `all`: merge both English and Chinese

#### For AnesCorpus (CPT):
```bash
python tools/anescorpus2json.py \
    --local-dir /path/to/anescorpus/parquet_files \
    --save-dir ./data \
    --split en
```
This will generate:  
`
./data/AnesCorpus_en.json
`


#### For AnesQA (SFT):
```bash
python tools/anescorpus2json.py \
    --local-dir /path/to/anesqa/parquet_files \
    --save-dir ./data \
    --split en \
    --instruction "Please answer the following question based on the anesthesiology context."
```

This will generate:  
`
./data/AnesCorpus_en.json
`

## 3. Register the Dataset
Move your dataset in `LLaMA-Factory/data`, and register your dataset entries in `LLaMA-Factory/data/dataset_info.json/`. 


```json
{
  "anescorpus_en": {
    "file_name": "AnesCorpus_en.json",
    "columns": {
      "prompt": "text"
    }
  },
  "anesqa_en": {
    "file_name": "AnesQA_en.json",
  }
}
```

For more details on dataset registration and formatting, refer to the official data preparation guide in [manual](https://llamafactory.readthedocs.io/en/latest/getting_started/data_preparation.html) and [github](https://github.com/hiyouga/LLaMA-Factory/blob/main/data/README.md).

## 4. Set Config File
You can use or modify the example config files we provide in `configs/`.

Edit them to set paths like:

```yaml
// Example snippet
dataset_dir: LLaMA-Factory/data    // Directory contains "dataset_info.json"
dataset: anesqa_en
model_name_or_path: meta-llama/Llama-3.1-8B-Instruct
output_dir: ./output/llama3.1-anesqa-sft
...
```
More details can be found in [official guide](https://llamafactory.readthedocs.io/en/latest/advanced/arguments.html).

## 5. Launch Training from CLI
### Continuous Pre-training (CPT)
```bash
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
llamafactory-cli train configs/qwen2.5-7b-pt-anesthesia.yaml
```

### Supervised Fine-Tuning (SFT)
```bash
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
llamafactory-cli train configs/qwen2.5-7b-sft-anesthesia.yaml
```


# ⭐ Citation

If you find AnesBench helpful, please consider giving this repo a ⭐ and citing:

```latex
@article{AnesBench,
  title={AnesBench: Multi-Dimensional Evaluation of LLM Reasoning in Anesthesiology},
  author={Xiang Feng and Wentao Jiang and Zengmao Wang and Yong Luo and Pingbo Xu and Baosheng Yu and Hua Jin and Bo Du and Jing Zhang},
  journal={arXiv preprint arXiv:2504.02404},
  year={2025}
}
```
