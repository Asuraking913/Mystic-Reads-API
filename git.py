import os

def git_commit():
    commit_m = input("Enter commit message: ")
    return os.system(f"git commit -m '{commit_m}'")

def git_add(): 
    return os.system("git add .")

def git_push(): 
    return os.system("git push origin master")

def git_add_url():
    url = input("Enter git url: ")
    return os.system(f"git remote add origin {url}")

def git_init():
    return os.system("git init")

file_list = os.listdir()

if ".git" in file_list:
    git_add()
    git_commit()
    git_push()
else:
    git_init()
    git_add()
    git_commit()
    git_add_url()
    git_push()


