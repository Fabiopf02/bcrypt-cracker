import sys
import bcrypt
from concurrent.futures import ThreadPoolExecutor
from libs import log
from colored import fg
import os
import psutil
import time

color = fg('#008000')
color_info = fg('#000080')
fail = fg('#808000')
success = fg('#800080')

def verify_password_with_hash(password, hashed_password):
    result = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    return {
        'password': password,
        'result': result
    }

def verify_password(hashed_password):
    def verify(password):
        return verify_password_with_hash(password, hashed_password)
    return verify

def parallel_hashing_and_verification(passwords, hashed_password, max_workers, chunks):
    count = 0
    total = len(passwords)
    start_time = time.time()
    with ThreadPoolExecutor(max_workers) as executor:
        match_found = False
        for processed in executor.map(verify_password(hashed_password), passwords, chunksize=chunks):
            count += 1
            password = processed['password']
            cpu = f'cpu: {color_info}{psutil.cpu_percent():05.1f}%{color}'
            memory = f'memory: {color_info}{psutil.virtual_memory().percent}%{color}'
            elapsed_time = time.time() - start_time
            hps = count / elapsed_time
            estimated_time = (((total - count) / hps) % 3600) // 60
            hashes_per_second = f'hashes/sec: {color_info}{hps:.2f}{color}'
            estimated_time = f'estimated time: {color_info}{estimated_time:.2f}min{color}'
            curr_pass = f'password: {color_info}{password}{color}'
            suffix = f'| {color_info}{count}/{total}{color} | {cpu} | {memory} | {hashes_per_second} | {estimated_time} | {curr_pass}'
            log(count, total, suffix=suffix)
            if processed['result']:
                match_found = password
                print()
                executor.shutdown(wait=False)
                break
        return match_found

if __name__ == "__main__":
    cpu_count = os.cpu_count()
    print(f'{color_info}CPU (OS): {cpu_count}')
    hashed_password = input(f'{color_info}Hash: {color}')
    max_workers = int(input(f'{color_info}Max workers(Threads | default={cpu_count}): {color}') or cpu_count)
    chunks = int(input(f'{color_info}Chunksize(default=4): {color}') or 4)

    with open("wordlist.txt", "r", encoding="utf8") as text_file:
        password_list = text_file.read().splitlines()
        start_time = time.time()
        verification_result = parallel_hashing_and_verification(password_list, hashed_password, max_workers, chunks)
        elapsed_time = (time.time() - start_time) / 60
        if verification_result:
            print(f'{success}Password found: {verification_result}')
        else:
            print(f'{fail}Password not found!')
        print(f'{fail}Processing time: {elapsed_time:.2f} min')
