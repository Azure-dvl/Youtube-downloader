import logging.config
import sys

from function.download import Download
from function.youtube import Youtube

class CLI:
    logging.basicConfig(
        level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    )
    
    def __init__(self, arg:list[str], link:str):
        logger_youtube = logging.getLogger('yt_dlp_custom')
        self.arg = arg
        self.link = link
        self.yt = Youtube(logger=logger_youtube)
        self.dw = Download(logguer=logger_youtube)
        self.sub = False
    
    def cli(self):
        print('--------------------- Welcome --------------------')
        if len(self.arg)>0:
            for a in self.arg:
                if '-h' == a:
                    self.options()
                    sys.exit()
                if(self.link==''):
                    self.link=input('Please insert the YouTube link or exit the Program: ')
                elif '-s' == a:
                    self.sub = True
                elif '-m' == a:
                    self.yt.download_music(link=self.link)
                elif '-v' == a:
                    if(self.link.startswith("https://youtube.com/playlist")):
                        self.yt.download(link=self.link, sub=self.sub, playlist=True)
                    elif(self.link.startswith("https://youtu.be")):
                        self.yt.download(link=self.link, sub=self.sub, playlist=False)
                    else:
                        self.dw.download(link=self.link, recursive=False)
        else:
            self.options()
    
    def options(self):
        print('-h   help\n-v   download\n-m   download music\n-s   download with subtitle\n[commands] [link]')