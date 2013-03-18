import sys

from JarvisPy.crawler.youtube import Youtube
from JarvisPy.crawler.tvpot import Tvpot

if __name__ == '__main__':
    if len(sys.argv) < 2:
	print 'Usage : python ' + sys.argv[0] + ' url_path("http://www.youtube.com/watch?v=mV6cvBorTfg") [output_filename(optional)]'
	exit(0)

    url = sys.argv[1]
    crawler = ''
    if 'youtu' in url:
	crawler = Youtube(url)
    elif 'daum' in url:
	crawler = Tvpot(url)
    video = crawler.downloadVideo()

    filename = ''
    if len(sys.argv) == 3:
	filename = sys.argv[2]
    else:
	filename = crawler.getVideoId() + '.flv'

    fp = open(filename, 'w')
    fp.write(video)
    fp.close()
