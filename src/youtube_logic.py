from pytube import YouTube


def get_youtube_title(url):
    youtube = YouTube(url)
    return youtube.title

# TODO transfer youtube transcript related logic here



