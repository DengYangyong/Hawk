# Hawk
Optimized speculative decoding based on EAGLE

# 0、环境配置
2卡 A40 每块 45G 显存，共 90G 显存。

Pytorch 镜像：Image: pytorch/pytorch:2.2.0-cuda12.1-cudnn8-devel


# 1、拉取数据
Vicuna 需要下载ShareGPT数据，但Vicuna的团队并没有发布原始数据集，而且shareGPT这个网站目前已经不让爬取数据。

有人开源了一版shareGPT数据集（链接在下面），EAGLE的作者应该是基于这个数据集去做的，数据集都是68k左右。以下是下载这个数据集的方法。

### 安装git-lfs
apt-get install git-lfs

### 克隆仓库，但是不立即下载 LFS 对象
git clone https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered

### 进入仓库目录
cd ShareGPT_Vicuna_unfiltered

### 安装 git-lfs 后，拉取指定的 LFS 文件
git lfs pull --include="ShareGPT_V3_unfiltered_cleaned_split.json"

# 2、拉取模型
git lfs clone https://huggingface.co/lmsys/vicuna-7b-v1.3 

git lfs pull

# 3、生成训练数据

直接跑根目录下的：ge_data.sh，生成 1500+的数据。

以下是拉取代码的说明：

python ge_data/ge_data_all_vicuna.py --start 0 --end 1000 --outdir /root/Hawk/data/ShareGPT_Vicuna_unfiltered/

需要自己设置一些命令行参数，先生成少量数据测通。

# 4、训练模型
用 train 目录下的 vicuna_7B_config.json 来初始化 auto-regression head，而不是 vicuna 的 config.json，因为参数量会设置得小一些。

虽然用了 accelerate，但直接跑的时候没有用到多 GPU。

在 main.py 中加了 local_rank 参数，然后启动方式改为torch.distributed.launch来启动。

R-Drop 版本的单节点多 GPU训练：

nohup python -m torch.distributed.launch --nproc_per_node=2 train/main_rdrop.py --tmpdir /root/Hawk/data/ShareGPT_Vicuna_unfiltered/1/ --outdir checkpoints/ --cpdir checkpoints/ --basepath /root/model/vicuna-7b-v1.3 --configpath train/vicuna_7B_config.json --bs 3 > vicuna_rdrop.log 2>&1 &

EAGLE原始版本的单节点多 GPU 训练：

nohup python -m torch.distributed.launch --nproc_per_node=2 train/main.py --tmpdir /root/Hawk/data/ShareGPT_Vicuna_unfiltered/1/ --outdir checkpoints/ --cpdir checkpoints/ --basepath /root/model/vicuna-7b-v1.3 --configpath train/vicuna_7B_config.json --bs 3 > vicuna.log 2>&1 &
