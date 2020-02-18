import os
import multiprocessing

def simultaneousFileUploadV1(ftp_website, path, srv_path, file_name):
    """
    Upload file to ftp_website
    """
    from logger import Logger
    from talk_to_ftp import TalkToFTP
    myFtp = TalkToFTP(ftp_website)
    with open(os.path.join(path, file_name), 'rb') as file:
        Logger.log_info("  FILE Starting : {0} - (Process : {1})".format(srv_path,os.getpid()))
        myFtp.connect()
        myFtp.ftp.storbinary('STOR ' + srv_path, file)
        myFtp.disconnect()
        Logger.log_info("  FILE Done     : {0} - (Process : {1})".format(srv_path,os.getpid()))


class FileUploadTask:
    """
    Holds data necessary for file upload.
    """
    QUEUE = multiprocessing.Queue()
    IS_RUNNING = True

    def __init__(self,path, srv_path, file_name):
        self.path = path
        self.srv_path = srv_path
        self.file_name = file_name

def simultaneousFileUploadV2(ftp_website, JobQueue):
    """
    Wait and execute file upload jobs from jobQueue
    """
    from logger import Logger
    from talk_to_ftp import TalkToFTP
    from File import File
    while True:
        # wait for job to be sent over from queue
        if not JobQueue.empty():
            myJob = JobQueue.get()
            pathToFile = os.path.join(myJob.path, myJob.file_name)
            # if file exists, we send it to ftp server
            if os.path.isfile(pathToFile):
                with open(pathToFile, 'rb') as file:
                    myFtp = TalkToFTP(ftp_website)
                    myFtp.connect()
                    Logger.log_info("  FILE Starting : {0} - (Process : {1})".format(myJob.srv_path, os.getpid()))
                    myFtp.ftp.storbinary('STOR ' + myJob.srv_path, file)
                    myFtp.disconnect()
                    Logger.log_info("  FILE Done     : {0} - (Process : {1})".format(myJob.srv_path, os.getpid()))




