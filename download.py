from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.query import Stream
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_video_info(url):
    yt = YouTube(url)
    formats = yt.streams.filter(type="video", mime_type="video/mp4", progressive=True).order_by('resolution')
    formats = list({format_.resolution: format_ for format_ in formats}.values())
    return {
        'title': yt.title,
        'uploader': yt.author,
        'channel_url': yt.channel_url,
        'thumbnail': yt.thumbnail_url,
        'subtitles': yt.captions,
        'formats': formats
    }


if __name__ == '__main__':
    get_info = get_video_info("https://youtu.be/bPjIeKmvY4A?si=jjiUamTzMwMPnkga")
    for format_ in get_info['formats']:
        print(format_)

