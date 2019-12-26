import socket
import sys
import time
import os
import tarfile
import argparse

# NOTE: Modify host_addr and host_post at the main entry below to adapt your task.

class FileTransferSender:

    def __init__(self, host_addr, host_port, buffer_size=102400):
        self.HOST_ADDR = host_addr
        self.HOST_PORT = host_port
        self.BUFFER_SIZE = buffer_size

    def get_file_size(self, file_name):
        try:
            return os.path.getsize(file_name)
        except OSError:
            print('File {0} does not exist.'.format(file_name))

    def send(self, file_name, is_directory=False):
        try:
            s = socket.socket()
            s.connect((self.HOST_ADDR, self.HOST_PORT))
            s.send(file_name)
            s.recv(1024)
            s.send(str(is_directory))
            s.recv(1024)
            if(is_directory):
                print('Folder {0} transfer completed.'.format(file_name.split('.')[0]))
            else:
                f = open(file_name, 'rb')
                packet = f.read(self.BUFFER_SIZE)
                start_ts = time.time()
                while(packet):
                    s.send(packet)
                    packet = f.read(self.BUFFER_SIZE)
                end_ts = time.time()
                speed = self.get_file_size(file_name) / (end_ts - start_ts) / 1024 / 1024
                print('File {0} transfer completed, average transfer speed is {1}MB/s.'.format(file_name, round(speed, 2)))
                f.close()
            s.close()
        except socket.error:
            print("Connection error, please check whether the host's service is started or the connection parameters is correct.")

    def recursive_send(self, file_path):
        self.send(file_path, True)
        files = os.listdir(file_path)
        for file in files:
            path = '/'.join([file_path, file])
            if(os.path.isdir(path)):
                self.send(path, True)
                self.recursive_send(path)
            else:
                self.send(path)
                

if __name__ == "__main__":
    try:
        # Modify here
        host_addr = '192.168.1.200'
        host_port = 23333
        sender = FileTransferSender(host_addr, host_port)
        # Do not modify any code except this block unless necessary

        parser = argparse.ArgumentParser(description = 'Remote File Transfer')
        parser.add_argument('-r', '--recursive', help='whether send a single file or a whole folder with files inside it',action='store_true')
        parser.add_argument('filename', help="specify file or folder's path you want to send")
        args = parser.parse_args()
        print('Transfer started.')
        if args.recurive:
            if(os.path.isdir(args.filename)): 
                sender.recursive_send(args.filename)
            else:
                print('Specified path is not a directory, try use without -r argument.')
        else:
            if(os.path.isfile(args.filename)):
                sender.send(args.filename)
            else:
                print('Specified path is not a file, try use -r argument.')
    except IndexError:
        print("Invalid arguments.")
    except KeyboardInterrupt:
        print("Transfer aborted.")