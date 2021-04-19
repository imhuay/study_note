#!/usr/bin/env bash

# git subtree add --prefix=code/keras_demo/keras_model/bert_by_keras bert_by_keras master --squash
# git subtree add --prefix=code/keras_demo keras_demo master --squash

# 使用 submodule 代替 subtree
# git subtree push --prefix=code/keras_demo/keras_model/bert_by_keras bert_by_keras master
# git subtree push --prefix=code/keras_demo keras_demo master

# 获取仓库父目录
pwd=$(pwd)

# 先更新子仓库
printf "=== Update submodule first ===\n"
printf "___ Start update bert_by_keras\n"
cd "$pwd/code/my_models/bert_by_keras" || exit
git pull origin master

printf "\n=== Submodule status list ===\n"
git submodule status
echo

# 更新父仓库
cd "$pwd" || exit
printf "\n=== Start father repository ===\n"
git push



