import sys
from cli import CLI

def main():
    arg = []
    link = ''
    
    for a in sys.argv:
        if(a.startswith("https://") and link==''):
            link = a
    if '-h' in sys.argv:
        arg.append('-h')
    if '-s' in sys.argv:
        arg.append('-s')
    if '-v' in sys.argv:
        arg.append('-v')
    if '-m' in sys.argv:
        arg.append('-m')
        
    cli = CLI(arg=arg, link=link)
    cli.cli()
            


if __name__=='__main__':
    main()