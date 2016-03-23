import logging
from wx_lib.wxconfig import Logpath


def log(msg):
	log_path = Logpath.path
	log_out_format = '%(asctime)s  %(levelname)s %(message)s'
	logging.basicConfig(level=logging.INFO, format=log_out_format, datefmt='%Y-%m-%d %H:%M:%S',
	                    filename=log_path, filemode='a')
	logging.info(msg)
