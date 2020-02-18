import logging
import os
import time
from Directory import Directory
from File import File
from talk_to_ftp import TalkToFTP
import multiprocessing

def simultaneousFileUploadV1(ftp_website, path, srv_path, file_name):
    from logger import Logger
    from talk_to_ftp import TalkToFTP

    myFtp = TalkToFTP(ftp_website)

    file = open(os.path.join(path, file_name), 'rb')
    myFtp.connect()
    Logger.log_info("  FILE Starting : {0} - (Process : {1})".format(srv_path,os.getpid()))

    myFtp.ftp.storbinary('STOR ' + srv_path, file)
    myFtp.disconnect()
    file.close()
    Logger.log_info("  FILE Done     : {0} - (Process : {1})".format(srv_path,os.getpid()))


class FileUploadTask:
    QUEUE = multiprocessing.Queue()
    IS_RUNNING = True

    def __init__(self,path, srv_path, file_name):
        self.path = path
        self.srv_path = srv_path
        self.file_name = file_name

def simultaneousFileUploadV2(ftp_website, JobQueue):
    from logger import Logger
    from talk_to_ftp import TalkToFTP

    while True:
        if not JobQueue.empty():
            myJob = JobQueue.get()

            myFtp = TalkToFTP(ftp_website)

            file = open(os.path.join(myJob.path, myJob.file_name), 'rb')
            myFtp.connect()
            Logger.log_info("  FILE Starting : {0} - (Process : {1})".format(myJob.srv_path, os.getpid()))
            myFtp.ftp.storbinary('STOR ' + myJob.srv_path, file)
            myFtp.disconnect()
            file.close()
            Logger.log_info("  FILE Done     : {0} - (Process : {1})".format(myJob.srv_path, os.getpid()))
