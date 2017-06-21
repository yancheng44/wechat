#!/usr/bin/env python
#coding=utf-8
import os,urllib2,requests,sys,time,json,pickle

corpid = 'wx15565f83aa3c66b8'
secret = 'SP3IIAU-69WIIcq3LULKgC_QzZnV71k9wnP-0Xp5jla13TEJkQQja2nNDTsIsBa3'

class Token(object):
  """Get AccessToken"""
  def __init__(self, corpid, secret):
    self.baseurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(corpid, secret)
    self.expire_time = sys.maxint
  def get_token(self):
    if self.expire_time > time.time():
      request = urllib2.Request(self.baseurl)
      response = urllib2.urlopen(request)
      ret = response.read().strip()
      ret = json.loads(ret)
      if 'errcode' in ret.keys():
        print >> ret['errmsg'], sys.stderr
        sys.exit(1)
      self.expire_time = time.time() + ret['expires_in']
      self.access_token = ret['access_token']
    return self.access_token
def SendMsg(user, title, content):
  gettoken = Token(corpid=corpid, secret=secret).get_token()
  url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}".format(gettoken)
  varload = {
    "touser":"{0}".format(user),
    "msgtype":"text",
    "agentid":"1",
    "text":{
      "content":"{0}\n{1}".format(title, content)
    },
    "safe":"0"
  }
  ret = requests.post(url, data=json.dumps(varload, ensure_ascii=False))
  print ret.json()
#if __name__ == '__main__':
SendMsg(sys.argv[1],sys.argv[2],sys.argv[3])