Python 工具备忘
===

Index
---
<!-- TOC -->

- [pip](#pip)
    - [帮助](#帮助)
    - [换源](#换源)
        - [linux](#linux)
- [conda](#conda)
    - [帮助](#帮助-1)
    - [基础命令](#基础命令)
    - [环境管理](#环境管理)
    - [换源](#换源-1)

<!-- /TOC -->

## pip

### 帮助
```shell
# 帮助
pip -h

# 具体命令帮助
pip install -h
pip config -h
```

### 换源
#### linux
```shell
# 创建配置文件
## linux
mkdir ~/.pip
vim ~/.pip/pip.conf
## windows
%HOMEPATH%/pip/pip.ini

# 设置源
[global]
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com

# 常用源
## 阿里源
http://mirrors.aliyun.com/pypi/simple/
## 豆瓣源
http://pypi.douban.com/simple
## 清华源
https://pypi.tuna.tsinghua.edu.cn/simple
```


## conda

### 帮助
```shell
# 帮助概览
conda -h

# 具体命令帮助
conda install -h
```

### 基础命令
```shell
# 切换环境
## window
activate env_name
## linux
source activate env_name

# 浏览包
conda list

# 安装包
conda 
```

### 环境管理
```shell
# 创建环境
conda create -n py36 anaconda python=3.6
conda create -n huay_ore python=3

# 指定目录创建环境
conda create -p ~/spath/py36 anaconda python=3.6

# 克隆/备份环境
conda create --name dst --clone src

# 删除环境
conda remove --name myenv --all
```

### 换源
```shell
# 新增源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes

# 移除源
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

# 常用源
## 清华源
https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
## USTC 源
https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
```
