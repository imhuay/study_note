#!/usr/bin/env bash

# git subtree add --prefix=code/keras_demo/keras_model/bert_by_keras bert_by_keras master --squash
# git subtree add --prefix=code/keras_demo keras_demo master --squash

# 使用 submodule 代替 subtree
# git subtree push --prefix=code/keras_demo/keras_model/bert_by_keras bert_by_keras master
# git subtree push --prefix=code/keras_demo keras_demo master

# 获取仓库父目录
pwd=$(pwd)

# 先更新子仓库
printf "=== First: Update submodule ===\n"

# 1.
sub_repo="bert_by_keras"
echo "____ Start update $sub_repo"
cd "$pwd/code/my_models/$sub_repo" || exit
ret=$(git pull origin master)
if [[ $ret =~ "Already up to date" ]]; then
  echo "$sub_repo is already up to date."
else
  cd "$pwd" || exit
  git add "$pwd/code/my_models/$sub_repo"
  git commit -m "U $sub_repo"
fi

# 更新父仓库
cd "$pwd" || exit
printf "\n=== Final: Push father repository ===\n"
git push
