import argparse
import os
import json
import pandas as pd

def convert_parquet_to_json(local_dir, save_dir, split='en'):
    output = []
    for file_name in os.listdir(local_dir):
        if (split in file_name or split=='all') and file_name.endswith('.parquet'):
            file_path = os.path.join(local_dir, file_name)
            df = pd.read_parquet(file_path)
            
            for _, row in df.iterrows():
                output.append({"text": row['text']})
    
    output_file = os.path.join(save_dir, f'AnesCorpus_{split}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"JSON file saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Parquet files to JSON format.")
    parser.add_argument('--local-dir', required=True, help="Directory containing Parquet files.")
    parser.add_argument('--save-dir', default='.', help="Path to save converted json files")
    parser.add_argument('--split', default='en', choices=['en', 'cn', 'all'], help="Column name to extract text from (default: 'en').")
    args = parser.parse_args()

    convert_parquet_to_json(args.local_dir, args.save_dir, args.split)