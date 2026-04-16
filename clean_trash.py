import argparse
import logging
import os
import time

LOG_FILE = "clean_trash.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(message)s",)
def remove_old_files(trash_folder_path, age_thr):
    now_time = time.time()
    for root, dirs, files in os.walk(trash_folder_path, topdown=False):
        dirs.sort()
        files.sort()
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_age = now_time - os.path.getmtime(file_path)
            if file_age > age_thr:
                os.remove(file_path)
                logging.info(file_path)

def remove_empty_dirs(trash_folder_path):
    for root, dirs, files in os.walk(trash_folder_path, topdown=False):
        dirs.sort()
        if root == trash_folder_path:
            continue
        if len(os.listdir(root)) == 0:
            os.rmdir(root)
            logging.info(root)

def clean_trash_once(trash_folder_path, age_thr):
    remove_old_files(trash_folder_path, age_thr)
    remove_empty_dirs(trash_folder_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trash_folder_path", required=True)
    parser.add_argument("--age_thr", required=True, type=float)
    args = parser.parse_args()
    while True:
        clean_trash_once(args.trash_folder_path, args.age_thr)
        time.sleep(1)

if __name__ == "__main__":
    main()
