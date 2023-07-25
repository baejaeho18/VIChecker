# commit-logger

<br>
<br>
#!/bin/bash
<br>

read -p "Enter the repository name: " name
<br>
if [ ! -d "$name" ]; then
<br>
    echo "폴더가 존재하지 않습니다."  
<br>
    exit 1
<br>
fi
<br>
cd "$name"
<br>

bash git-log.sh
<br>

python git-commit-logger.py 100
<br>

folder_name="${name%-commits}"
<br>
# 폴더가 존재하는지 확인
<br>
if [ ! -d "$folder_name" ]; then
<br>
    echo "No commits folder"
<br>
    mkdir "$folder_name"
<br>
fi
<br>
cd "$folder_name"
<br>

# 파일이 존재하는지 확인
<br>
if [ ! -f "../../gpt-response-logger.py" ]; then
<br>
    echo "gpt.py not found"
<br>
else
<br>
    cp "../../gpt-response-logger.py" .
<br>
    echo "gpt.py copied"
<br>
fi
<br>

python gpt-response-logger.py

<br>
