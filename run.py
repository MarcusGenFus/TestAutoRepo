from repo_test import reg_file
import os

def main():
    re = reg_file()
    print(re.list_branches())
    temp = re.read_last_branch()
    if temp == False:
        re.mount_branch("main")
    re.repo_file_checkout("testfile1.txt")
    with open("H:/TestAutoRepo/files/testfile1.txt", "a") as file:
        file.write("new message")
        file.close()
    re.update_config()
    re.repo_file_release()

if __name__ == "__main__":
    main()