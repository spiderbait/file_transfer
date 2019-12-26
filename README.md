#使用方法
##getter.py
在接收端机器执行命令启动接收端守护进程
python getter.py
可加nohup &后台常驻运行
默认文件接收路径和日志存放路径均为执行该脚本的当前路径，可以通过分别更改main方法中的file_path和log_path来实现客制化
支持同时接收多个文件

##sender.py
对于文件，执行命令：
python sender.py example_file
对于文件夹，执行命令
python sender.py -r example_folder

#可配置参数
##getter.py
bind_host       绑定本地接收端主机地址
bind_port       绑定本地接收端主机端口
buffer_size     缓冲块大小（字节）
log_path        日志存放路径，默认为当前路径
file_path       文件存放路径，默认为当前路径

##sender.py
host_addr       目标主机地址
host_port       目标主机端口
buffer_size     缓冲块大小（字节）