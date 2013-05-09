import os
import sys

sys.path.append( os.path.dirname(os.path.abspath(__file__)) + '/JarvisPy/' )
from crawler.youtube import Youtube

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage : python ' + sys.argv[0] + ' http://www.youtube.com/watch?v=mV6cvBorTfg'
        exit()

    youtube = Youtube(sys.argv[1])
    video = youtube.downloadVideo()

    if len(video) > 0:
        fp = open('/storage/downloads/' + youtube.getVideoId() + ".mp4", 'w')
        fp.write(video)
        fp.close()

    print 'done.'

