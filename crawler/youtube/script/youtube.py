import sys
import urllib
import uuid

CONNECTION_PATH = 'http://www.youtube.com';
INFO_PATH = '/get_video_info?el=popout&amp;video_id=';

import time
def getTickCount():
    return time.time() * 1000.0 #return milliseconds

def downloadPage(connPath, infoPath):
    data = '';
    try:
        response = urllib.urlopen(connPath + infoPath);
        data = response.read();
    except :
        print 'Error : function downloadPage';
    return data;

def downloadVideo(fileUrl, fileName):
    try:
        response = urllib.urlopen(fileUrl);
        video = response.read();

        f = open(fileName, 'wb');
        f.write(video);

        f.close();
    except:
        print 'Error : function downloadVideo';
    return;

def parseArguments(stringData):
    resultDict = {}

    dataList = stringData.split('&')
    for data in dataList:
	if '=' in data:
	    key, value = data.split('=')
	    resultDict[key] = urllib.unquote(value)

    return resultDict

def parseYoutubeInfo(infoData):
    resultList = []

    stream_map = parseArguments(infoData)['url_encoded_fmt_stream_map']
    list_of_stream = stream_map.split(',')

    for stream in list_of_stream:
	tempDict = parseArguments(stream)
	resultList.append(tempDict)

    return resultList

def getExetentionType(typeString):
    rv = '.flv'
    if 'mp4' in typeString:
	rv = '.mp4'
    elif 'webm' in typeString:
	rv = '.webm'
    elif 'flv' in typeString:
	rv = '.flv'
    else:
	rv = '.flv'
    return rv

if __name__ == '__main__':
    inputUrl = sys.argv[1];

    videoId = '';
    tempUrls = inputUrl.split('&amp;');
    for url in tempUrls:
        index = url.find('v=')+2;
        if index >= 0:
            videoId = url[index:];
    print 'videoId : ' + videoId;
    
    infoPath = INFO_PATH + videoId;
    info = downloadPage(CONNECTION_PATH, infoPath);

    # get video URL
    videoUrlList = parseYoutubeInfo(info)

    print 'video stream type list'
    for video in videoUrlList:
	print video['quality'] + ' (' + video['type'] + ') :',
	print video['url'][:30] + '...'

    index = 0
    for i in range(len(videoUrlList)):
	if index > 0:
	    continue
	if 'mp4' in videoUrlList[i]['type']:
	    index = i

    count = len(videoUrlList)
    if count > 0:
        # make a pattern
	video = videoUrlList[index]
        videoUrl = video['url'] + '&signature=' + video['sig']
        videoUrl += '&title=file';

	print 'download : ' + video['quality'] + ' (' + video['type'] + ')'
        print 'videoUrl : ' + videoUrl;
        print 'downloading...';

	startTick = getTickCount()

        filename = videoId + '_' + video['quality'] + getExetentionType(video['type'])
        downloadVideo(videoUrl, filename);

	endTick = getTickCount()

        print 'done. as ' + filename
	print '(download time : ' + str(endTick - startTick) + 'ms)'
    else:
        print 'invalied data';

