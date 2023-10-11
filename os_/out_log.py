from config import config

import os
import datetime


class out_log:
    log_file = config.log_file
    err_file = config.err_file
    log_file_max_size = config.log_file_max_size
    err_file_max_size = config.err_file_max_size

    def __init__(self):
        self.log_file = self.update_file(self.log_file, self.log_file_max_size)
        self.err_file = self.update_file(self.err_file, self.err_file_max_size)

    def update_file(self, file, max_size):
        if not os.path.exists(file[2:5]):
            os.makedirs(file[2:5])
        i = 0
        file = "{}_{}.log".format(file[0:9], i)
        if os.path.exists(file):
            size = os.path.getsize(file)
            while size > max_size:
                i += 1
                file = "{}_{}.log".format(file[0:5], i)
                size = os.path.getsize(file)

        else:
            with open(file, 'w') as f:
                f.write('')

        return file

    def get_log_file(self):
        return slef.log_file

    def get_err_file(self):
        return slef.err_file

    def out_txt(self, id, txt):
        if id == 1:
            file_name = self.log_file
        else:
            file_name = self.err_file
        with open(file_name, mode="a", encoding="utf-8") as f:
            f.write("time: {} -----> {}\n".format(datetime.datetime.now(), txt))
