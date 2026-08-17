import os
import sys

def get_msg(error_msg, error_details:sys):
    _,_,exc_tb = error_details.exc_info()

    filename = exc_tb.tb_frame.f_code.co_filename
    lineno = exc_tb.tb_lineno

    msg = 'Error occured in Python script name [{0}] line no [{1}] error message [{2}]'.format(
        filename, lineno, error_msg
    )

    return msg


class CustomeException(Exception):
    def __init__(self, error_msg, error_details:sys):
        super().__init__(error_msg)
        self.error_msg = get_msg(error_msg, error_details)

    def __str__(self):
        return self.error_msg


