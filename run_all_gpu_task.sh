screen -S task0 -d -m python task_server.py -i task_gpu0.txt -g 0
screen -S task1 -d -m python task_server.py -i task_gpu1.txt -g 1
screen -S task2 -d -m python task_server.py -i task_gpu2.txt -g 2
screen -S task3 -d -m python task_server.py -i task_gpu3.txt -g 3

