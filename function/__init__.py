import logging
import yt_dlp
from yt_dlp import YoutubeDL

class Functions:
    '''Class for all the manage of the yt_dlp lib'''
    
    # logger config
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    def __init__(self):
        self.folder='./Downloads'
        self.logger = logging.getLogger('yt_dlp_custom')
            
    def get_format(self, info):
        '''Get all the video formats available'''
        ydl_opts={
            'logger': self.logger,
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            list_formats = ydl.list_formats(info)
            return input("Format's id: ")
            
    def get_info(self, link):
        '''Get info of the video'''
        ydl_opts={
            'list_subs':True,
            'logger': self.logger,
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            self.logger.info('Getting info ...')
            return ydl.extract_info(link, download=False, process=False)
    
    def download(self, link:str, sub:bool, playlist:bool):
        if(playlist):
            self.folder += '//Playlists/%(playlist_uploader)s ## %(playlist)s/%(title)s ## %(uploader)s ## %(id)s.%(ext)s'
        else:
            self.folder += '//Videos/%(title)s ## %(uploader)s ## %(id)s.%(ext)s'
            
        info = self.get_info(link)
        format = self.get_format(info)
        if(sub):
            subtitle = self.get_subtitle(info)
        ydl_opts = {
            'outtmpl': self.folder,
            'ignoreerrors': True,
            'abort_on_unavailable_fragments': True,
            'logger': self.logger,
            'quiet': True,
            'format': format,
            'writesubtitles': sub,
            'subtitleslangs': subtitle,
            'subtitlesformat': 'vtt',
        }
        with YoutubeDL(ydl_opts) as ydl:
            self.logger.info('Downloading ...')
            ydl.download(link)
            self.logger.info('Download complete!')
    
    def get_subtitle(self, info):
        '''Get the list of all the subtitles available'''
        subs = []
        with YoutubeDL() as ydl:
            list_subtitles = info.get('subtitles', {})
            print('List of subtitles availables')
            for lang, sub_info in list_subtitles.items():
                print(f"Language: {lang}")
            subs.append(input('Insert the language short: '))
            return subs
    
    def download_music(self, link):
        '''Extract and download the music of the video'''
        self.folder += '//Music/%(title)s ## %(uploader)s ## %(id)s.%(ext)s'
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