import os
import subprocess
import json
import sys
import pandas as pd

max_commit = 100 # int(sys.argv[1]) 

# Raw 문자열로 처리하기 위해 문자열 앞에 'r'을 붙임
with open('git-log.json', 'r', encoding='utf-8') as f:
    data = f.read()
    raw_data = r'' + data

# Raw 문자열을 JSON으로 디코드
try:
    json_data = json.loads(raw_data) 
    print(json.dumps(json_data, indent = '\t'))
    
except json.JSONDecodeError as e:
    print(f"JSON 디코드 오류: {e}")

subprocess.run(['mkdir', 'commits'])

def read_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"File Open 오류:")
        content = ''
    return content

def write_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except:
        print(f"File Write 오류")

cnt = 0

for commit in json_data:        
    files = []
    commit['changed_file_list'] = []
    
    
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
    java_files = list(filter(lambda file: 'src/test' not in file, java_files))
    
    if java_files != [] :
        diff = subprocess.run(['git', 'show', commit['commitHash'], '-p'], capture_output=True, text=True)
        commit['changed_file_list'] = java_files
        print(files)
        cnt += 1
        print(commit['commitHash'])
        print(cnt, ":", commit['changed_file_list'])

df = pd.DataFrame()

cnt = 0
for commit in json_data:
    if commit['changed_file_list'] != []:
        cnt += 1
        print(cnt)
    else:
        continue
    
    print(commit['commitHash'])
    
    for file in commit['changed_file_list']:
        print(file)
        
        sanitized_path = file.replace("/", "_")
        file_path = os.path.join('commits', f'{cnt}_diff_{sanitized_path}')
        diff_content = read_file(file_path)

        file_path = file_path.replace('.java', '_response.txt')
        response_content = read_file(file_path)

        row_data = {
                        "Repository":"h2database",
                        "Hash Code":commit['commitHash'],
                        "file name":file,
                        "Diff Content":diff_content,
                        "4,0 Response":response_content
                    }
        df = df._append(row_data, ignore_index=True)
    
    
df.to_excel("../h2database.xlsx", index=False)

print("데이터가 엑셀 파일에 저장되었습니다.")
