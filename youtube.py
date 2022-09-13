from pytube import YouTube as yt, Playlist
import sys, time, traceback

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
videos_error = []
def DownloadEncerrado(a,b):
    print("Download Encerrado")

def DownloadProgresso(stream,chunk,bytes_faltando):
    bytes_baixados = stream.filesize -bytes_faltando
    porcentagem = round((bytes_baixados/stream.filesize)*100.0,2)
    print('Download em progresso... '+str(porcentagem)+'%')
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)

def BaixarUmVideo(url=None):
    if url == None:
        url = str(input("Insira a url do video: "))

    video = yt(url,on_progress_callback=DownloadProgresso,on_complete_callback=DownloadEncerrado)

    if video.check_availability()==None:
        
        stream = video.streams.filter(progressive=True,file_extension='mp4').order_by('resolution').desc().first()
        
        if stream == None:
            stream = video.streams.filter(progressive=False,file_extension='mp4').order_by('resolution').desc().first()
        print()
        print("-------------------------------------------------------------------")
        print("Baixando o video: ",video.title)
        print("Stream: ",stream)
        try:
            stream.download()
        except:
            videos_error.append(video.title)
    else:
        print("Video indisponível, Erro: ",video.check_availability)

def BaixarMultiplosVideos():
    print("Insira multiplos links, quando encerrar digite 0")
    urlVideo = -1
    listaUrlVideos = list()
    while urlVideo != '0':
        urlVideo = str(input())
        listaUrlVideos.append(urlVideo)
    listaUrlVideos.pop()

    for url in listaUrlVideos:
        BaixarUmVideo(url)
        time.sleep(2)

def BaixarPlaylist():
    playlistLink = input("Insira o link da playlist: ")
    
    ytPlaylist = Playlist(playlistLink)
    for video_url in ytPlaylist.video_urls:
        BaixarUmVideo(video_url)
    
if __name__=='__main__':
    
    print("Insira 1 para baixar apenas um vídeo")
    print("Insira 2 para baixar multíplos vídeos")
    print("Insira 3 para baixar uma playlist do Youtube")
    opcaoMenu = str(input())
    
    if opcaoMenu == '1':
        BaixarUmVideo()
    elif opcaoMenu == '2':
        BaixarMultiplosVideos()
    elif opcaoMenu == '3':
        BaixarPlaylist()
    else:
        print("Você não inseriu uma opção valida")
    
    if videos_error != []:
        print("Os seguintes videos apresentaram erros durante o download")
        for video in videos_error:
            print(video)