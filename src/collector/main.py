import os
import sys
from base import Issue
from eur_radiology import EurRadiology

# main.py getJouDir -j eur_radiology -v 32 -i 10

def get_issue(journal:str, volume:int, issue:int) -> Issue:
    if journal == "eur_radiology":
        eur_radiology = EurRadiology()
        issue = eur_radiology.get_issue(32, 10)
        return issue
    else:
        sys.exit('failed to get <{}> contents!'.format(journal))

def write_to_file(issue:Issue, path:str, file_name:str):
    if not os.path.exists(path):
        print("make dir:{}".format(path))
        os.mkdir(path)
    file_path = os.path.join(path, file_name)
    file = open(file_path, mode="w", encoding='utf-8')
    index = 1
    for paper in issue.papers:
        file.write("## {} {}\n\n".format(index, paper.title))
        file.write("<{}>\n\n".format(paper.herf))
        index += 1
    file.close()

def main():
    cwd = os.getcwd()
    file_dir = __file__
    print("cwd:{}, file_dir:{}".format(cwd, file_dir))

    # parse getJouDir arg, is stupid way!
    if len(sys.argv) != 8:
        print("usage: getJouDir -j <journal_name> -v <volume> -i <issue>")
        sys.exit()

    if sys.argv[1] == "getJouDir":
        journal:str = ""
        volume_int:int
        issue_int:int

        cmd = sys.argv[2:]
        for index in range(3):
            option = cmd[index * 2]
            argument = cmd[index * 2 + 1]
            if option == "-j":
                journal = argument
            elif option == "-v":
                volume_int = argument
            elif option == "-i":
                issue_int = argument

        issue = get_issue(journal, volume_int, issue_int)
        if (issue is not None):
            write_to_file(issue, os.path.join(cwd, "out"), "{} {} {}.md".format(journal, volume_int, issue_int))

if __name__ == "__main__":
    main()