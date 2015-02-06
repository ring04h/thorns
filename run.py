#!/usr/bin/env python
# encoding: utf-8
# tasks.py
# email: ringzero@0x557.org

import sys
from tasks import *
from wyfunc import make_target_list

def start_nmap_dispath(targets, taskid=None):
	print '-' * 50
	target_list = make_target_list(targets)

	for target in target_list:
		print '-' * 50
		print '* push %s to Redis' % target
		print '* AsyncResult:%s' % nmap_dispath.delay(target,taskid=taskid)

	print '-' * 50
	print '* Push nmapscan tasks complete.'
	print '-' * 50

if __name__ == "__main__":
	if len(sys.argv) == 2:
		start_nmap_dispath(sys.argv[1])
		sys.exit(0)
	elif len(sys.argv) == 3:
		start_nmap_dispath(sys.argv[1], sys.argv[2])
	else:
		print ("usage: %s targets taskid" % sys.argv[0])
		sys.exit(-1)