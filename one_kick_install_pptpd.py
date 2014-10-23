#!/usr/bin/env python

import os
import sys

def pre_work():
	print "******install pptpd**********"
	log = os.popen("apt-get install pptpd -y").read()
	#print log
	#print "****install iptables***********"
	#log = os.popen("apt-get install ipbables -y").read()
	print "******install pptpd done******"

def open_ip_forward():
	with open("/etc/sysctl.conf","r+") as f:
		data = f.readlines()
		line = 0
		while line < len(data):
			if data[line].startswith("#net.ipv4.ip_forward=1"):
				data[line] = "net.ipv4.ip_forward=1"
			line = line + 1
		f.seek(0,0)
		#print data
		f.writelines(data)
	print "******open ip_forward done**********"

def ip_forward():
	ipfwd = os.popen("sysctl -a |grep net.ipv4.ip_forward").read()[-1]
	if ipfwd == 1:
		return
	else:
		open_ip_forward()
	
	
def config_pptp_ip():
	f =  open("/etc/pptpd.conf","r+") 
	data  = f.readlines()
	line = data[-5]
	line = line[1:]
	data[-5] = line
	line = data[-4]
	line = line[1:]
	data[-4] = line
		
	f.seek(0,0)
	f.writelines(data)
	f.close()
	print "*****config pptp ip done*******"

def config_pptp_dns():
	f = open("/etc/ppp/pptpd-options","a+")
	dns2 = "ms-dns 8.8.4.4\n"
	dns1 = "ms-dns 8.8.8.8\n"
	f.write(dns1)
	f.write(dns2)
	f.close()
	print "***********config pptp dns done********"

def config_pptp_users():
	print "*********** add vpn user ************"
	f = open("/etc/ppp/chap-secrets","a+")
	user = raw_input("please input username:\n")
	password = raw_input("please input password:\n")
	line = user + "	" +"pptpd"+"	"+password+"	"+"*"+"	"+"\n"
	#print line
	f.seek(0,2)
	f.write("\n")
	f.writelines(line)
	f.close()

def config_iptables():
	rule = "/sbin/iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE"
	log = os.popen(rule).read()
	print log
	log = os.popen("iptables-save > /etc/iptables-rules").read()
	print log
	f = open("/etc/network/interfaces","r+")
	f.seek(0,2)
	f.writelines("pre-up iptables-restore < /etc/iptables-rules\n")
	f.close()
	print "*******config iptables done**********"


if __name__ == '__main__':
	pre_work()
	ip_forward()
	config_pptp_ip()
	config_pptp_dns()
	config_iptables()
	#config_pptp_users()
	print "************please reboot system ***********"
