import os
import sys
from uuid import uuid4
import threading
from collections import namedtuple
import platform

Task = namedtuple('Task', ['cmd', 'cwd', 'conda_env'])


task_dict = {}
thread_dict = {}


def execute_task(task, gpu=None):
    task_id = uuid4()

    task_dict[task_id] = task

    cmd = ''


    if task.cwd is not None and len(task.cwd) != 0:
        if platform.system() == "Windows":
            cmd += 'cd /D ' + str(task.cwd) + "&&"
        else:
            cmd += 'cd ' + str(task.cwd) + ';'

    if gpu is not None:
        cmd += 'CUDA_VISIBLE_DEVICES={} '.format(gpu)

    if task.conda_env is not None and len(task.conda_env) != 0:
        if platform.system() == "Windows":
            cmd += 'conda run --no-capture-output -n ' + str(task.conda_env) + " "
        else:
            cmd += 'conda run --no-capture-output -n ' + str(task.conda_env) + " "

    cmd += task.cmd


    print(cmd)
    t = threading.Thread(target=lambda cmd:os.system(cmd), args=(cmd, ))
    t.start()
    t.join()
    thread_dict[task_id] = t

    return task_id




def get_task_state(task_id):
    t = thread_dict[task_id]
    return t.is_alive()

def wait_task(task_id):
    thread_dict[task_id].join()

