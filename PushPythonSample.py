#!usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'leiyuan'  
__mail__ = 'leiyuan@iflytek.com'  
__date__ = '2016-09-27'  
__version__ = 1001

import sys
import time
from socket import *
import hashlib
import urllib
import os
import getopt
import urllib2
import datetime
import logging
import ConfigParser
import socket as Socket
import json


reload(sys)
sys.setdefaultencoding('utf8')


#ȫ�ֱ���
Global_runTime = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
Global_localIp = Socket.gethostbyname(Socket.getfqdn(Socket.gethostname()))

###��־������
class Log(object):
    
    #���캯������ʼ��������Ϣ
    def __init__(self,Um):
        self.logPath = Um.logDir
        asctime = Global_runTime
        self.logName = self.logPath + "/" + asctime + "_" +Global_localIp +  "_log"  + ".log"
        #self.logName = self.logPath + "/" + asctime + "_" + "_log"  + ".log"
        
        logging.basicConfig(level=logging.DEBUG,\
                            format='%(asctime)s %(filename)s %(levelname)s %(message)s',\
                            datefmt='%Y-%m-%d %H:%M:%S',\
                            filename=self.logName,\
                            filemode='w')
        
        #����һ��StreamHandler����INFO�������ߵ���־��Ϣ��ӡ����׼���󣬲�������ӵ���ǰ����־�������
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)            
              
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #д��־���ֲ�ͬ��־�����¼��־
    def write_log(self,logType,content):
        if logType == 1:
            logging.info(content)
        elif logType == 2:
            logging.error(content)
        elif logType == 3:
            logging.debug(content)
        else:
            logging.info(content)

            
###ͨ�÷�����
class UniversalMethod(object):
    
    #���캯������ʼ��������Ϣ
    def __init__(self):
        
        '''
         logDir #��־���ɴ�ŵ�·��
        '''
        
        self.logDir = './log'
        
        self.createLogDir(self.logDir)
            
    #������־Ŀ¼���Զ�������־Ŀ¼
    def createLogDir(self,new_path):
        if new_path.strip()!='':
            if not os.path.isdir(new_path):
                os.makedirs(new_path)
                self.debug_print('������־Ŀ¼ %s' %(new_path))
            else:
                self.debug_print('�Ѿ�������־Ŀ¼ %s' %(new_path))
        else:
            self.deal_error('������־��Ŀ¼����Ϊ�գ������˳�')
            sys.exit()
            
    #д��������¼���
    def writeResult(self,new_file,resultList):
        resultLine = ""
        if os.path.exists(new_file)==False:
                for result in resultList:
                        if resultLine == "":
                                resultLine = resultLine+result
                        else:
                                resultLine = resultLine+"\n"+result
                fw = open(new_file,"w")
                fw.write("%s\n"%resultLine)
                fw.close()
        
        fwExist = open(new_file,"w+")
        for result in resultList:
                if resultLine=="":
                        resultLine = resultLine+result
                else:
                        resultLine = resultLine+"\n"+result
        fwExist.write("%s\n"%resultLine)
        fwExist.close()
                
     
        
    #��ӡ��Ϣ����ӡ����������Ϣ
    def debug_print(self, logstr):
        timenow  = time.localtime()
        datenow  = time.strftime('%Y-%m-%d', timenow)
        logstr += " - %s ִ�в���\n" %datenow
        print (logstr)
    
    #��ӡ��Ϣ����ӡ����������Ϣ    
    def deal_error(self, e):
        logstr = '%s ��������: %s' %(datenow, e)
        self.debug_print(logstr)
        ###file.write(logstr)
        #sys.exit()


###�����в���and��ȡ�����ļ���
class CLI(object):
    
        #���캯������ʼ��������Ϣ
        def __init__ (self,conf):
                self.push_num = 'default'
                self.msg_size = 'default'
                self.appid= 'default'
                self.api_key = 'default'
                self.did = "default"
                self.expires = "default"
                self.click_action = "default"
                
                
                self.push_type = "default"
                self.msg_type = "default"
                self.dvc_type = "default"
                
                self.conf = conf
                
                self.read_config_param(conf)
                self.getParm()
                
        #��ȡ�����ļ�����ȡ�����ļ����õĲ���
        def read_config_param(self,conf):
                try:
                        self.push_num = conf.get('common', 'push_num')
                        if self.push_num == '':
                                self.push_num == 'default'
                except:
                        self.push_num = 'default'
                
                try:
                        self.msg_size = conf.get('common', 'msg_size')
                        if self.msg_size == '':
                                self.msg_size == 'default'
                except:
                        self.msg_size = 'default'
                
                try:
                        self.appid = conf.get('common', 'appid')
                        if self.appid == '':
                                self.appid == 'default'
                except:
                        self.appid = 'default'
                
                try:
                        self.api_key = conf.get('common', 'api_key')
                        if self.api_key == '':
                                self.api_key == 'default'
                except:
                        self.api_key = 'default'
                
                try:
                        self.did = conf.get('common', 'did')
                        if self.did == '':
                                self.did == 'default'
                except:
                        self.did = 'default'
                        
                try:
                        self.click_action = conf.get('common', 'click_action')
                        if self.click_action == '':
                                self.click_action == 'default'
                except:
                        self.click_action = 'default'
                
                try:
                        self.expires = conf.get('common', 'expires')
                        if self.expires == '':
                                self.expires == 'default'
                except:
                        self.expires = 'default'
                        
                try:
                        self.push_type = conf.get('choose', 'push_type')
                        if self.push_type == '':
                                self.push_type == 'default'
                except:
                        self.push_type = 'default'
                
                try:
                        self.msg_type = conf.get('choose', 'msg_type')
                        if self.msg_type == '':
                                self.msg_type == 'default'
                except:
                        self.msg_type = 'default'
                
                try:
                        self.dvc_type = conf.get('choose', 'dvc_type')
                        if self.dvc_type == '':
                                self.dvc_type == 'default'
                except:
                        self.dvc_type = 'default'
                
                
        #��ȡ�����У���ȡ�����в���
        def getParm(self):
                opts, args = getopt.getopt(sys.argv[1:], "hv:",["help=","version=","pn=","ms=","appid=","ak=","did=","expires=","ca=","pt=","mt=","dt="])
                for op, value in opts:
                        if op == "--pn":
                                self.push_num = value
                        elif op == "--ms":
                                self.msg_size = value
                        elif op == "--appid":
                                self.appid = value
                        elif op == "--ak":
                                self.api_key = value
                        elif op == "--did":
                                self.did = value
                        elif op == "--expires":
                                self.expires = value
                        elif op == "--ca":
                                self.click_action = value
                        elif op == "--pt":
                                self.push_type = value
                        elif op == "--mt":
                                self.msg_type = value
                        elif op == "--dt":
                                self.dvc_type = value
                        elif op in ("-h","--help"):
                            self.usage()
                        elif op in ("-v","--version"):
                            self.version()
                return True
            
            
        #��ʾ����ʾʹ�÷���
        def usage(self):
                print "ѡ��\t����\tĬ��ֵ"
                print "-h or --help\t����\tֻ��ʾ�����в������壬��ִ�нű����˳�"
                print "-v or --version\t��python���������汾�ţ���ִ�нű����˳�"
                print "--pn\t���͵Ĵ���\tdefault"
                print "--ms\t������Ϣ�Ĵ�С\tdefault"
                print "--appid\tApp ID\tdefault"
                print "--ak\tApi Key\tdefault"
                print "--did\tDid\tdefault"
                print "--expires\tExpires\tdefault"
                print "--ca\tClick Action\tdefault"
                print "--pt\t���͵�����\tdefault"
                print "--mt\t��Ϣ������\tdefault"
                print "--dt\t�豸������\tdefault"
                sys.exit(0)
        
        #�汾�ţ���ʾ��python���������汾��        
        def version(self):
            print 'PushPythonSample.py 1.0.0.1'
            sys.exit(0)

###�����װ��
class RequestPackage(object):
    
    #���캯������ʼ��������Ϣ
    def __init__(self, conf, Um, Lg):
        self.conf = conf
        self.Um = Um
        self.Lg = Lg
        
        self.cli = CLI(self.conf)
        
        self.server_addr = "xpush.voicecloud.cn"
        self.msg = ""  #���͵���Ϣ
        self.push_msg = ""  #ʵ�ʷ��͵�body��Ϣ
        
        self.dids = ""  #list����ʱ��Ⱥ��did
        
        self.ret = 0  #��Ӧ��Ϣ���صĴ�����
        self.req_id = ""  #��Ӧ��Ϣ���ص�sid
        
        self.push_num = self.cli.push_num  #���ʹ���
        self.Um.debug_print('The number of this push is '+'['+self.push_num+']')
        self.Lg.write_log(1, 'The number of this push is '+'['+self.push_num+']')
        
        self.msg_size = self.cli.msg_size  #������Ϣ�Ĵ�С
        self.Um.debug_print('The size of the push message is '+'['+self.msg_size+']')
        self.Lg.write_log(1, 'The size of the push message is '+'['+self.msg_size+']')
        
        self.appid = self.cli.appid  #App ID
        self.Um.debug_print('The appid of this push is '+'['+self.appid+']')
        self.Lg.write_log(1, 'The appid of this push is '+'['+self.appid+']')
        
        self.api_key = self.cli.api_key  #Api Key
        self.Um.debug_print('The api key of this push is '+'['+self.api_key+']')
        self.Lg.write_log(1, 'The api key of this push is '+'['+self.api_key+']')
        
        self.did = self.cli.did  #Did
        self.Um.debug_print('The did of this push is '+'['+self.did+']')
        self.Lg.write_log(1, 'The did of this push is '+'['+self.did+']')
        
        self.expires = self.cli.expires  #����ʱ��
        self.Um.debug_print('The expiration time of this push is '+'['+self.expires+']')
        self.Lg.write_log(1, 'The expiration time of this push is '+'['+self.expires+']')
        
        self.click_action = self.cli.click_action
        self.Um.debug_print('The click action of this push is '+'['+self.click_action+']')
        self.Lg.write_log(1, 'The click action of this push is '+'['+self.click_action+']')
        
        self.push_type = self.cli.push_type  #��������
        self.Um.debug_print('The push type of this push is '+'['+self.push_type+']')
        self.Lg.write_log(1, 'The push type of this push is '+'['+self.push_type+']')
        
        self.msg_type = self.cli.msg_type  #��Ϣ����
        self.Um.debug_print('The message type of this push is '+'['+self.msg_type+']')
        self.Lg.write_log(1, 'The message type of this push is '+'['+self.msg_type+']')
        
        self.dvc_type = self.cli.dvc_type  #�豸����
        self.Um.debug_print('The device type of this push is '+'['+self.dvc_type+']')
        self.Lg.write_log(1, 'The device type of this push is '+'['+self.dvc_type+']')
        
        self.connection = self.EstablishConnection()
        
        
        
        
    #��������: ������������ͨ��
    def EstablishConnection(self):
        try:
            c = socket(AF_INET, SOCK_STREAM)
            c.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            c.connect((self.server_addr, 80))
            self.Um.debug_print('The connection channel has now been established!')
            self.Lg.write_log(1, 'The connection channel has now been established!')
            
            return c
        except Exception, ex:
            self.Um.deal_error('Sorry. Failed to establish connection channel!')
            self.Lg.write_log(2, 'Sorry. Failed to establish connection channel!')
            print "connect exception:", ex
        
        
    #��ȡsign��md5��ȡsignֵ
    def GetSign(self, api_key, paramdict, server_addr):
        
        keys = paramdict.keys()
        keys.sort()
        sign_str = "POST%s/rest/2.0/push.do" %(server_addr)
        for key in keys:
            sign_str = sign_str + key
            sign_str = sign_str + "="
            sign_str = sign_str + str(paramdict[key])
  
        sign_str = sign_str + api_key
        #print "sign_str:%s" %(sign_str)
        self.Um.debug_print('The sign string is '+'['+sign_str+']')
        self.Lg.write_log(1, 'The sign string is '+'['+sign_str+']')
        
        m = hashlib.md5()
        m.update(sign_str)
        sign = m.hexdigest()
        #print "sign:%s" %(sign)
        self.Um.debug_print('The sign key is '+'['+sign+']')
        self.Lg.write_log(1, 'The sign key is '+'['+sign+']')
        
        return sign
        
    
    
    #�������󣺷�����������
    def InitiateRequest(self, server_addr, push_msg):
        
        http_msg = "POST /rest/2.0/push.do HTTP/1.1\r\nHost: %s\r\nContent-Length: %d\r\n\r\n%s" %(server_addr, len(push_msg), push_msg)
        #print "http_msg:%s" %(http_msg)
        
        self.Um.debug_print('Now initiate the push request!')
        self.Lg.write_log(1, 'Now initiate the push request!')
        self.connection.send(http_msg)
    
    
    #��������(�ڶ��ַ���)��������������
    def InitiateRequest2(self, server_addr, push_msg):
        url = "http://" + server_addr + "/rest/2.0/push.do"
        req = urllib2.Request(url,push_msg)
        try:
            response = urllib2.urlopen(req)
            print ("Launch the push request!")
            self.Lg.write_log(1, 'Launch the push request!')
        except Exception, ex:
            print "url open exception:", ex
        
        return response
    
        
    #�������̣��ӽ������ӵ������������󣬵��������ͽ��
    def SinglePush(self):
        ##��ȡ���Ӷ���
        #�����캯������ʼ��ʱ�ѽ�������
        
        
        '''
        ���췢��body
        '''
        ##�������͵�body��Ϣ
        for i in range(0, int(self.msg_size)):
            self.msg += "m"
            
        for i in range(0, int(self.push_num)):
            #print "��%s����������ʼ:\n" %str(i)
            self.Um.debug_print('��%s����������ʼ:' %str(i))
            self.Lg.write_log(1, '��%s����������ʼ:' %str(i))
            
            real_msg = '{ "title": "test Xpush", "content": "%s", "builder_id": 0 }' %(self.msg)
            self.Um.debug_print('The real message of the push is '+'['+real_msg+']')
            self.Lg.write_log(1, 'The real message of the push is '+'['+real_msg+']')
            
            params = dict()
            params["appid"] = self.appid
            params["push_type"] = int(self.push_type)
            params["msg_type"] = int(self.msg_type)
            params["click_action"] = int(self.click_action)
            params["message"] = real_msg
            params["timestamp"] = int(time.time())
            params["expires"] = int(self.expires)
            params["did"] = self.did
            params["dvc_type"] = int(self.dvc_type)
            
            ##��ȡsign
            sign = self.GetSign(self.api_key, params, self.server_addr)
            params ["sign"] = sign
            #print params
            
            ##��body�������б���
            try:
                self.push_msg = urllib.urlencode(params)
            except Exception, ex:
                self.Um.deal_error('Sorry. Failed to encode body params!')
                self.Lg.write_log(2, 'Sorry. Failed to encode body params!')
                print "urlencode exception:", ex
            
            self.Um.debug_print("The body of the push request is ["+str(params)+']')
            self.Lg.write_log(1, "The body of the push request is ["+str(params)+']')
            
            '''
            ������������
            '''
            ##����single����http post����
            self.InitiateRequest(self.server_addr, self.push_msg)
            time.sleep(2)
            #print "\n��%s�������������.\n" %str(i)
            self.Um.debug_print('��%s�������������.' %str(i))
            self.Lg.write_log(1, '��%s�������������.' %str(i))
            
        print ("All push send requests completed!")
        self.Lg.write_log(1, '###All push send requests completed!###')
            
        '''
        ��������������Ӧ��Ϣ
        '''
        for i in range(0, int(self.push_num)):
            time.sleep(1)
            buf = self.connection.recv(102400)  #���ý��ջ�������С
            time.sleep(1)
            if len(buf) > 0:
                #print "receive push response message:",buf
                strdata = buf.split("\r\n\r\n")[1]
                ddata = eval(strdata)
                self.ret = ddata['ret']
                self.Um.debug_print('This push request ret is:[%s]' %str(self.ret))
                if self.ret == 0:
                    self.Lg.write_log(1, 'This push request ret is:[%s]' %str(self.ret))
                else:
                    self.Lg.write_log(2, 'The push request error!')
                    self.Lg.write_log(2, 'This push request ret is:[%s]' %str(self.ret))
                self.req_id = ddata["req_id"]
                self.Um.debug_print('This push request req_id is:[%s]' %str(self.req_id))
                self.Lg.write_log(1, 'This push request req_id is:[%s]' %str(self.req_id))
            else:
                print "do not receive push response message"
        self.connection.close()
        
        print ("All push receive requests completed!")
        self.Lg.write_log(1, '###All push receive requests completed!###')
        print "All operations completed!"
        self.Lg.write_log(1, '###All operations completed!###')
     
        
    
    #��������(�ڶ��ַ���)���ӽ������ӵ������������󣬵��������ͽ��
    def SinglePush2(self):
        ##��ȡ���Ӷ���
        #�����캯������ʼ��ʱ�ѽ�������
        
        
        '''
        ���췢��body
        '''
        ##�������͵�body��Ϣ
        for i in range(0, int(self.msg_size)):
            self.msg += "m"
            
        for i in range(0, int(self.push_num)):
            #print "��%s����������ʼ:\n" %str(i)
            self.Um.debug_print('��%s����������ʼ:' %str(i))
            self.Lg.write_log(1, '��%s����������ʼ:' %str(i))
            
            real_msg = '{ "title": "test Xpush", "content": "%s", "builder_id": 0 }' %(self.msg)
            self.Um.debug_print('The real message of the push is '+'['+real_msg+']')
            self.Lg.write_log(1, 'The real message of the push is '+'['+real_msg+']')
            
            params = dict()
            params["appid"] = self.appid
            params["push_type"] = int(self.push_type)
            params["msg_type"] = int(self.msg_type)
            params["click_action"] = int(self.click_action)
            params["message"] = real_msg
            params["timestamp"] = int(time.time())
            params["expires"] = int(self.expires)
            params["did"] = self.did
            params["dvc_type"] = int(self.dvc_type)
            
            ##��ȡsign
            sign = self.GetSign(self.api_key, params, self.server_addr)
            params ["sign"] = sign
            #print params
            
            ##��body�������б���
            try:
                self.push_msg = urllib.urlencode(params)
            except Exception, ex:
                self.Um.deal_error('Sorry. Failed to encode body params!')
                self.Lg.write_log(2, 'Sorry. Failed to encode body params!')
                print "urlencode exception:", ex
            
            self.Um.debug_print("The body of the push request is ["+str(params)+']')
            self.Lg.write_log(1, "The body of the push request is ["+str(params)+']')
            
            '''
            ������������,������Ӧ��Ϣ
            '''
            ##����single����http post����,��������Ӧ��Ϣ
            try:
                response = self.InitiateRequest2(self.server_addr, self.push_msg)
                thejsonreturn = response.read()
                print ("Parse the push request response message!")
                self.Lg.write_log(1, 'Parse the push request response message!')
                ddata = json.loads(thejsonreturn)
               
                self.ret = ddata['ret']
                self.Um.debug_print('This push request ret is:[%s]' %str(self.ret))
                if self.ret == 0:
                    self.Lg.write_log(1, 'This push request ret is:[%s]' %str(self.ret))
                else:
                    self.Lg.write_log(2, 'The push request error!')
                    self.Lg.write_log(2, 'This push request ret is:[%s]' %str(self.ret))
                self.req_id = ddata["req_id"]
                self.Um.debug_print('This push request req_id is:[%s]' %str(self.req_id))
                self.Lg.write_log(1, 'This push request req_id is:[%s]' %str(self.req_id))
            except Exception, ex:
                print "analysis response exception:", ex
           
            time.sleep(2) 
            #print "\n��%s�������������.\n" %str(i)
            self.Um.debug_print('��%s�������������.' %str(i))
            self.Lg.write_log(1, '��%s�������������.' %str(i))
            
        print "All operations completed!"
        self.Lg.write_log(1, '###All operations completed!###')
        
    
    
    #list�����̣��ӽ������ӵ������������󣬵��������ͽ��
    def ListPush(self):
        ##��ȡ���Ӷ���
        #�����캯������ʼ��ʱ�ѽ�������
        
        
        '''
        ���췢��body
        '''
        ##�������͵�body��Ϣ
        for i in range(0, int(self.msg_size)):
            self.msg += "m"
            
        didsList = self.did.split(",")
        for i in didsList:
            self.dids += str(i) + "\r\n"
        
        self.Um.debug_print('The dids of List Push is['+self.did+']')
        self.Lg.write_log(1, 'The dids of List Push is['+self.did+']')
        for i in range(0, int(self.push_num)):
            #print "��%s����������ʼ:\n" %str(i)
            self.Um.debug_print('��%s����������ʼ:' %str(i))
            self.Lg.write_log(1, '��%s����������ʼ:' %str(i))
            
            real_msg = '{ "title": "test Xpush", "content": "%s", "builder_id": 0 }' %(self.msg)
            self.Um.debug_print('The real message of the push is '+'['+real_msg+']')
            self.Lg.write_log(1, 'The real message of the push is '+'['+real_msg+']')
            
            params = dict()
            params["appid"] = self.appid
            params["push_type"] = int(self.push_type)
            params["dvc_type"] = int(self.dvc_type)
            params["msg_type"] = int(self.msg_type)
            params["message"] = real_msg
            params["timestamp"] = int(time.time())
            params["expires"] = int(self.expires)
            params["click_action"] = int(self.click_action)
            params["did"] = self.dids
            
            ##��ȡsign
            sign = self.GetSign(self.api_key, params, self.server_addr)
            params ["sign"] = sign
            #print params
            
            ##��body�������б���
            try:
                self.push_msg = urllib.urlencode(params)
            except Exception, ex:
                self.Um.deal_error('Sorry. Failed to encode body params!')
                self.Lg.write_log(2, 'Sorry. Failed to encode body params!')
                print "urlencode exception:", ex
                
            self.Um.debug_print("The body of the push request is ["+str(params)+']')
            self.Lg.write_log(1, "The body of the push request is ["+str(params)+']')    
            
            '''
            ������������
            '''
            ##����list����http post����
            self.InitiateRequest(self.server_addr, self.push_msg)
            time.sleep(2)
            #print "\n��%s�������������.\n" %str(i)
            self.Um.debug_print('��%s�������������.' %str(i))
            self.Lg.write_log(1, '��%s�������������.' %str(i))
            
        print ("All push send requests completed!")
        self.Lg.write_log(1, '###All push send requests completed!###')
        '''
        ��������������Ӧ��Ϣ
        '''
        time.sleep(1)
        buf = self.connection.recv(10240)  #���ý��ջ�������С
        if len(buf) > 0:
            #print "receive push response message:",buf
            strdata = buf.split("\r\n\r\n")[1]
            ddata = eval(strdata)
            self.ret = ddata['ret']
            self.Um.debug_print('This push request ret is:[%s]' %str(self.ret))
            if self.ret == 0:
                self.Lg.write_log(1, 'This push request ret is:[%s]' %str(self.ret))
            else:
                self.Lg.write_log(2, 'The push request error!')
                self.Lg.write_log(2, 'This push request ret is:[%s]' %str(self.ret))
            self.req_id = ddata["req_id"]
            self.Um.debug_print('This push request req_id is:[%s]' %str(self.req_id))
            self.Lg.write_log(1, 'This push request req_id is:[%s]' %str(self.req_id))
        else:
            print "do not receive push response message"
        self.connection.close()
        
        print ("All push receive requests completed!")
        self.Lg.write_log(1, '###All push receive requests completed!###')
        print "All operations completed!"
        self.Lg.write_log(1, '###All operations completed!###')
    
    
    
    #list������(�ڶ��ַ���)���ӽ������ӵ������������󣬵��������ͽ��
    def ListPush2(self):
        ##��ȡ���Ӷ���
        #�����캯������ʼ��ʱ�ѽ�������
        
        
        '''
        ���췢��body
        '''
        ##�������͵�body��Ϣ
        for i in range(0, int(self.msg_size)):
            self.msg += "m"
            
        didsList = self.did.split(",")
        for i in didsList:
            self.dids += str(i) + "\r\n"
        
        self.Um.debug_print('The dids of List Push is['+self.did+']')
        self.Lg.write_log(1, 'The dids of List Push is['+self.did+']')
        for i in range(0, int(self.push_num)):
            #print "��%s����������ʼ:\n" %str(i)
            self.Um.debug_print('��%s����������ʼ:' %str(i))
            self.Lg.write_log(1, '��%s����������ʼ:' %str(i))
            
            real_msg = '{ "title": "test Xpush", "content": "%s", "builder_id": 0 }' %(self.msg)
            self.Um.debug_print('The real message of the push is '+'['+real_msg+']')
            self.Lg.write_log(1, 'The real message of the push is '+'['+real_msg+']')
            
            params = dict()
            params["appid"] = self.appid
            params["push_type"] = int(self.push_type)
            params["dvc_type"] = int(self.dvc_type)
            params["msg_type"] = int(self.msg_type)
            params["message"] = real_msg
            params["timestamp"] = int(time.time())
            params["expires"] = int(self.expires)
            params["click_action"] = int(self.click_action)
            params["did"] = self.dids
            
            ##��ȡsign
            sign = self.GetSign(self.api_key, params, self.server_addr)
            params ["sign"] = sign
            #print params
            
            ##��body�������б���
            try:
                self.push_msg = urllib.urlencode(params)
            except Exception, ex:
                self.Um.deal_error('Sorry. Failed to encode body params!')
                self.Lg.write_log(2, 'Sorry. Failed to encode body params!')
                print "urlencode exception:", ex
                
            self.Um.debug_print("The body of the push request is ["+str(params)+']')
            self.Lg.write_log(1, "The body of the push request is ["+str(params)+']')    
            
            '''
            ������������,������Ӧ��Ϣ
            '''
            ##����list����http post����,��������Ӧ��Ϣ
            try:
                response = self.InitiateRequest2(self.server_addr, self.push_msg)
                thejsonreturn = response.read()
                print ("Parse the push request response message!")
                self.Lg.write_log(1, 'Parse the push request response message!')
                ddata = json.loads(thejsonreturn)
               
                self.ret = ddata['ret']
                self.Um.debug_print('This push request ret is:[%s]' %str(self.ret))
                if self.ret == 0:
                    self.Lg.write_log(1, 'This push request ret is:[%s]' %str(self.ret))
                else:
                    self.Lg.write_log(2, 'The push request error!')
                    self.Lg.write_log(2, 'This push request ret is:[%s]' %str(self.ret))
                self.req_id = ddata["req_id"]
                self.Um.debug_print('This push request req_id is:[%s]' %str(self.req_id))
                self.Lg.write_log(1, 'This push request req_id is:[%s]' %str(self.req_id))
            except Exception, ex:
                print "analysis response exception:", ex
                
            time.sleep(2)
            #print "\n��%s�������������.\n" %str(i)
            self.Um.debug_print('��%s�������������.' %str(i))
            self.Lg.write_log(1, '��%s�������������.' %str(i))
            
        print "All operations completed!"
        self.Lg.write_log(1, '###All operations completed!###')
        
            
        
    #App�����̣��ӽ������ӵ������������󣬵��������ͽ��
    def AppPush(self):
        ##��ȡ���Ӷ���
        #�����캯������ʼ��ʱ�ѽ�������

        
        '''
        ���췢��body
        '''
        ##�������͵�body��Ϣ
        for i in range(0, int(self.msg_size)):
            self.msg += "m"
            
        for i in range(0, int(self.push_num)):
            #print "��%s����������ʼ:\n" %str(i)
            self.Um.debug_print('��%s����������ʼ:' %str(i))
            self.Lg.write_log(1, '��%s����������ʼ:' %str(i))
            
            real_msg = '{ "title": "test Xpush", "content": "%s", "builder_id": 0 }' %(self.msg)
            self.Um.debug_print('The real message of the push is '+'['+real_msg+']')
            self.Lg.write_log(1, 'The real message of the push is '+'['+real_msg+']')
            
            params = dict()
            params["appid"] = self.appid
            params["push_type"] = int(self.push_type)
            params["msg_type"] = int(self.msg_type)
            params["dvc_type"] = int(self.dvc_type)
            params["click_action"] = int(self.click_action)
            params["message"] = real_msg
            params["timestamp"] = int(time.time())
            params["expires"] = int(self.expires)
                
            ##��ȡsign
            sign = self.GetSign(self.api_key, params, self.server_addr)
            params ["sign"] = sign
            #print params

            ##��body�������б���
            try:
                self.push_msg = urllib.urlencode(params)
            except Exception, ex:
                self.Um.deal_error('Sorry. Failed to encode body params!')
                self.Lg.write_log(2, 'Sorry. Failed to encode body params!')
                print "urlencode exception:", ex
            
            self.Um.debug_print("The body of the push request is ["+str(params)+']')
            self.Lg.write_log(1, "The body of the push request is ["+str(params)+']')    
            
                
            '''
            ������������
            '''
            ##����App����http post����
            self.InitiateRequest(self.server_addr, self.push_msg)
            time.sleep(2)
            #print "\n��%s�������������.\n" %str(i)
            self.Um.debug_print('��%s�������������.' %str(i))
            self.Lg.write_log(1, '��%s�������������.' %str(i))
            
                
        print ("All push send requests completed!")
        self.Lg.write_log(1, '###All push send requests completed!###')
            
        '''
        ��������������Ӧ��Ϣ
        '''
        time.sleep(1)
        buf = self.connection.recv(10240)  #���ý��ջ�������С
        if len(buf) > 0:
            #print "receive push response message:",buf
            strdata = buf.split("\r\n\r\n")[1]
            ddata = eval(strdata)
            self.ret = ddata['ret']
            self.Um.debug_print('This push request ret is:[%s]' %str(self.ret))
            if self.ret == 0:
                self.Lg.write_log(1, 'This push request ret is:[%s]' %str(self.ret))
            else:
                self.Lg.write_log(2, 'The push request error!')
                self.Lg.write_log(2, 'This push request ret is:[%s]' %str(self.ret))
            self.req_id = ddata["req_id"]
            self.Um.debug_print('This push request req_id is:[%s]' %str(self.req_id))
            self.Lg.write_log(1, 'This push request req_id is:[%s]' %str(self.req_id))
        else:
            print "do not receive push response message"
        self.connection.close()
        
        print ("All push receive requests completed!")
        self.Lg.write_log(1, '###All push receive requests completed!###')
        print "All operations completed!"
        self.Lg.write_log(1, '###All operations completed!###')
    
    
    #App������(�ڶ��ַ���)���ӽ������ӵ������������󣬵��������ͽ��
    def AppPush2(self):
        ##��ȡ���Ӷ���
        #�����캯������ʼ��ʱ�ѽ�������

        
        '''
        ���췢��body
        '''
        ##�������͵�body��Ϣ
        for i in range(0, int(self.msg_size)):
            self.msg += "m"
            
        for i in range(0, int(self.push_num)):
            #print "��%s����������ʼ:\n" %str(i)
            self.Um.debug_print('��%s����������ʼ:' %str(i))
            self.Lg.write_log(1, '��%s����������ʼ:' %str(i))
            
            real_msg = '{ "title": "test Xpush", "content": "%s", "builder_id": 0 }' %(self.msg)
            self.Um.debug_print('The real message of the push is '+'['+real_msg+']')
            self.Lg.write_log(1, 'The real message of the push is '+'['+real_msg+']')
            
            params = dict()
            params["appid"] = self.appid
            params["push_type"] = int(self.push_type)
            params["msg_type"] = int(self.msg_type)
            params["dvc_type"] = int(self.dvc_type)
            params["click_action"] = int(self.click_action)
            params["message"] = real_msg
            params["timestamp"] = int(time.time())
            params["expires"] = int(self.expires)
                
            ##��ȡsign
            sign = self.GetSign(self.api_key, params, self.server_addr)
            params ["sign"] = sign
            #print params

            ##��body�������б���
            try:
                self.push_msg = urllib.urlencode(params)
            except Exception, ex:
                self.Um.deal_error('Sorry. Failed to encode body params!')
                self.Lg.write_log(2, 'Sorry. Failed to encode body params!')
                print "urlencode exception:", ex
            
            self.Um.debug_print("The body of the push request is ["+str(params)+']')
            self.Lg.write_log(1, "The body of the push request is ["+str(params)+']')    
            
            '''
            ������������,������Ӧ��Ϣ
            '''
            ##����app����http post����,��������Ӧ��Ϣ
            try:
                response = self.InitiateRequest2(self.server_addr, self.push_msg)
                thejsonreturn = response.read()
                print ("Parse the push request response message!")
                self.Lg.write_log(1, 'Parse the push request response message!')
                ddata = json.loads(thejsonreturn)
               
                self.ret = ddata['ret']
                self.Um.debug_print('This push request ret is:[%s]' %str(self.ret))
                if self.ret == 0:
                    self.Lg.write_log(1, 'This push request ret is:[%s]' %str(self.ret))
                else:
                    self.Lg.write_log(2, 'The push request error!')
                    self.Lg.write_log(2, 'This push request ret is:[%s]' %str(self.ret))
                self.req_id = ddata["req_id"]
                self.Um.debug_print('This push request req_id is:[%s]' %str(self.req_id))
                self.Lg.write_log(1, 'This push request req_id is:[%s]' %str(self.req_id))
            except Exception, ex:
                print "analysis response exception:", ex
            
            time.sleep(2)
            #print "\n��%s�������������.\n" %str(i)
            self.Um.debug_print('��%s�������������.' %str(i))
            self.Lg.write_log(1, '��%s�������������.' %str(i))
            
        print "All operations completed!"
        self.Lg.write_log(1, '###All operations completed!###')

if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read('xpush.cfg')
    Um = UniversalMethod()
    Lg = Log(Um)
    
    request = RequestPackage(conf,Um,Lg)
    
    ##��һ�ַ���
    '''
    if int(request.push_type) == 0:
        print "You choose [Single Push]"
        request.SinglePush()
    elif int(request.push_type) == 1:
        print "You choose [APP Push]"
        request.AppPush()
    else:
        print "You choose [List Push]"
        request.ListPush()
    '''
    
    ##�ڶ��ַ���
    
    if int(request.push_type) == 0:
        print "You choose [Single Push]"
        request.SinglePush2()
    elif int(request.push_type) == 1:
        print "You choose [APP Push]"
        request.AppPush2()
    else:
        print "You choose [List Push]"
        request.ListPush2()
    
    
    
    