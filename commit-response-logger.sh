#!/bin/bash

read -p "Enter the repository name: " name

# 폴더가 존재하는지 확인
if [ ! -d "$name" ]; then
    echo "폴더가 존재하지 않습니다."  
    exit 1
fi
cd "$name"

bash git-log.sh

python git-commit-logger.py 100

folder_name="${name%-commits}"
if [ ! -d "$folder_name" ]; then
    echo "No commits folder"
    mkdir "$folder_name"
fi
cd "$folder_name"

# 파일이 존재하는지 확인
if [ ! -f "../../gpt-response-logger.py" ]; then
    echo "gpt.py not found"
else
    cp "../../gpt-response-logger.py" .
    echo "gpt.py copied"
fi

python gpt-response-logger.py
