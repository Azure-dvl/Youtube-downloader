import logging
import logging.config
from yt_dlp import YoutubeDL

class Functions:
    '''Class for all the manage of the yt_dlp lib'''
    
    # logger config
    logging.basicConfig(
        level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    )
    
    def __init__(self):
        self.folder='./Downloads'
        self.logger = logging.getLogger('yt_dlp_custom')
            
    def get_info(self, link):
        '''Get info of the video'''
        ydl_opts={
            'extract_flat': True,
            'list_subs':True,
            'logger': self.logger,
            'quiet': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            self.logger.info('Getting info ...')
            return ydl.extract_info(link, download=False, process=False)
    
    def entries(self, info):
        return info.get('entries', [])
    
    def get_all(self, info, sub:bool, playlist:bool):
        '''Get all the formats available'''
        format = ''
        subtitle = ''
        ydl_opts={
            'logger': self.logger,
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            if(playlist):
                url = ''
                
                for video in self.entries(info):
                    url = video.get('url')
                
                link = self.get_info(url)
                list_formats = ydl.list_formats(link)
                format = input("Format's id: ")
                if(sub):
                    subtitle = self.get_subtitle(link)
            
            else:
                list_formats = ydl.list_formats(info)
                format = input("Format's id: ")
                if(sub):
                    subtitle = self.get_subtitle(info)
            return format, subtitle
    
    def get_subtitle(self, info):
        '''Get the list of all the subtitles available'''
        subs = []
        list_subtitles = info.get('subtitles', {})
        print('List of subtitles availables')
        
        for lang, sub_info in list_subtitles.items():
            print(f"Language: {lang}")

        subs.append(input('Insert the language short: '))
        return subs
    
    def download(self, link:str, sub:bool, playlist:bool):
        if(playlist):
            self.folder += '/Playlists/%(playlist)s/%(title)s.%(ext)s'
        
        else:
            self.folder += '/Videos/%(title)s.%(ext)s'
            
        info = self.get_info(link)
        format, subtitle = self.get_all(info, sub=sub, playlist=playlist)
        
        ydl_opts = {
            'outtmpl': self.folder,
            'ignoreerrors': True,
            'abort_on_unavailable_fragments': True,
            'format': format,
            'writesubtitles': sub,
            'subtitleslangs': subtitle,
            'subtitlesformat': 'vtt',
        }
        with YoutubeDL(ydl_opts) as ydl:
            self.logger.info('Starting download')
            ydl.download(link)
            self.logger.info('Download complete!')
    
    def download_music(self, link):
        '''Extract and download the music of the video'''
        self.folder += '/Music/%(title)s.%(ext)s'
        ydl_opts = {
            'outtmpl': self.folder,
            'ignoreerrors': True,
            'abort_on_unavailable_fragments': True,
            'logger': self.logger,
            'quiet': True,
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            self.logger.info('Downloading ...')
            ydl.download(link)
            self.logger.info('Download complete!')