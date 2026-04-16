import argparse
import os
import re

def read_gitignore(project_dir):
    gitignore_path = os.path.join(project_dir, ".gitignore")
    rules = []
    with open(gitignore_path, "r", encoding="utf-8") as gitignore_file:
        for line in gitignore_file:
            line = line.strip().lstrip("\ufeff")
            if line != "":
                rules.append(line.replace("\\", "/"))
    return rules

def get_files(project_dir):
    result = []
    for root, dirs, files in os.walk(project_dir):
        dirs.sort()
        files.sort()
        for file_name in files:
            if file_name == ".gitignore":
                continue
            file_path = os.path.join(root, file_name)
            short_path = os.path.relpath(file_path, project_dir)
            short_path = short_path.replace("\\", "/")
            result.append(short_path)
    return result

def make_regex(rule):
    return r"^.*" + re.escape(rule[1:]) + r"$"

def is_ignored(file_path, rule):
    if rule.startswith("*"):
        regular = make_regex(rule)
        return re.match(regular, file_path) is not None
    return file_path == rule

def print_ignored(project_dir):
    rules = read_gitignore(project_dir)
    files = get_files(project_dir)
    used_files = set()
    print("Ignored files:")
    for rule in rules:
        for file_path in files:
            if file_path in used_files:
                continue
            if is_ignored(file_path, rule):
                used_files.add(file_path)
                full_path = os.path.join(project_dir, file_path)
                full_path = full_path.replace("\\", "/")
                print(full_path, "ignored by expression", rule)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_dir", required=True)
    args = parser.parse_args()
    print_ignored(args.project_dir)

if __name__ == "__main__":
    main()
