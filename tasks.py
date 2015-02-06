#!/usr/bin/env python
# encoding: utf-8
# tasks.py
# email: ringzero@0x557.org

'''
	Thorns Project 分布式任务控制脚本
	tasks
		-- nmap_dispath			# nmap 扫描调度函数
		-- hydra_dispath 		# hydra 暴力破解调度函数
		-- medusa_dispath 		# medusa 暴力破解调度函数

	worker run()
		--workdir=/home/thorns
'''

import subprocess
from celery import Celery, platforms 

# 初始化芹菜对象
app = Celery()

# 允许celery以root权限启动
platforms.C_FORCE_ROOT = True

# 修改celery的全局配置
app.conf.update(
	CELERY_IMPORTS = ("tasks", ),
	BROKER_URL = 'redis://120.132.54.90:6379/0',
	CELERY_RESULT_BACKEND = 'db+mysql://celery:celery1@3Wscan@42.62.52.62:443/wscan',
	CELERY_TASK_SERIALIZER='json',
	CELERY_RESULT_SERIALIZER='json',
	CELERY_TIMEZONE='Asia/Shanghai',
	CELERY_ENABLE_UTC=True,
	CELERY_REDIS_MAX_CONNECTIONS=5000, # Redis 最大连接数
	BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}, # 如果任务没有在 可见性超时 内确认接收，任务会被重新委派给另一个Worker并执行  默认1 hour.
	# BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True},		# 设置一个传输选项来给消息加上前缀
)

# 失败任务重启休眠时间300秒，最大重试次数5次
# @app.task(bind=True, default_retry_delay=300, max_retries=5)

@app.task
def nmap_dispath(targets, taskid=None):
	# nmap环境参数配置
	run_script_path = '/home/thorns'
	if taskid == None:
		cmdline = 'python wyportmap.py %s' % targets
	else: 
		cmdline = 'python wyportmap.py %s %s' % (targets, taskid)
	nmap_proc = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process_output = nmap_proc.stdout.readlines()
	return process_output

@app.task
def hydra_dispath(targets, protocol, userdic, passdic, taskid=None):
	# 命令执行环境参数配置
	run_script_path = '/home/thorns/script/hydra'
	run_env = '{"LD_LIBRARY_PATH": "/home/thorns/libs/"}'

	if taskid == None:
		cmdline = 'python hydra.py %s %s %s %s' % (target, protocol, userdic, passdic)
	else:
		cmdline = 'python hydra.py %s %s %s %s %s' % (target, protocol, userdic, passdic, taskid)

	nmap_proc = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=run_script_path,env=run_env)

	process_output = nmap_proc.stdout.readlines()
	return process_output

@app.task
def medusa_dispath(targets, protocol, userdic, passdic, taskid=None):
	# 命令执行环境参数配置
	run_script_path = '/home/thorns/script/medusa'
	run_env = '{"LD_LIBRARY_PATH": "/home/thorns/libs/"}'

	if taskid == None:
		cmdline = 'python medusa.py %s %s %s %s' % (target, protocol, userdic, passdic)
	else:
		cmdline = 'python medusa.py %s %s %s %s %s' % (target, protocol, userdic, passdic, taskid)

	nmap_proc = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=run_script_path,env=run_env)

	process_output = nmap_proc.stdout.readlines()
	return process_output





