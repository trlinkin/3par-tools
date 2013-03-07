#!/usr/bin/python

# Thomas Linkin - 4/6/10
# 3Par 2.3.1 Hosts Export Script
# This script exports the currently defined hosts on 
# an Inserv 2.3.1 OS, and creates the createhost statements
# required to import them into a new system. This script 
# saves the output as 'creat_hosts_3par.cmds.'

import sys
import paramiko
import getpass
import socket
import string
import re
import getopt
import os.path

array = paramiko.SSHClient()
array.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname = "address or IP of array"
arr_username = "3paradm"
arr_password = "your admin password here"


# OPERATION: Could have done this better
#  Sure, there is probably some elegant way to do what im doing, but it got the job done.
#  This script is provided without warrenty and so on and so forth.
host = dict()
persona = dict()


def connect():
        try:
                array.connect(hostname,username=arr_username,password=arr_password)
        except (paramiko.SSHException, socket.gaierror) as sshfail:
                print sshfail
                sys.exit(-1)

def get_hosts():
	global host, persona 

	i,o,e = array.exec_command('showhost -d')
	o.readline()

	for line in o.readlines():		
		split = string.split(line)
		if(split[0] == "--"):
			break		

		if(host.has_key(split[1])):
			wwns = host[split[1]]
		else:
			wwns = []

		persona[split[1]] = split[2]
		wwns.append(split[3])

		host[split[1]] = wwns

def create_hosts():

	file = open('creat_hosts_3par.cmds','w')

	for hosts in host.iterkeys():
#		print hosts
#		print host[hosts]
#		print persona[hosts] + "\n"

		create_host = "createhost -persona "
		if( persona[hosts] == "Generic-legacy"):
			create_host = create_host + "6 "
		elif ( persona[hosts] == "ONTAP-legacy"):
			create_host = create_host + "10 "

		create_host = create_host + hosts

		for wwn in host[hosts]:
			create_host = create_host + " " + wwn

		print create_host
		file.write(create_host + "\n")

if __name__ == "__main__":
	connect()
	get_hosts()
	create_hosts()
	array.close()
