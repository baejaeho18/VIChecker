import os
import subprocess
import json
import sys
import openai
import re

# Read API key from file
with open('../../api_key.txt', 'r', encoding='utf-8') as file:
    api_key = file.read().strip()

# Set the OpenAI API key
openai.api_key = api_key

def ask_to_gpt(file_path, content):
    # Make a question using the API
    question = "Can you check the following code and if there is any CWE or CVE related vulnerability, can you point it out the number of CWE or CVE and describe it?\n" + content
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
#        model="gpt-4",
        messages=[
            {"role": "user", "content": question}
        ],
    )
    # generated answer
    answer = response['choices'][0]['message']['content'].strip()
    # Record the answer
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(answer)   
    except:
        print(f"Answer Write 오류")

def remove_comments(code):
    # Remove /* ... */ style comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove // style comments
    code = re.sub(r'//.*', '', code)

    return code

import os

def read_java_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if "_after" in file and file.endswith(".java"):
                file_path = os.path.join(root, file)
                response_file_path = file_path.replace(".java", "_response.txt")
                if not os.path.exists(response_file_path):
                    file_size = os.path.getsize(file_path)
                    if file_size <= 80 * 1024:  # 80KB in bytes
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # content = remove_comments(content)
                            print(file_path)
                            # ask_to_gpt(file_path.replace(".java", "_response.txt"), content)
                            try:
                                ask_to_gpt(response_file_path, content)
                            except Exception as e:
                                print(f"Response Error: {str(e)}")
                    else:
                        print(f"Ignored {file_path} - File size exceeds 80KB")

def read_diff_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_diff.txt"):
                file_path = os.path.join(root, file)
                response_file_path = file_path.replace(".txt", "_response.txt")
                if not os.path.exists(response_file_path):
                    file_size = os.path.getsize(file_path)
                    if file_size <= 80 * 1024:  # 80KB in bytes
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            print(file_path)
                            try:
                                ask_to_gpt(response_file_path, content)
                            except Exception as e:
                                print(f"Response Error: {str(e)}")
                    else:
                        print(f"Ignored {file_path} - File size exceeds 80KB")


# 현재 디렉토리에서 자바 파일 읽기
dir_path = os.getcwd()
read_diff_files(dir_path)
# read_java_files(dir_path)