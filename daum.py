import sys
from JarvisPy.crawler.tvpot import Tvpot

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage : python ' + sys.argv[0] + ' http://www.youtube.com/watch?v=mV6cvBorTfg'
        exit()

    youtube = Tvpot(sys.argv[1])
    video = youtube.downloadVideo()

    fp = open('/home/pi/videos/others/' + youtube.getVideoId() + ".mp4", 'w')
    fp.write(video)
    fp.close()

    print 'done.'
