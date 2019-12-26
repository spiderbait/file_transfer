import socket
import sys
import time
import tarfile
import os

# NOTE: Specify bind_host, bind_port and log_path below at the main entry to initial this FileTransferDaemon.

class FileTransferDaemon:

    def __init__(self, bind_host, bind_port, buffer_size=102400, log_path='transfer.log', file_path=''):
        self.BIND_HOST = bind_host
        self.BIND_PORT = bind_port
        self.BUFFER_SIZE = buffer_size
        self.LOG_PATH = log_path
        self.FILE_PATH = file_path if file_path.endswith('/') or file_path == '' else file_path + '/' 
    
    def start(self):
        s = socket.socket()
        host = socket.gethostname()
        s.bind((self.BIND_HOST, self.BIND_PORT))
        s.listen(5)

        print('FileTransferDaemon started at {0}:{1}, ready to receive files.'.format(self.BIND_HOST, self.BIND_PORT))
        while True:
            info = ''
            conn, addr = s.accept()
            conn.send('filename')
            filename = conn.recv(1024)
            conn.send('is_directory')
            is_directory = conn.recv(1024)
            print(is_directory)
            if(is_directory == 'True'):
                if(os.path.exists(filename)):
                    continue
                else:
                    os.mkdir(filename)
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                info = '{0} - INFO: Folder {1} from host {2} transfer completed.'.format(ts, filename.split('.')[0], host)
            else:
                f = open(self.FILE_PATH + filename, 'wb')
                while True:
                    packet = conn.recv(self.BUFFER_SIZE)
                    if not packet:
                        log = open(log_path, 'a')
                        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                        info = '{0} - INFO: File {1} from host {2} transfer completed.'.format(ts, filename, host)
                        log.write(info + '\n')
                        log.close()
                        conn.close()
                        f.close()
                        break
                    f.write(packet)
            print(info)
    

if __name__ == "__main__":

    try:
        # Modify here
        bind_host = '192.168.1.200'
        bind_post = 23333
        log_path = 'transfer.log'
        file_path = ''
        # Do not modify any code except this block unless necessary.

        transferd = FileTransferDaemon(bind_host, bind_post, log_path=log_path, file_path=file_path)
        transferd.start()
    except KeyboardInterrupt:
        print("Bye!")