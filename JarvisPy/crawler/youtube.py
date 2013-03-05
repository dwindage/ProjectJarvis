import sys
import urllib
import uuid

CONNECTION_PATH = 'http://www.youtube.com'
INFO_PATH = '/get_video_info?el=popout&amp;video_id='

class Youtube:
    # url : http://www.youtube.com/watch?v=mV6cvBorTfg
    # url : http://youtu.be/mV6cvBorTfg
    # url : mV6cvBorTfg
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
	self.videoInfoList = self.__parseYoutubeInfo__(info)
	return self.videoInfoList

    # default parameter is best query of viedo
    def downloadVideo(self, index=-1):
	if len(self.videoInfoList) == 0:
	    self.getVideoType()
	if len(self.videoInfoList) <= index:
	    index = len(self.videoInfoList)-1;
	if index == -1:
	    index = self.__selectBestVideo__()
	if len(self.videoInfoList) <= index:
	    return ''

	videoUrl = self.__makeVideoPath__(self.videoInfoList[index])
	return self.__downloadVideo__(videoUrl)

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

    def __parseYoutubeInfo__(self, infoData):
	resultList = []
	try:
	    stream_map = self.__parseArguments__(infoData)['url_encoded_fmt_stream_map']
	    list_of_stream = stream_map.split(',')

	    for stream in list_of_stream:
		tempDict = self.__parseArguments__(stream)
		resultList.append(tempDict)
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
        videoUrl = video['url'] + '&signature=' + video['sig']
        videoUrl += '&title=file';
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
    youtube = Youtube('http://www.youtube.com/watch?v=mV6cvBorTfg')
    print youtube.getVideoId()
    print youtube.getVideoType()[0]['quality']
    data = youtube.downloadVideo()
    fp = open(youtube.getVideoId() + ".1.flv", 'w')
    fp.write(data)
    fp.close()

    youtube = Youtube('http://youtu.be/mV6cvBorTfg')
    print youtube.getVideoId()
    data = youtube.downloadVideo()
    fp = open(youtube.getVideoId() + ".2.flv", 'w')
    fp.write(data)
    fp.close()

    youtube = Youtube('mV6cvBorTfg')
    print youtube.getVideoId()
    data = youtube.downloadVideo()
    fp = open(youtube.getVideoId() + ".3.flv", 'w')
    fp.write(data)
    fp.close()

#from JarvisPy.crawler.youtube import Youtube
#youtube = Youtube('http://www.youtube.com/watch?v=mV6cvBorTfg')
#video = youtube.downloadVideo()

