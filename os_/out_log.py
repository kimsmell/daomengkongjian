import os
import datetime

class out_log:
    log_file = "./log.log"
    err_file = "./err.log"


    def get_log_file(slef):
        return slef.log_file
    
    def get_err_file(slef):
        return slef.err_file

    def out_txt(slef, file_name, txt):
        with open(file_name, mode="a", encoding="utf-8") as f:
            f.write("time: {} -----> {}\n".format(datetime.datetime.now(), txt))
            