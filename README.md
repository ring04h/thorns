# thorns
thorns_project 分布式异步队列系统

运行流程
-----------------------------------
* 启动redis内存服务器，作为队列存储数据库使用
* 配置芹菜(celery)运行环境，并连接redis队列内存，读取执行任务，并返回结果存储到后端MySQL数据库
* 配置任务控制台花花(flower)，并连接redis队列内存，管理所有worker客户端与执行的任务队列
* 通过run.py脚本调用celery向队列压入任务
* 通过flower的http api脚本调用api向队列压入任务
* 任务执行的结果自动存入后端数据库

反馈
-----------------------------------
> 微博：http://weibo.com/ringzero<br />
> 邮箱：ringzero@0x557.org<br />

运行环境
-----------------------------------
* CentOS、Kali Linux、Ubuntu、Debian
* Python 2.7.x
* Redis
* MysQL
* Celery
* Tornado

安装配置说明
-----------------------------------
## CentOS
#### 安装 Redis-Server
	

#### 安装 MySQL-python
	sudo yum -y install python-devel mysql-devel subversion-devel
	sudo pip install MySQL-python

#### 安装 pip
	wget https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz
	tar zvxf pip-6.0.8.tar.gz
	cd pip-6.0.8
	sudo python setup.py install
#### 安装 Celery

#### 安装 Flower

使用说明
-----------------------------------
#### HTTP API 远程调用
    重启 worker 线程池:
    $ curl -X POST http://thorns.wuyun.org:8080/api/worker/pool/restart/myworker
    
    远程调用HTTP API启动一个nmap扫描任务：
    $ curl -X POST -d '{"args":["42.62.52.62",2222]}' http://thorns.wuyun.org:8080/api/task/send-task/tasks.nmap_dispath
    
    强制结束一个正在执行的任务：
    $ curl -X POST -d 'terminate=True' http://thorns.wuyun.org:8088/api/task/revoke/a9361c1b-fd1d-4f48-9be2-8656a57e906b

