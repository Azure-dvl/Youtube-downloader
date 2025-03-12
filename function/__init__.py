import logging
import logging.config
from yt_dlp import YoutubeDL
from yt_dlp import utils

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
        '''Getting the info of the video'''
        ydl_opts={
            'extract_flat': True,
            'listformats':True,
            'listsubtitles':True,
            'logger': self.logger,
            'quiet': True,
            'skip_download':True
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            self.logger.info('Getting info ...')
            return ydl.extract_info(link, download=False, process=False)
    
    def entries(self, info):
        '''Sent the entries's playlist'''
        list_urls = info.get('entries', [])
        for u in list_urls:
            return u.get('url')
    
    def get_all(self, info, sub:bool, playlist:bool):
        '''Sent the info to subtitle and format'''
        format = ''
        subtitle = ''
        if(playlist):
            url = self.entries(info)
            url_info = self.get_info(url)
            format = self.get_format(url_info)
            if(sub):
                print(url_info)
                subtitle = self.get_subtitle(url_info)
        else:
            format = self.get_format(info)
            if(sub):
                subtitle = self.get_subtitle(info)
        
        return format, subtitle
        
    def get_format(self, info):
        '''Sent the list of all the formats available'''
        list_formats = info.get('formats', [])
        print('-------------------- List of formats availables --------------------')
        for f in list_formats:
            if f.get('resolution')!='audio only' and f.get('filesize', 'N/A')!='N/A' and f.get('ext')!='mhtml' and f.get('format_note', 'N/A')!='N/A':
                print(
                    f"ID: {f['format_id']}, "
                    f"Size: {utils.format_bytes(f.get('filesize'))} Mb, "
                    f"Format: {f.get('ext')}, "
                    f"Resolucion: {f.get('format_note')}"
                )
        return input("Format's id: ")
    
    def get_subtitle(self, info):
        '''Sent the list of all the subtitles available'''
        subs = []
        list_subtitles = info.get('subtitles', {})
        print('-------------------- List of subtitles availables --------------------')
        
        for lang, sub_info in list_subtitles.items():
            print(f"Language: {lang}")

        subs.append(input('Insert the language short: '))
        return subs
    
    def download(self, link:str, sub:bool, playlist:bool):
        '''Download the video or playlist'''
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