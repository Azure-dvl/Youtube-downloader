from yt_dlp import YoutubeDL
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

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
            # 'cookies-from-browser': 'brave'
        }
        with YoutubeDL(ydl_opts) as ydl:
            if(recursive):
                links = self.get_links(link)
                for l in links:
                    if l:
                        ydl.download(l)
            else:
                self.logger.info('Starting download ...')
                ydl.download(link)
                self.logger.info('Download complete!')
    
    def get_links(self, link, content_selector=None):
        self.logger.info('Getting links')
        try:
            r_link = requests.get(link)
            r_link.raise_for_status()
            html = r_link.content
            s_link = BeautifulSoup(html, "html.parser")

            if content_selector:
                container = s_link.select_one(content_selector)
                if not container:
                    self.logger.warning(f"No element found with selector: {content_selector}")
                    return []
                content_links = container.find_all('a', href=True)
            else:
                content_links = s_link.find_all('a', href=True)
        
            list_links = []
            base_url = link if link.endswith('/') else link + '/'

            for a in content_links:
                href = a.get('href')
                if href and not href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    absolute_url = urljoin(base_url, href)
                    list_links.append(absolute_url)
            
            self.logger.info(f'Found {len(list_links)} links')
            return list_links

        except requests.RequestException as e:
            self.logger.error(f"Error fetching links: {e}")
            return []
        
        
        
    
    