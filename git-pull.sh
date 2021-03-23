#!/usr/bin/env bash

git pull
git subtree pull --prefix=code/keras_demo keras_demo master --squash
git subtree pull --prefix=code/keras_demo/keras_model/bert_by_keras bert_by_keras master --squash
