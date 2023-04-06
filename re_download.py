import subprocess
import os
import sys
# Run a command in the terminal
path = sys.argv[1]
with open('selenium.log', 'r') as log:
    lines = [line.strip() for line in log.readlines() if "Can't downloaded file:" in line.strip()]
    for line in lines:
        file_not_download = line.split("Can't downloaded file:")[-1]
        info_file = file_not_download.split('|')
        # subprocess.run(["python", "mini_project.py", f"-lf {info_file[1]}", f"-d {info_file[2]}")
        result = subprocess.run(f"python {path} manual -lf {info_file[1]} -d {info_file[2]}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        print(result.stderr.decode())

