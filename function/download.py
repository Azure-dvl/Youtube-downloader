from yt_dlp import YoutubeDL
from bs4 import BeautifulSoup
import requests

class Download:
    '''Download manager of anything else'''
    def __init__(self, logguer):
        self.logger = logguer
        self.folder='~/Downloads/%(title)s.%(ext)s'
    
    def download(self, link, recursive):
        ydl_opts = {
            'outtmpl': self.folder,
            'ignoreerrors': True,
            'abort_on_unavailable_fragments': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            if(recursive):
                links = self.get_links(link)
                for l in links:
                    ydl.download(l)
            else:
                self.logger.info('Starting download ...')
                ydl.download(link)
                self.logger.info('Download complete!')
    
    def get_links(self, link):
        self.logger.info('Getting links') 
        r_link = requests.get(link)
        html = r_link.content
        s_link = BeautifulSoup(html, "html.parser")
        content_links = s_link.find_all('a')
        list_links = []
        for a in content_links:
            list_links.append(a.get('href'))
        
        print(list_links)
        return list_links
        
        
        
    
    