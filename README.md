
<p align="center">

  <h2 align="center"><strong>AnesBench: Multi-Dimensional Evaluation of LLM Reasoning in Anesthesiology</strong></h2>

<div align="center">
<h5>
<em>Xiang Feng<sup>1 *</sup>, Wentao Jiang<sup>1 *</sup>, Zengmao Wang<sup>1</sup>, Yong Luo<sup>1 †</sup>, Pingbo Xu<sup>2,3</sup>, Baosheng Yu<sup>4</sup>,<br/> Hua Jin<sup>5,6</sup>, Bo Du<sup>1 †</sup>, Jing Zhang<sup>3 †</sup> </em>
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
<a href="https://mililab.github.io/anesbench.ai/"> <img src="https://img.shields.io/badge/Project-AnesBench-4183C4.svg?logo=Github"></a> <a href="https://arxiv.org/abs/2504.02404"> <img src="https://img.shields.io/badge/Arxiv-2504.02404-b31b1b.svg?logo=arXiv"></a> <img src="https://img.shields.io/badge/🤗-Coming Soon-FF8C00.svg">
</h5>

<figure>
<div align="center">
<img src=figs/logo.png width="20%">
</div>
</figure>


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
**AnesBench** is designed to assess anesthesiology-related reasoning capabilities of Large Language Models (LLMs). 
It contains 4,427 anesthesiology questions in English. 
Each question is labeled with a three-level categorization of cognitive demands and includes Chinese-English translations, 
enabling evaluation of LLMs’ knowledge, application, and clinical reasoning abilities across diverse linguistic contexts.

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

<a href="https://huggingface.co/datasets/MiliLab/AnesBench"> <img src="https://img.shields.io/badge/🤗%20HuggingFace-Dataset-FFD43B.svg?logo=huggingface"></a>

## AnesCorpus

## AnesQA


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

## Run Evaluation

### For SGLang service
```bash
bash sglang_server.sh 
```

### For Inference
```bash
python ./evaluate.py --config ./config.yaml 
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
