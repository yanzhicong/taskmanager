import os
import sys
import argparse
import time
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_file', type=str, default='task.txt')
parser.add_argument('-g', '--gpu', type=str, default=None)
args = parser.parse_args()


from task import *

def cal_task(cmd_str):
    splits = cmd_str.split(';')

    if len(splits) == 1:
        task = Task(cmd=splits[0], cwd=None, conda_env=None)
    elif len(splits) == 2:
        task = Task(cmd=splits[0], cwd=splits[1], conda_env=None)
    else:
        task = Task(cmd=splits[0], cwd=splits[1], conda_env=splits[2])


    task_id = execute_task(task, gpu=args.gpu)
    wait_task(task_id)

while True:
    try:
        task_list = []

        find_task = False
        with open(args.input_file, 'r') as infile:
            for line in infile:
                if len(line) > 1:
                    task_list.append(line)

        for ind, line in enumerate(task_list):
            if not line.startswith('done'):

                line = line.strip()
                print('processing : ' + line)
                find_task = True
                cal_task(line)
                break

        if find_task:
            task_list = []
            with open(args.input_file, 'r') as infile:
                for line in infile:
                    if len(line) > 1:
                        task_list.append(line.strip())

            task_list[ind] = 'done '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+':'+task_list[ind]

            with open(args.input_file, 'w') as outfile:
                outfile.write('\n'.join(task_list))

        if not find_task:
            time.sleep(10)


    except KeyboardInterrupt:
        print('exit')
        break


