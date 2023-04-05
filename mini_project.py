import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description='Mini project to crawl data from https://www.sgx.com/research-education/derivatives')
parser.add_argument('-d','--days_ago' ,default=0, help="(type:int, default:0) Day users want to get. Choose day ago to download: (0 -> 4 day(s) ago )")
parser.add_argument('run', help='Type:run to start process')
args = parser.parse_args()
days_ago = int(args.days_ago)
if args.run:
    if days_ago > 4 or days_ago < 0:
        print('Please choose another day in range 0 -> 4')
        exit()
    file_process = os.path.join(os.getcwd(), 'crawl_process.py')
    file_re_download = os.path.join(os.getcwd(), 're_download.py')

    subprocess.run(f"python {file_process} auto -d {days_ago}")
    subprocess.run(f"python {file_re_download} {file_process}")