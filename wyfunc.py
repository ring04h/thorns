#!/usr/bin/env python
# encoding: utf-8
# wyfunc.py
# email: ringzero@0x557.org

def ip2num(ip):
	ip = [int(x) for x in ip.split('.')]
	return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

def num2ip(num):
	return '%s.%s.%s.%s' % (
		(num & 0xff000000) >> 24,
		(num & 0x00ff0000) >> 16,
		(num & 0x0000ff00) >> 8,
		num & 0x000000ff
	)
 
def gen_ips(start, end):
	"""生成IP地址"""
	# if num & 0xff 过滤掉 最后一段为 0 的IP
	return [num2ip(num) for num in range(start, end + 1) if num & 0xff]

def make_ips_c_block(ipaddr):
	address = {}
	ipaddr = ipaddr.split('.')
	ipaddr[3] = '0'
	ipaddr = '.'.join(ipaddr)

	address[ipaddr] = gen_ips(ip2num(ipaddr),ip2num(ipaddr) + 254)
	return address

def ip_check(ip):
	q = ip.split('.')
	return len(q) == 4 and len(filter(lambda x: x >= 0 and x <= 255, \
		map(int, filter(lambda x: x.isdigit(), q)))) == 4

def make_target_list(targets):
	target_list = []
	process_nmap_count = 1
	startip, endip = targets.split('-')
	if not ip_check(startip):
		print '* StartIP format error'
	else:
		endip_len = len(endip.split('.'))
		startip_num = ip2num(startip)
		if endip_len == 1: # 结束IP为数字的场景
			startip_endnum = startip.split('.')[3]
			target_count =  int(endip) - int(startip_endnum)
			if target_count >= 0:
				target_list.append(num2ip(startip_num))
				# 每10个IP分配到一个wyportmap子进程上
				# 更新：为每个独立的IP创建一个单独的任务，并删除掉开始IP，修改的时候注释掉上面那行
				for i in xrange(0,(target_count+process_nmap_count-1)/process_nmap_count):
					ip_count = (i * process_nmap_count) + process_nmap_count
					remaining_count = target_count - ip_count
					if remaining_count > 0:
						scan_startip = num2ip(startip_num)
						endip_num = startip_num + process_nmap_count
						startip_num = endip_num
						# target_option = '%s-%s' % (scan_startip, num2ip(endip_num))
						target_option = num2ip(endip_num)
						target_list.append(target_option)
					else:
						scan_startip = num2ip(startip_num)
						endip_num = startip_num + process_nmap_count + remaining_count
						startip_num = endip_num
						# target_option = '%s-%s' % (scan_startip, num2ip(endip_num))
						target_option = num2ip(endip_num)
						target_list.append(target_option)
			else:
				print '* EndIP Less than StartIP'
		elif endip_len == 4:
			if ip_check(endip):
				startip_num = ip2num(startip)
				endip_num = ip2num(endip)
				if startip_num <= endip_num:
					target_count =  endip_num - startip_num
					if target_count >= 0:
						for i in xrange(0,(target_count+process_nmap_count-1)/process_nmap_count):
							ip_count = (i * process_nmap_count) + process_nmap_count
							remaining_count = target_count - ip_count
							if remaining_count > 0:
								scan_startip = num2ip(startip_num)
								endip_num = startip_num + process_nmap_count
								startip_num = endip_num
								target_option = '%s-%s' % (scan_startip, num2ip(endip_num))
								target_list.append(target_option)
							else:
								scan_startip = num2ip(startip_num)
								endip_num = startip_num + process_nmap_count + remaining_count
								startip_num = endip_num
								target_option = '%s-%s' % (scan_startip, num2ip(endip_num))
								target_list.append(target_option)
				else:
					print '* EndIP Less than StartIP'
			else:
				print '* EndIP format error'	
		else:
			print '* EndIP format error'

	return target_list


