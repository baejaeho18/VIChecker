#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import json
import pandas as pd

def read_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"File Open 오류:", str(e))
        content = ''
    return content

def commits_to_sheet(directory, output_directory, option):
    output_file = os.path.join("..", "..", output_directory, f"{directory}_{option}.xlsx")
    
    try:
        df = pd.read_excel(output_file)
    except FileNotFoundError:
        df = pd.DataFrame()

    cnt = 0
    commits = []
    log_file = os.path.join("..", "..", "commit-logs", f"{directory}-files-log.json")
    with open(log_file, "r", encoding='utf-8') as f:
        data = f.read()
        raw_data = r''+data
        try:
            commits = json.loads(raw_data)
        except json.JSONDecodeError as e:
            print(f"JSON 디코드 오류: {e}")
    
    for commit in commits:
        if commit['changed_file_list'] != []:
            cnt += 1
            print(cnt)
        else:
            continue

        for file in commit['changed_file_list']:
            print(file)
        
            sanitized_path = file.replace("/", "_")
            file_path = f'{cnt}_{option}_{sanitized_path}'
            file_content = read_file(file_path)

            response_file_path = file_path.replace('.java', '_response.txt')
            response_content = read_file(response_file_path)

            row_data = {
                        "Repository":directory,
                        "Hash Code":commit['commitHash'],
                        "File Name":file,
        #                "Content":file_content,
                        "Response":response_content
                        }
            df = df.append(row_data, ignore_index=True)

    df.to_excel(output_file, index=False)

    print(directory, "데이터가 엑셀 파일에 저장되었습니다.")
    


# In[10]:


if __name__ == "__main__":
    directories = ["bc-java"] # ["pgjdbc", "junit4", "gson", "guava", "h2database", "bc-java"]
    working_directory = "commit-files"
    output_directory = "commit-sheets"
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # 3_에서 이미 만들어졌으리라 가정.
    os.chdir(working_directory)
    
    for directory in directories:
        os.chdir(directory)
        commits_to_sheet(directory, output_directory, "diff")
        os.chdir("..")
    
    print("모든 작업이 완료되었습니다.")        
    os.chdir("..")


# In[8]:


os.getcwd()


# In[7]:


os.chdir("..")
os.chdir("..")


# In[ ]:




