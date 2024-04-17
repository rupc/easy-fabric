#!/usr/bin/python3

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

# 스택 이름 정의
stack_name = 'hlfcaliper'

def find_yaml_files(directory):
    """지정된 디렉토리에서 모든 YAML 파일의 경로를 찾습니다."""
    yaml_files = []
    for file in os.listdir(directory):
        if file.endswith(".yaml"):
            yaml_files.append(os.path.join(directory, file))
    return yaml_files

def deploy_stack(compose_file):
    """주어진 compose 파일로 Docker 스택을 배포합니다."""
    command = f'docker stack deploy -c {compose_file} {stack_name}'
    try:
        # subprocess.run을 사용하여 명령어 실행
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return f"{compose_file}: success deploy, {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"{compose_file}: fail deploy, {e.stderr}"

def main():
    # 'swarm' 디렉토리 내의 모든 .yaml 파일을 찾습니다.
    compose_files = find_yaml_files('swarm')
    
    # ThreadPoolExecutor를 사용하여 병렬 실행
    with ThreadPoolExecutor(max_workers=len(compose_files)) as executor:
        results = list(executor.map(deploy_stack, compose_files))
    
    # 결과 출력
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
