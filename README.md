# 자동화 pipeline 만들기

root
ㄴapi-key.txt
ㄴprojectList.txt
ㄴgit-clonner.py
ㄴgit-logger.sh/py
ㄴgit-file-tracker.py
ㄴgpt-responser.py
ㄴgit-logs
  ㄴbc-java-log.json
ㄴgit-commits
  ㄴbc-java-commits
  ㄴpgjdbc-commits
ㄴsheets
  ㄴbc-java.xlsx


1 projectList(git path)를 모두 clone 받아 각각 하위폴더로 삼는다.
+ .gitignore에 "{project-name}/" 추가

root
ㄴapi-key.txt
ㄴprojectList.txt
ㄴgit-clonner.py
ㄴbc-java
ㄴh2databse
ㄴpgjdbc

2 각 프로젝트 폴더로 이동하여 git log를 json포맷으로 받는다. 실행은 git-logger로 한다.
+ git log를 받으며 수정된 파일 목록을 함께 저장할 수 있는지 확인
+ json파일을 1) 전체 읽고, 에러가 생기면 2) 한줄씩 읽어서 이어붙이다가, 에러가 생긴 줄은 3) \를 \\으로 바꾼 후 다시 읽어서 이어붙이기 반복
try:	content = readALL()
except: try:	line = readLine()
	except: changeLine("\\", "\\\\")
		line = readLine()
	content += line

root
ㄴapi-key.txt
ㄴprojectList.txt
ㄴgit-clonner.py
ㄴgit-logger.sh/py
ㄴbc-java
  ㄴgit-log.json
ㄴh2databse
ㄴpgjdbc

3 git-log.json을 읽고 '수정된 java파일 목록', 'commit-hash'으로 이루어진 json 파일을 만든다?

4 수정된 java 파일 내용을 before, after, diff 저장한다.
+ 만약 before나 after가 존재하지 않는다면, diff에서 'dev/null'로 인식하고 있는지 체크한다. - 아니라면 다시 시도하고, 그래도 안되면 기록에 남긴다.
- checkout, diff 명령어 사용

root
ㄴapi-key.txt
ㄴprojectList.txt
ㄴgit-clonner.py
ㄴgit-logger.sh/py
ㄴgit-file-tracker.py
ㄴbc-java
  ㄴgit-log.json
  ㄴbc-java-commits
    ㄴbefore_{file-path}.java
    ㄴafter_{file-path}.java
    ㄴdiff_{file-path}.txt 
ㄴh2databse
ㄴpgjdbc

5 원하는 파일 유형(before, after, diff)과 모델명(gpt-3.5/4.0)을 입력하면 해당 파일들을 읽고 prompt와 함께 해당 모델에 질의 후, {original-path}_response.txt에 저장한다.
- 세가지 예외를 발견할 수 있었다 1) billing : quota limit으로 인함이니 메일 드리자. 2) max token/min : 30초  sleep시켜주자 3) max token limit : 단일 파일 토큰 한계이니 무시하거나/fine-tuning으로 이어붙여주자
+ 2번으로 인해 몇몇 파일들이 놓쳐질 수 있다. 따라서 2번 예외 발생시 repeat 변수를 활성화시켜서 다시 질의할 수 있도록 한다.
- 다시 질의시 _response.txt가 존재하는지 체크하고 돌리면 중복 질의를 피할 수 있겠다. 물론 이를 위해선, 예외 발생시 _response.txt 파일을 생성해서는 안된다!

root
ㄴapi-key.txt
ㄴprojectList.txt
ㄴgit-clonner.py
ㄴgit-logger.sh/py
ㄴgit-file-tracker.py
ㄴgpt-responser.py
ㄴbc-java
  ㄴgit-log.json
  ㄴbc-java-commits
    ㄴbefore_{file-path}.java
    ㄴbefore_{file-path}_response.txt 
    ㄴafter_{file-path}.java
    ㄴafter_{file-path}_response.txt 
    ㄴdiff_{file-path}.txt 
    ㄴdiff_{file-path}_response.txt 
ㄴh2databse
ㄴpgjdbc

6 'project', 'commit-hash', 'file-path', 'content', 'response', 'label', 'reason', 'static result'로 이루어진 {project-name}.xlsx 파일을 채운다. 유형은 5번에서 입력한 바를 따른다.
+ 만들어진 xlsx를 구글 시트에 옮긴다?

root
ㄴapi-key.txt
ㄴprojectList.txt
ㄴgit-clonner.py
ㄴgit-logger.sh/py
ㄴgit-file-tracker.py
ㄴgpt-responser.py
ㄴsave2sheet.py
ㄴbc-java
  ㄴgit-log.json
  ㄴbc-java-commits
    ㄴbefore_{file-path}.java
    ㄴbefore_{file-path}_response.txt 
    ㄴafter_{file-path}.java
    ㄴafter_{file-path}_response.txt 
    ㄴdiff_{file-path}.txt 
    ㄴdiff_{file-path}_response.txt
    ㄴbc-java.xlsx
ㄴh2databse
ㄴpgjdbc






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
