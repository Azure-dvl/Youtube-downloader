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
        folder='./Video/'
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
            self.logger.info('Getting list of formats availables')
            return ydl.extract_info(link, download=False, process=False)
    
    def download_stream(self, link:str, sub:bool):
        '''Download the video with the format selected and (if U wanted) the subtitle'''
        info = self.get_info(link)
        format = self.get_format(info)
        if(sub):
            subtitle = self.get_subtitle(info)
        ydl_opts = {
            'format': format,
            'writesubtitles': sub,
            'subtitleslangs': subtitle,
            'subtitlesformat': 'vtt',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(link)
    
    def download_play(self, link:str, sub:bool):
        '''Download the playlist with the format selected and (if U wanted) the subtitles'''
        info = self.get_info(link)
        format = self.get_format(info)
        if(sub):
            subtitle = self.download_sub(format)
        ydl_opts = {
            'format': format,
            'writesubtitles': sub,
            'subtitleslangs': subtitle,
            'subtitlesformat': 'srt'
        }
    
    def get_subtitle(self, info):
        '''Get the list of all the subtitles available'''
        with YoutubeDL() as ydl:
            list_subtitles = info.get('subtitles', {})
            print('List of subtitles availables')
            for lang, sub_info in list_subtitles.items():
                print(f"Language: {lang}")
            return input('Insert the language short: ')
    
    def download_music(self, link):
        '''Extract and download the music of the video'''
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(link)