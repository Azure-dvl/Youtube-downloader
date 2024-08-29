#!/bin/python

import sys
import asyncio

async def Descargar(comando, link):
    directorio="-o $HOME/Downloads/'%('title')'s.'%('ext')'s "
    num = await asyncio.create_subprocess_shell(f"yt-dlp {comando} {directorio} {link}")
    await num.communicate()
    print('Fin de la descarga')

def Argumentos():
    print('-h Ayuda\n-d Descargar un solo archivo\n-p Descargar playlist\n-s Descarga con subtitulos')

async def Subtitulos(link):
    num = await asyncio.create_subprocess_shell(f"yt-dlp --list-subs {link}")
    await num.communicate()
    idioma=input('Ingrese el lenguaje del subtitulo: ')
    
    return idioma

async def main():
    link = ''
    comando = ''

    if '-p' in sys.argv:
        comando+='-f mp4 --restrict-filenames --yes-playlist --no-overwrites '
    if '-s' in sys.argv:
        idioma = await Subtitulos(link)
        comando+=f'--write-sub --sub-lang {idioma} '
    if '-d' in sys.argv:
        comando+='-f mp4 --restrict-filenames '
    if '-h' in sys.argv:
        Argumentos()
        sys.exit()

    for arg in sys.argv:
        if(arg.startswith("https://") and link==''):
            link = arg

    if(link==''):
        link=input('Ingrese el link: ') 
    
    while True:
        await Descargar(comando, link)
        entrada=input('Ingrese el link, h para cambiar de argumentos o q para salir): ')
        if entrada=='q':
            print('^~^')
            break   
        elif entrada=='h':
            Argumentos()
            comando=''
            arg=input('Ingrese los argumentos: ')
            link=input('Ingrese el link: ')
            for a in arg:
                if a=='p':
                    comando+='-f mp4 --restrict-filenames --yes-playlist --no-overwrites '
                elif a=='d':
                    comando+='-f mp4 --restrict-filenames '
                elif a=='s':
                    idioma = await Subtitulos(link)
                    comando+=f'--write-sub --sub-lang {idioma} '
        else:
            link=entrada

if __name__=='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Detencion forzada.")
        num = input('Deseas correr el programa de nuevo? y o n: ')
        if num=='y':
            asyncio.run(main())
        else:
            print('Gracias x usarnos')