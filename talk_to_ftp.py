import os
from ftplib import FTP, error_perm
from logger import Logger


class TalkToFTP:
    def __init__(self, ftp_website):
        my_srv = ftp_website.split(",")
        self.host = my_srv[0]
        self.user = my_srv[1]
        self.password = my_srv[2]
        self.directory = my_srv[3]
        self.ftp = False

    def connect(self):
        self.ftp = FTP(self.host, self.user, self.password)

    def disconnect(self):
        self.ftp.quit()

    def go_to(self, folder_path):
        self.ftp.cwd(folder_path)

    def create_folder(self, folder):
        self.ftp.mkd(folder)
        Logger.log_info("FOLDER Created  : " + folder)

    def remove_folder(self, folder):
        self.ftp.rmd(folder)
        Logger.log_info("FOLDER Removed  : " + folder)

    def file_transfer(self, path, srv_path, file_name):
        file = open(os.path.join(path, file_name), 'rb')
        self.ftp.storbinary('STOR ' + srv_path, file)
        file.close()
        Logger.log_info("  FILE Created  : {0} ".format(srv_path))

    def remove_file(self, file):
        # self.ftp.delete(file)
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        try:
            self.ftp.size(file)
        except error_perm:
            # file wasn't uploaded
            pass
        finally:
            self.ftp.delete(file)
            Logger.log_info("  FILE Removed  : " + file)
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        # Logger.log_info("  FILE Removed  : " + file)

    def get_folder_content(self, path):
        init_list = self.ftp.nlst(path)
        new_list = []
        for path in init_list:
            new_list.append(path.replace("\\", os.path.sep).replace("/", os.path.sep))
        return new_list

    def if_exist(self, element, list):
        if element in list:
            return True
        else:
            return False
