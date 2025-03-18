from yt_dlp import YoutubeDL
from bs4 import BeautifulSoup

class Download:
    '''Download manager of anything else'''
    def __init__(self, logguer):
        self.logger = logguer
        self.folder='./Downloads/%(title)s.%(ext)s'
    
    def download(self, link, recursive):
        if(recursive):
            # Poner el name de la carpeta
            self.get_links(link)
        
        ydl_opts = {
            'outtmpl': self.folder,
            'ignoreerrors': True,
            'abort_on_unavailable_fragments': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            self.logger.info('Starting download ...')
            ydl.download(link)
            self.logger.info('Download complete!')
    
    def get_links(self, link):
        self.logger.info('Getting links')
    
    