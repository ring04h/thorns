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
* Supervisord

安装配置说明
-----------------------------------
## CentOS 服务端

#### 安装 Redis-Server
	$ wget http://download.redis.io/releases/redis-2.8.19.tar.gz
	$ tar xzf redis-2.8.19.tar.gz
	$ cd redis-2.8.19
	$ make
	$ sudo cp src/redis-server /usr/bin/
	$ sudo cp redis.conf /etc/redis.conf
	/* 修改 /etc/redis.conf 37行，将daemonize no改为daemonize yes，让redis后台运行 */
	$ sudo vim /etc/redis.conf
	daemonize yes
	# 启动Redis-Server
	$ sudo redis-server /etc/redis.conf

#### 安装 pip
	$ wget https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz
	$ tar zvxf pip-6.0.8.tar.gz
	$ cd pip-6.0.8
	$ sudo python setup.py install

#### 安装 MySQL-python
	$ sudo yum -y install python-devel mysql-devel subversion-devel
	$ sudo pip install MySQL-python SQLAlchemy

#### 安装 Celery
	$ sudo pip install -U celery[redis]

#### 安装 Flower & 下载thorns运行环境代码
	$ cd /home/
	$ sudo yum -y install git
	$ git clone https://github.com/ring04h/thorns.git
	$ cd /home/thorns/src
	$ tar zvxf flower.tar.gz
	$ cd flower-0.7.3
	$ python setup.py install
	/* 启动Flower 这里的redis ip可以配置为你的外网的IP */
	$ celery flower --port=8080 --broker=redis://127.0.0.1:6379/0 &
	建议使用Supervisord的守护进程来启动Flower，确保系统7*24小时的稳定性

#### 安装 Supervisord
	$ sudo pip install supervisor
	$ sudo cp /home/thorns/src/supervisord_server.conf /etc/supervisord.conf
	/* 修改 /etc/supervisord.conf 141行 修改redis ip为你自己的ip --broker=redis://127.0.0.1:6379/0 */
	/* 修改 /etc/supervisord.conf 153行 修改programe为你想定义的worker名称 [program:worker-ringzero] */
	$ sudo vim /etc/supervisord.conf
	/* 启动 supervisord */
	$ supervisord -c /etc/supervisord.conf
	http://127.0.0.1:9001/ 可以在线守护管理thorns的进程，实现远程重启

#### 检查各服务是否正常启动后，开始配置客户端任务脚本
	1、http://youip:8080/  thorns 控制台
	2、http://youip:9001/  supervisord 控制台
	3、修改tasks.py内的芹菜配置
	对应你自己的redis-server服务器IP
	BROKER_URL = 'redis://120.132.54.90:6379/0',
	对应你自己的MySQL-server服务器IP
	CELERY_RESULT_BACKEND = 'db+mysql://celery:celery1@3Wscan@42.62.52.62:443/wscan',

	配置完毕后，就可以部署多台客户端进行分布式任务执行了

## CentOS 客户端（建议大规模部署）
	# 安装 git & 下载 thorns_project
	$ sudo yum -y install git
	$ cd /home/
	$ git clone https://github.com/ring04h/thorns.git

	# 安装 pip
	$ wget https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz
	$ tar zvxf pip-6.0.8.tar.gz
	$ cd pip-6.0.8
	$ sudo python setup.py install

	# 安装 MySQL-python
	$ sudo yum -y install python-devel mysql-devel subversion-devel
	$ sudo pip install MySQL-python SQLAlchemy

	# 安装 nmap
	# 32位系统
	$ sudo rpm -vhU https://nmap.org/dist/nmap-6.47-1.i386.rpm
	# 64位系统
	$ sudo rpm -vhU https://nmap.org/dist/nmap-6.47-1.x86_64.rpm

	# 安装 Celery
	$ sudo pip install -U celery[redis]

	# 安装 Supervisord
	$ sudo pip install supervisor
	$ sudo cp /home/thorns/src/supervisord_client.conf /etc/supervisord.conf
	/* 修改 /etc/supervisord.conf 140行 修改programe为你想定义的worker名称 [program:worker-ringzero] */
	$ sudo vim /etc/supervisord.conf
	/* 启动 supervisord */
	$ supervisord -c /etc/supervisord.conf
	http://127.0.0.1:9001/ 可以在线守护管理thorns的进程，实现远程重启

	# 修改tasks.py内的芹菜配置（分布式任务关键配置项）
	对应你自己的redis-server服务器IP
	BROKER_URL = 'redis://120.132.54.90:6379/0',
	对应你自己的MySQL-server服务器IP
	CELERY_RESULT_BACKEND = 'db+mysql://celery:celery1@3Wscan@42.62.52.62:443/wscan',

	# 环境搭建完毕，这时候访问thorns project的控制台，就会发现worker客户端已经出现在那里
	演示地址：http://thorns.wuyun.org:8080/
	你的请访问：http://youip:8080/


使用说明(可客户端发起任务也可http api发起任务)
-----------------------------------
#### 命令行调用
	在你的任意一台worker客户端，或者thorns服务端
	$ cd /home/thorns/
	$ python run.py 42.62.52.1-42.62.62.254 188
	$ python run.py 42.62.52.1-254 189
	均可以向redis压入nmap扫描任务，worker客户端的分布式集群会自动分发任务执行，并存储到后台数据库
	记得修改wyportmap.py里面的扫描结果，存到你自己的数据库
	
	reinhard-mbp:thorns reinhard$ python run.py 42.62.52.1-254 189
	--------------------------------------------------
	* push 42.62.52.1 to Redis
	* AsyncResult:23147d02-294d-41e5-84e5-5e1b15e72fc4
	--------------------------------------------------
	* push 42.62.52.2 to Redis
	* AsyncResult:542984a4-4434-475f-9a62-bfc81206ea57
	--------------------------------------------------
	* push 42.62.52.3 to Redis
	* AsyncResult:7d005661-d719-41ef-babc-4c853b2c49cc
	--------------------------------------------------
	* push 42.62.52.4 to Redis
	* AsyncResult:ddcf9486-09d9-4dd2-9bb4-2618e6a161b8
	--------------------------------------------------

	wyportmap相关帮助: https://github.com/ring04h/wyportmap

#### HTTP API 远程调用
    重启 worker 线程池:
    $ curl -X POST http://thorns.wuyun.org:8080/api/worker/pool/restart/myworker
    
    远程调用HTTP API启动一个nmap扫描任务：
    $ curl -X POST -d '{"args":["42.62.52.62",2222]}' http://thorns.wuyun.org:8080/api/task/send-task/tasks.nmap_dispath

    强制结束一个正在执行的任务：
    $ curl -X POST -d 'terminate=True' http://thorns.wuyun.org:8088/api/task/revoke/a9361c1b-fd1d-4f48-9be2-8656a57e906b

