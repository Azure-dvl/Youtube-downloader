import sys
from function import Functions

class CLI:
    def __init__(self, arg:list[str], link:str):
        self.arg = arg
        self.link = link
        self.fun = Functions()
        self.sub = False
    
    def cli(self):
        print('--------------------- Welcome --------------------')
    
        if(self.link==''):
            self.link=input('Please insert the YouTube link or exit the Program: ')

        if len(self.arg)>0:
            for a in self.arg:
                if '-h' == a:
                    self.options()
                    sys.exit()
                elif '-s' == a:
                    self.sub = True
                elif '-m' == a:
                    self.fun.download_music(link=self.link)
                elif '-p' == a:
                    if(self.link.startswith('https://youtube.com/playlist')):
                        self.fun.download(link=self.link, sub=self.sub, playlist=True)
                    elif(self.link.startswith('https://youtube.com/playlist')):
                        self.fun.download(link=self.link, sub=self.sub, playlist=False)
        else:
            self.options()
    
    def options(self):
        print('-h   help\n-v   download\n-m   download music\n-s   download with subtitle')