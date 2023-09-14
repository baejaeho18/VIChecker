#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import git

def get_repo_path(project_list_file):
    with open(project_list_file, "r") as file:
        project_urls = file.readlines()
    print(project_urls)
    return project_urls

def clone_project_and_update_gitignore(project_urls):
    project_names = []
    
    # 각 프로젝트 클론 및 .gitignore 업데이트
    for project_url in project_urls:
        project_url = project_url.strip()  # 공백과 개행 문자 제거
        if project_url:
            project_name = project_url.split("/")[-1].rstrip(".git")
            project_names.append(project_name)
    
            # 프로젝트 클론 경로
            clone_folder = os.path.join(os.getcwd(), project_name)

            # Check if the repository already exists in the specified folder
            if os.path.exists(clone_folder):
                # If it exists, fetch the latest changes
                repo = git.Repo(clone_folder)
                origin = repo.remote("origin")
                origin.fetch()
                print(project_name, "프로젝트를 fetch하고, ", end='')
            else:
                # If it doesn't exist, clone it
                git.Repo.clone_from(project_url, clone_folder)
                print(project_name, "프로젝트를 clone하고,", end='')

            # .gitignore 파일 열고 프로젝트 이름 추가
            with open(".gitignore", "a") as gitignore:
                gitignore.write(f"{project_name}/\n")
            print(".gitignore를 업데이트했습니다.")
            
    print("클론이 모두 완료되었습니다.")
    return project_names

if __name__ == "__main__":
    project_list_file = "projectLIst.txt"
    project_list = get_repo_path(project_list_file)
    clone_project_and_update_gitignore(project_list)


# In[ ]:




