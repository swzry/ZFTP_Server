#!/usr/bin/ python
# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import ConfigParser
from threading import Thread as thread
from pyftpdlib import ftpserver
from daemonlib import Daemon
now = lambda: time.strftime("[%Y-%b-%d %H:%M:%S]")

def standard_logger(msg):
    f1.write("%s %s\n" %(now(), msg))
    f1.flush()

def line_logger(msg):
    f2.write("%s %s\n" %(now(), msg))
    f2.flush()

class UpConf(thread):
    def run(self):
        while 1:
            time.sleep(ttl)
            user=[]
            __user_table = {}
            conf=ConfigParser.ConfigParser()
            conf.read(currdir+currname+".conf")
            sections=conf.sections()
            for i in sections:
                if i != '!ftpd':
                    if not os.path.isdir(conf.get(i,'dir')):
                        continue
                    else:
                        user.append(i)
            for i in user:
                __dir=conf.get(i,'dir')
                __password=conf.get(i,'password')
                __power=conf.get(i,'access')
                __dir = os.path.realpath(__dir)
                authorizer._check_permissions(i, __power)
                dic = {'pwd': str(__password),
                       'home': __dir,
                       'perm': __power,
                       'operms': {},
                       'msg_login': str("Login successful."),
                       'msg_quit': str("Goodbye.")
                       }
                __user_table[i] = dic
            authorizer.user_table=__user_table
def mainfunc():
    global authorizer
    global ttl
    user=[]
    __user_table = {}
    addr=("",21)
    ttl=60
    ftpserver.log = standard_logger
    ftpserver.logline = line_logger
    authorizer = ftpserver.DummyAuthorizer()
    conf=ConfigParser.ConfigParser()
    conf.read(currdir+currname+".conf")
    sections=conf.sections()
    global f1,f2
    for i in sections:
        if i != '!ftpd':
	    if not os.path.isdir(conf.get(i,'dir')):
                print('No such directory: "%s"' % conf.get(i,'dir'))
                continue
            else:
                user.append(i)
        if i == '!ftpd':
            addr=(conf.get('!ftpd','host'),int(conf.get('!ftpd','port')))
            ttl=int(conf.get('!ftpd','ttl'))
            _servername=conf.get('!ftpd','servername')
	    sys.stdout.write("Server Name: %s\n"%_servername)
	    sys.stdout.flush()
            _maxcon=int(conf.get('!ftpd','maxconnect'))
            _maxconperu=int(conf.get('!ftpd','maxconperuser'))
            f1 = open(conf.get('!ftpd','logfile'), 'a')
            f2 = open(conf.get('!ftpd','lineslogfile'), 'a')
            if ttl==0:ttl=60
    for i in user:
        __dir=conf.get(i,'dir')
        __password=conf.get(i,'password')
        __power=conf.get(i,'access')
        __dir = os.path.realpath(__dir)
        authorizer._check_permissions(i, __power)
        dic = {'pwd': str(__password),
               'home': __dir,
               'perm': __power,
               'operms': {},
               'msg_login': str("Login successful."),
               'msg_quit': str("Goodbye.")
               }
        __user_table[i] = dic
    authorizer.user_table=__user_table
    ftp_handler = ftpserver.FTPHandler
    ftp_handler.authorizer = authorizer
    ftp_handler.banner = _servername
    ftpd = ftpserver.FTPServer(addr, ftp_handler)
    ftpd.max_cons = _maxcon
    ftpd.max_cons_per_ip = _maxconperu
    UpConf().start()
    line_logger('~~~~~~~~~Serve forever......')
    ftpd.serve_forever()

class MyDaemon(Daemon):
    def _run(self):
        #while True:
            reload(sys)
            sys.setdefaultencoding('utf-8')
	    #mainfunc()
            try:
            	mainfunc()
            except Exception,e:
                time.sleep(1)
		s=traceback.format_exc()
                sys.stderr.write("\n"+now()+"Application was shutdown by a fatal error.\n%s\n"%s)
		sys.stderr.flush()
            sys.stdout.write("A Server Session End. Restart a new session...\n")
            sys.stdout.flush()

if __name__ == '__main__':
    global currdir,currname
    currdir='/home/ftpd/'
    currname='zftpd'
    daemon = MyDaemon('/dev/shm/'+currname+'.pid',currdir+currname+'.in',currdir+currname+'.out',currdir+currname+'.err')
    print "ZFTP Server Init!"
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print "Starting...                                            [\033[1;32;40mOK\033[0m]"
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            print "Stopping...                                            [\033[1;32;40mOK\033[0m]"
        elif 'restart' == sys.argv[1]:
            print "Stopping...                                            [\033[1;32;40mOK\033[0m]"
            print "Starting...                                            [\033[1;32;40mOK\033[0m]"
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
