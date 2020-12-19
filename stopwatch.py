import atexit
from time import time, strftime, localtime
from datetime import timedelta

def seconds_to_string(elapsed=None):
	if elapsed is None:
		return strftime("%Y-%m-%d %H:%M:%S", localtime())
	else:
		return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
	line = "="*40
	print(line)
	print(seconds_to_string(), '-', s)
	if elapsed:
		print("Elapsed time: " , elapsed)
		print(line)
		print()

def endlog():
	end = clock()
	elapsed = end - start
	log("End Program", seconds_to_string(elapsed))

start = clock()
atexit.register(endlog)
log("Start Program")