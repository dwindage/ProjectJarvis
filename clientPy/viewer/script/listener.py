#usr/bin/python
# -*- coding: utf-8 -*-
# @author Woonhyuk Baek

import os, sys, socket 
import time, uuid
import urllib, urllib2
import logging
from string import Template

module_path = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname( os.path.abspath(__file__) )
                )
            )
        ) + '/JarvisPy'
sys.path.append( module_path )

import twisted
from twisted.web import server, resource, http
from twisted.internet import reactor, threads, defer
import simplejson as json

PROJECT_NAME = 'Jarvis'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FRAME_TEMPLATE = BASE_PATH + '/template/frame.html'
HTML_DATA_TEMPLATE = BASE_PATH + '/template/data.html'
HTML_QUERY_TEMPLATE = BASE_PATH + '/template/query.html'
frameTemplate = Template(open(HTML_FRAME_TEMPLATE).read())
dataTemplate = Template(open(HTML_DATA_TEMPLATE).read())
queryTemplate = Template(open(HTML_QUERY_TEMPLATE).read())

UPLAOD_FILE_PATH = BASE_PATH + '/upload/'
UPLOAD_FILE_URL = 'HTTP_ALIAS_PTH/'

#Wolfram|Alpha back door : urllib2.urlopen(API, "content=query").read()
WOLFRAM_ALPHA_API = 'http://derik-wa.appspot.com/walpha'
def callWolframAlpha(query):
    try:
        responseString = urllib2.urlopen( WOLFRAM_ALPHA_API, 'content='+query.strip() ).read()
        jsonr = eval(responseString);
        result = [x for x in jsonr if x[0] == 'pod']
    except Exception, e:
        print '[ERRO]', '[callWolframAlpha]', str(e)
        result = []
    return result

def getReqArg(args, key, default=''):
    value = default
    try:
        if args.has_key(key):
            if len(args[key][0]) > 0:
                value = args[key][0]
    except Exception, e:
        print '[ERRO]', '[getReqArg]', str(e)
    return value

def index(req):
#    queryTemplate = Template(open(HTML_QUERY_TEMPLATE).read())
    queryBindingData = {'QUERY':'', 'DESCRIPTION':''}
    query = queryTemplate.substitute(queryBindingData)

#    frameTemplate = Template(open(HTML_FRAME_TEMPLATE).read())
    frameBindingData = {'PROJECT_NAME':PROJECT_NAME, 'QUERY':query, 'BODY':''}
    resultHtml = frameTemplate.substitute(frameBindingData)

    req.setHeader('Content-type', 'text/html')
    req.write(resultHtml)
    req.finish()
    return

def search(req):
    try:
        args = req.args
        query = getReqArg(args, "q", "")
        query = urllib.unquote(query)
        filestream = getReqArg(args, "f", "")

        # if file uploaed
        if len(query) == 0 and len(filestream) > 0:
            # save file
            filename = '%s_%s.jpg' % (time.strftime("%Y-%M-%D", time.localtime()), uuid.uuid4())
            filepath = UPLAOD_FILE_PATH 
            try:
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                of = file(filepath + filename, 'wb')
                of.write(filestream)
                of.close()

                fileurl = UPLOAD_FILE_URL + filename
                query = fileurl
            except Exception, e:
                print '[ERRO]', '[upload]', str(e)
            
#        queryTemplate = Template(open(HTML_QUERY_TEMPLATE).read())
        queryBindingData = {'QUERY':query, 'DESCRIPTION':''}
        queryResult = queryTemplate.substitute(queryBindingData)

#        dataTemplate = Template(open(HTML_DATA_TEMPLATE).read())
        data = ''
        if len(query) > 1: # is valid query
            # call search engine
            resultList = []
            for i in range(3):
                jsonr = callWolframAlpha(query)
                if len(jsonr) > 0:
                    resultList = jsonr
                    break;

            count = len(resultList)
            for idx, result in enumerate(resultList):
                title = [x for x in result if x[0] == 'title'][0][1]
                sub = [x for x in result if x[0] == 'subpod']

                plaintext = ''
                imageList = []
                for pod in sub:
                    plaintext_temp = [x for x in pod if x[0] == 'plaintext']
                    image_temp = [x for x in pod if x[0] == 'img']
                    if len(plaintext_temp) > 0:
                        if len(plaintext_temp[0]) == 2:
                            plaintext = plaintext_temp[0][1]
                    if len(image_temp) > 0:
                        if len(image_temp[0]) >= 2:
                            imageList.append(image_temp[0][1][1])

                resultHtml = ''
                if len(plaintext) > 1:
                    plaintext = plaintext.replace('My name is Wolfram|Alpha.', 'Jarvis')
                    resultHtml += plaintext
                else:
                    for image in imageList:
                        resultHtml += '<img src="' + image + '"/>'

                dataBindingData = {'TITLE':title, 'DATA':resultHtml}
                data += dataTemplate.substitute(dataBindingData)
            if count == 0:
                data = '<div class="alert"><strong>Warning!</strong> No Results!!</div>'

#        frameTemplate = Template(open(HTML_FRAME_TEMPLATE).read())
        frameBindingData = {'PROJECT_NAME':PROJECT_NAME, 'QUERY':queryResult, 'BODY':data}
        resultHtml = frameTemplate.substitute(frameBindingData)

        req.setHeader('Content-type', 'text/html')
        req.write(resultHtml)
        req.finish()
    except Exception, e:
        print '[ERRO]', '[search]', str(e)
    return

class HandleRequest(http.Request):
    pageHandlers = {
        '/':index,
        '/search':search,
        }

    def process(self):
        if self.pageHandlers.has_key(self.path):
            # is valid request
            print '[INFO]', '[REQUEST]',
            print self.getClientIP() + ' ' + self.method + ' ' + self.uri
            print '[INFO]', '[REQUEST]', '[PARAM] ' + str(self.args)[:200]

            handler = self.pageHandlers[self.path]
            d = threads.deferToThread(handler, self)
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.setHeader('Content-type', 'text/html')
            self.write('<H1>Not Found</H1>Sorry, no such page.')
            self.finish()

class MyHttp(http.HTTPChannel):
    requestFactory = HandleRequest

class MyHttpFactory(http.HTTPFactory):
    protocol = MyHttp

if __name__ == '__main__':
    print module_path
    if len(sys.argv) != 2:
        print sys.stderr, 'Usage : ' + sys.argv[0] + ' PORT'
        exit()

    port = int(sys.argv[1])
    localIP = socket.gethostbyname(socket.gethostname())

    print '[INFO]', '[DAEMON]', ':::::::::::::::::::::::::::::::::::'
    print '[INFO]', '[DAEMON]', 'START listener - ' + str(localIP) + ':' + str(port)
    print '[INFO]', '[DAEMON]', ':::::::::::::::::::::::::::::::::::'

    reactor.suggestThreadPoolSize(16)
    reactor.listenTCP(port, MyHttpFactory())
    reactor.run()

    print '[INFO]', '[DAEMON]', ':::::::::::::::::::::::::::::::::::'
    print '[INFO]', '[DAEMOM]', 'STOP listener'
    print '[INFO]', '[DAEMON]', ':::::::::::::::::::::::::::::::::::'
 
