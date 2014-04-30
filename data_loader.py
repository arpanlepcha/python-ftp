__author__ = 'monk'

from ftplib import FTP
import threading
import os


class ThreadedZoom(threading.Thread):

    def __init__(self, file_name, path):
        super(ThreadedZoom, self).__init__()

        self.fp = open(os.path.join(path, file_name), 'wb')
        self.file_name = file_name
        self.connection = FTP('ftp.xxx.xxx')
        self.connection.login('xxxxx','xxxxxxxxxx')
        self.connection.set_pasv(True)

    def run(self):
        """thread run method,called on thread start,writes to a file"""
        self.connection.retrbinary('RETR '+self.file_name, self.callback)
        self.connection.close()
        self.fp.close()

    def callback(self, bin_data):
        self.fp.write(bin_data)


class ZoomOfflineLoader(object):

    def __init__(self, path):
        self.connection = FTP('ftp.xxxx.com')
        self.connection.login('xxxxx','xxxxxx')
        self.connection.set_pasv(True)
        self.path = path

    def thread_factory(self):
        """creates a lot of threads,each to download one zip file at a time"""

        files = self.connection.nlst()
        self.connection.close()

        threads = []
        for file_name in files:
            file_thread = ThreadedZoom(file_name, self.path)
            file_thread.start()
            threads.append(file_thread)

        for thread in threads:
            thread.join()

        return files


def main():
    path = os.path.dirname(__file__)
    data_path = os.path.join(path, 'ftp-data')

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    initiator = ZoomOfflineLoader(data_path)
    files = initiator.thread_factory()

    print "following files were downloaded from the server \n"
    for file_name in files:
        print '******* %s ********' % file_name

if __name__ == "__main__":
    main()
