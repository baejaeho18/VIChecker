#!/usr/bin/env python
# coding: utf-8

# In[2]:


def commit_logger(project_names):
    
    for directory in project_names:
#         if not os.path.exists(os.path.join(directory, ".git")):
#             print(directory)
#             continue  # Git 저장소가 아닌 경우 스킵

        os.chdir(directory)  # 리포지토0리 디렉토리로 이동

        # 스크립트를 실행하여 Git 로그를 파일로 저장
        start_date = "2021-10-01"
        end_date = "2023-07-18"  # 원하는 날짜로 수정
        output_file = f"{directory}-log.json"

        # logger.sh 스크립트 실행
        # Shell 스크립트를 실행하고 표준 입력으로 start_date, end_date, output_file을 전달
        subprocess.run(['bash', '../logger.sh', start_date, end_date, output_file])
        
        os.chdir("..")
        print(directory, "의 커밋로그를 저장하였습니다.")
        
    print("모든 프로젝트의 log.json 파일을 생성하였습니다.")

def validate_log_json_file(project_names, output_directory):

    for directory in project_names:
        
        commits = []
        log_file = f"{directory}-log.json"
        
        os.chdir(directory)  # 리포지토0리 디렉토리로 이동
        
        with open(log_file, "r") as f:
            try:
                log_data = json.load(f)
                commits.extend(log_data)
            except json.JSONDecodeError:
                combined_lines = ""
                # JSON 파싱 오류가 발생한 경우 줄 단위로 읽어서 이어붙이기
                # 여긴 미완성 - 수동으로 일단 하자...
        
        os.chdir("..")
        # validate된 json파일을 "../{output_directory"/{log_file}"에 저장
    print("모든 json file의 유효성을 검사하였습니다.")
    


# In[28]:


import os
import json
import subprocess
    
def add_changed_file_list(project_names, output_directory):
    # 만들어진 json 파일에 changed_file_list 항목을 추가해서 저장
    # 필요한 항목만 남겨서 새로 저장 (hash, parent, date, subject, body, changed_file_list)
    
    for directory in project_names:
        commits = []
        
        log_file = os.path.join(os.getcwd(), output_directory, f"{directory}-git-log.json")
        with open(log_file, "r", encoding='utf-8') as f:
            data = f.read()
            raw_data = r''+data
            try:
                commits = json.loads(raw_data)
#                 print(commits)
            except json.JSONDecodeError as e:
                print(f"JSON 디코드 오류: {e}")
        
        os.chdir(directory)
        
        cnt = 0
        for commit in commits:
            files = []
            java_files = []
            commit['changed_file_list'] = []
            
            changed_file_list = subprocess.run(['git', 'show', commit['commitHash'], '--name-only', '--pretty=format:%b'], capture_output=True, text=True)
            if changed_file_list.returncode == 0 and changed_file_list.stdout:
                lines = changed_file_list.stdout.split('\n')
                # Process the rest of the code using the 'lines' variable
            else:
                # Handle the case when the Git command didn't execute successfully
                print("Failed to get the changed file list of ", commit['commitHash'])
            
            for line in lines:
                if line.strip() in commit['body']:
                    continue
                elif line.strip() != '':
                    files.append(line.strip())

            java_files = [file for file in files if file.endswith('.java')]
            java_files = list(filter(lambda file: 'src/test' not in file, java_files))
            
            if java_files != []:
                commit['changed_file_list'] = java_files
                cnt += 1
                # print(commit['commitHash'])
                # print(cnt, ":", commit['changed_file_list'])
        
        os.chdir("..")
        new_log_file = os.path.join(output_directory, f"{directory}-files-log.json")
        with open(new_log_file, "w", encoding='utf-8') as nf:
            json.dump(commits, nf, indent=2)
        print(directory, "- log.json 파일에 파일목록을 추가하였습니다.")
        
    print("모든 json파일을 업데이트하였습니다.")


# In[33]:


if __name__ == "__main__":
    directories = ["h2database", "bc-java", "pgjdbc", "junit4", "gson", "guava"]
    output_directory = "commit-logs"
    # commit_logger(directories)
    add_changed_file_list(directories, output_directory)


# In[32]:


os.getcwd()


# In[31]:


os.chdir("..")


# In[ ]:




