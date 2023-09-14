#!/usr/bin/env python
# coding: utf-8

# In[60]:


import os
import json
import subprocess

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

def checkout_file_before_commit(parent_hash, file, sanitized_path, directory, cnt):
    subprocess.run(['git', 'checkout', parent_hash, '--', file])
    before_content = read_file(file)
    file_path = os.path.join('..', 'commit-files', f'{directory}', f'{cnt}_before_{sanitized_path}')
    write_file(file_path, before_content)
    subprocess.run(['git', 'checkout', 'HEAD', '--', file])
    
def checkout_file_after_commit(commit_hash, file, sanitized_path, directory, cnt):
    subprocess.run(['git', 'checkout', commit_hash, '--', file])
    after_content = read_file(file)
    file_path = os.path.join('..', 'commit-files', f'{directory}', f'{cnt}_after_{sanitized_path}')
    write_file(file_path, after_content)   
    subprocess.run(['git', 'checkout', 'HEAD', '--', file])
    
def diff_file_of_commit(commit_hash, file, sanitized_path, directory, cnt):
    hash_path = commit_hash+":"+file
    # numOfLine = subprocess.run(['git', 'show', hash_path, "|", "wc", "-l"], shell=True, stdout=subprocess.PIPE, text=True).stdout.rstrip()
    numOfLine = 9999
    line_option = "-U"+str(numOfLine)
    file_path = os.path.join('..', 'commit-files', f'{directory}', f'{cnt}_diff_{sanitized_path}')
    file_option = "--output="+file_path
    parent_hash = commit_hash+"~1"
    subprocess.run(['git', 'diff', line_option, file_option, parent_hash, commit_hash, "--", file])
    # print("git diff", line_option, file_option, parent_hash, commit_hash, "--", file)
    
    
def file_tracker(directories, output_directory):
    
    # 만약 output_directory 디렉토리가 없다면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    root = os.getcwd()
    
    for directory in directories:
        
        os.chdir(output_directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.chdir("..")
        
        commits = []
        log_file = os.path.join(os.getcwd(), "commit-logs", f"{directory}-files-log.json")
         
        # 리포지토리 디렉토리로 이동
        os.chdir(directory) 
        
        with open(log_file, "r", encoding='utf-8') as f:
            data = f.read()
            raw_data = r''+data
            try:
                commits = json.loads(raw_data)
#                 print(commits)
            except json.JSONDecodeError as e:
                print(f"JSON 디코드 오류: {e}")

        cnt=0
        for commit in commits:
            if commit['changed_file_list'] != []:
                cnt += 1
                # print(cnt)
            else:
                continue

            for file in commit['changed_file_list']:
                # print(file)
                sanitized_path = file.replace("/", "_")
            
                # 하려는 작업 선택
                # checkout_file_before_commit(commit['parent'], file, sanitized_path, directory, cnt)
                # checkout_file_after_commit(commit['commitHash'], file, sanitized_path, directory, cnt)
                diff_file_of_commit(commit['commitHash'], file, sanitized_path, directory, cnt)
        print(directory, "files 생성 완료")
        os.chdir("..")
    print("모든 file 생성 완료")


# In[64]:


if __name__ == "__main__":
    directories = ["h2database", "bc-java", "pgjdbc", "junit4", "gson", "guava"]
    output_directory = "commit-files"
    # commit_logger(directories)
    file_tracker(directories, output_directory)


# In[65]:


os.getcwd()


# In[62]:


os.chdir("..")


# In[ ]:




