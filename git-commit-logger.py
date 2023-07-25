#!/usr/bin/env python
# coding: utf-8

# In[8]:

import os
import subprocess
import json
import sys

# 확인할 커밋 개수 : 100개
max_commit = int(sys.argv[1]) 

# Raw 문자열로 처리하기 위해 문자열 앞에 'r'을 붙임
with open('git-log.json', 'r', encoding='utf-8') as f:
    data = f.read()
    raw_data = r'' + data

# Raw 문자열을 JSON으로 디코드
try:
    json_data = json.loads(raw_data) 
    # print(json.dumps(json_data, indent = '\t'))
    
except json.JSONDecodeError as e:
    print(f"JSON 디코드 오류: {e}")


def read_checkout_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"File Open 오류:")
        content = ''
    return content

def write_checkout_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except:
        print(f"File Write 오류")

# 디코드된 JSON 데이터(commitHash)를 활용하여 git show <hash> 결과를 json에 통합(100개)
# https://runebook.dev/ko/docs/git/
cnt = 0

for commit in json_data:        
    files = []
    commit['changed_file_list'] = []
    
    if cnt >= max_commit:
        break
    
    changed_file_list = subprocess.run(['git', 'show', commit['commitHash'], '--name-only', '--pretty=format:%b'], capture_output=True, text=True)
    if changed_file_list.returncode == 0 and changed_file_list.stdout:
        lines = changed_file_list.stdout.split('\n')
        # Process the rest of the code using the 'lines' variable
    else:
        # Handle the case when the Git command didn't execute successfully
        print("Failed to get the changed file list.")
    
    for line in lines:
        if line.strip() in commit['body']:
            continue
        elif line.strip() != '':
            files.append(line.strip())
                  
    java_files = [file for file in files if file.endswith('.java')]
    
    if java_files != [] :
        diff = subprocess.run(['git', 'show', commit['commitHash'], '-p'], capture_output=True, text=True)
        commit['changed_file_list'] = java_files
        print(files)
        cnt += 1
        print(commit['commitHash'])
        print(cnt, ":", commit['changed_file_list'])
        
        file_path = os.path.join('commits', f'{cnt}_diff.txt')
        write_checkout_file(file_path, diff.stdout)

# print(json.dumps(json_data, indent = '\t'))

# 각 commit의 변경된 파일 목록에서 각 파일들의
# before change 또는 after change를 구한다.
# git checkout을 사용해 당시 파일 내용을 불러오고 저장 -> ChatGPT API에 질문한다.
# git checkout HEAD -- <file_path> 를 사용해 돌려놓는 것을 잊지 않는다.

# 다만 이 경우 커밋에서 변경된 파일이 여러개일 경우, 부분적으로밖에 물어보지 못한다. 이를 해결하기 위해서
# 1) 여러 파일의 커밋일 경우 동일한 세션에서 누적해서 물어본다
# 2) commitHash로 branch를 새로 파서 옮긴다. 그 안에서 수정된 부분이 call graph로 연결된 메소드들을 모은다.

subprocess.run(['mkdir', 'commits'])

cnt = 0

for commit in json_data:
    if cnt > max_commit:
        break
    elif commit['changed_file_list'] != []:
        cnt += 1
        print(cnt)
    else:
        continue
        
    for file in commit['changed_file_list']:
        print(file)
        
        subprocess.run(['git', 'checkout', commit['commitHash'], '--', file])
        after_content = read_checkout_file(file) 
        file_path = os.path.join('commits', f'{cnt}_{os.path.basename(file)}_after')
        write_checkout_file(file_path, after_content)
        
        subprocess.run(['git', 'checkout', commit['parent'], '--', file])
        before_content = read_checkout_file(file)
        file_path = os.path.join('commits', f'{cnt}_{os.path.basename(file)}_before')
        write_checkout_file(file_path, before_content)
        
        subprocess.run(['git', 'checkout', 'HEAD', '--', file])