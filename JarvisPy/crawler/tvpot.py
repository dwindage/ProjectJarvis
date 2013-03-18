import sys
import urllib
import uuid

CONNECTION_PATH = 'http://videofarm.daum.net'
INFO_PATH = '/controller/api/open/v1_2/MovieLocation.apixml?play_loc=tvpot&profile=HIGH&vid='

class Tvpot:
    # url : http://tvpot.daum.net/v/v829dp9tL9w11tLfwWwmWyo
    # url : v829dp9tL9w11tLfwWwmWyo
    def __init__(self, url):
	self.url = url
	self.videoId = self.__parseUrl__(url)
	self.videoInfoList = []

    def getVideoId(self):
	return self.videoId

    def getVideoType(self):
        infoPath = INFO_PATH + self.videoId;
	info = self.__downloadPage__(CONNECTION_PATH, infoPath);

	# get video URL
	self.videoInfoList = self.__parseTvpotInfo__(info)
	return self.videoInfoList

    def getDownloadUrl(self, index=-1):
	if len(self.videoInfoList) == 0:
	    self.getVideoType()
	if len(self.videoInfoList) <= index:
	    index = len(self.videoInfoList)-1;
	if index == -1:
	    index = self.__selectBestVideo__()
	if len(self.videoInfoList) <= index:
	    return ''

	videoUrl = self.__makeVideoPath__(self.videoInfoList[index])
	return videoUrl

    # default parameter is best query of viedo
    def downloadVideo(self, index=-1):
	return self.__downloadVideo__(self.getDownloadUrl(index))

    def __downloadPage__(self, connPath, infoPath):
	data = ''
        try:
	    response = urllib.urlopen(connPath + infoPath)
	    data = response.read()
	except :
	    data = ''
	return data

    def __downloadVideo__(self, fileUrl):
	video = ''
	try:
	    response = urllib.urlopen(fileUrl);
	    video = response.read();
	except:
	    video = ''
	return video

    def __parseArguments__(self, stringData):
	resultDict = {}
	if '?' in stringData:
	    stringData = stringData.split('?')[-1]

	dataList = stringData.split('&')
	for data in dataList:
	    if '=' in data:
		key, value = data.split('=')
		resultDict[key] = urllib.unquote(value)
	return resultDict

    def __parseFunction__(self, stringData):
	result = ''
	if '?' in stringData:
	    stringData = stringData.split('?')[0]
	return stringData.split('/')[-1]

    def __parseUrl__(self, url):
	dic = self.__parseArguments__(url);
	vid = ''
	if dic.has_key('v'):
	    vid = dic['v']
	elif not '=' in url and not '/' in url:
	    vid = url
	elif not '=' in url:
	    vid = url.split('/')[-1]
	return vid

    def __parseTvpotInfo__(self, infoData):
	resultList = []
	try:
	    if '<url>' in infoData and '</url>' in infoData:
		url = infoData.split('<url><![CDATA[')[-1].split(']]></url>')[0]
		filename = self.__parseFunction__(url).split('.')[-1]
		resultList.append({'url':url, 'type':filename})
	except:
	    resultList = []
	return resultList

    def __selectBestVideo__(self):
        index = 0
	for i in range(len(self.videoInfoList)):
	    if index > 0:
		continue
	    if 'mp4' in self.videoInfoList[i]['type']:
		index = i
	return index

    def __makeVideoPath__(self, videoInfo):
	video = videoInfo
        videoUrl = video['url']
	return videoUrl

    def __getExetentionType_(typeString):
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
    tvpot = Tvpot('http://tvpot.daum.net/v/v829dp9tL9w11tLfwWwmWyo')
    print tvpot.getVideoId()
    print tvpot.getDownloadUrl()
    data = tvpot.downloadVideo()
    fp = open(tvpot.getVideoId() + ".1.flv", 'w')
    fp.write(data)
    fp.close()

#from JarvisPy.crawler.tvpot import Tvpot
#tvpot = Tvpot('http://tvpot.daum.net/v/v829dp9tL9w11tLfwWwmWyo')
#video = tvpot.downloadVideo()


