#usr/bin/python
# -*- coding: utf-8 -*-
# @author Woonhyuk Baek

import os, sys, socket 
import time, uuid
import logging
from string import Template

module_path = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname( os.path.abspath(__file__) )
                )
            )
        ) + '/JarvisPy'
print module_path
sys.path.append( module_path )

import twisted
from twisted.web import server, resource, http
from twisted.internet import reactor, threads, defer

PROJECT_NAME = 'SAMPLE'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FRAME_TEMPLATE = BASE_PATH + '/template/frame.html'
HTML_DATA_TEMPLATE = BASE_PATH + '/template/data.html'
HTML_QUERY_TEMPLATE = BASE_PATH + '/template/query.html'
frameTemplate = Template(open(HTML_FRAME_TEMPLATE).read())
dataTemplate = Template(open(HTML_DATA_TEMPLATE).read())
queryTemplate = Template(open(HTML_QUERY_TEMPLATE).read())

UPLAOD_FILE_PATH = BASE_PATH + '/upload/'
UPLOAD_FILE_URL = 'HTTP_ALIAS_PTH/'

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
        query = queryTemplate.substitute(queryBindingData)

#        dataTemplate = Template(open(HTML_DATA_TEMPLATE).read())
        data = ''
        if len(query) > 1: # is valid query
            # call search engine
            # ...

            # result
            resultList = [
                {'image':'http://10.33.37.185/flickr/Starbucks/7851954064_7299785025_b.jpg'},
                {'image':'http://10.33.37.185/flickr/Starbucks/7560466908_2be71fa4ce_b.jpg'},
                {'image':'http://10.33.37.185/flickr/Starbucks/7875493092_45e0a116e6_b.jpg'},
                {'image':'http://10.33.37.185/flickr/Starbucks/7910756016_2f58993ab1_b.jpg'},
                {'image':'http://10.33.37.185/flickr/Starbucks/7872406120_7073fdd596_b.jpg'},
                {'image':'http://10.33.37.185/flickr/Starbucks/7822293938_2f0863ee1a_b.jpg'},
                ]

            count = len(resultList)
            for idx, result in enumerate(resultList):
                dataBindingData = {'TITLE':str(idx), 'DATA':result['image']}
                data += dataTemplate.substitute(dataBindingData)
            if count == 0:
                data = '<div class="alert"><strong>Warning!</strong> No Results!!</div>'

#        frameTemplate = Template(open(HTML_FRAME_TEMPLATE).read())
        frameBindingData = {'PROJECT_NAME':PROJECT_NAME, 'QUERY':query, 'BODY':data}
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
 
