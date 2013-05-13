import sys
import os

sys.path.append( os.path.dirname(os.path.abspath(__file__)) + '/../../JarvisPy/' )
from crawler.tvpot import Tvpot

if __name__ == '__main__':
    if len(sys.argv) != 2:
		print 'Usage : python ' + sys.argv[0] + ' http://tvpot.daum.net/v/v829dp9tL9w11tLfwWwmWyo'
		exit()

    tvpot = Tvpot(sys.argv[1])
    video = tvpot.downloadVideo()

    if len(video) > 0:
        fp = open('/storage/downloads/' + tvpot.getVideoId() + ".mp4", 'w')
        fp.write(video)
        fp.close()

    print 'done.'

