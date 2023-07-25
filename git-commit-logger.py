#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import subprocess
import json
import sys


# In[6]:


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


# In[7]:


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


# In[9]:


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
            
    is_all_java = all(file.endswith('.java') for file in files)
    
    if is_all_java and files != []:
        diff = subprocess.run(['git', 'show', commit['commitHash'], '-p'], capture_output=True, text=True)
        commit['changed_file_list'] = files
        print(files)
        cnt += 1
        print(commit['commitHash'])
        print(cnt, ":", commit['changed_file_list'])
        
        file_path = os.path.join('commits', f'{cnt}_diff.txt')
        write_checkout_file(file_path, diff.stdout)


# In[ ]:


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
        file_path = os.path.join('commits', f'{cnt}_after_{os.path.basename(file)}')
        write_checkout_file(file_path, after_content)
        
        subprocess.run(['git', 'checkout', commit['parent'], '--', file])
        before_content = read_checkout_file(file)
        file_path = os.path.join('commits', f'{cnt}_before_{os.path.basename(file)}')
        write_checkout_file(file_path, before_content)
        
        subprocess.run(['git', 'checkout', 'HEAD', '--', file])


# In[ ]:




