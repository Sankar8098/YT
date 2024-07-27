import yt_dlp


def get_video_info(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_info = {
                'title': info_dict.get('title', None),
                'description': info_dict.get('description', None),
                'duration': info_dict.get('duration', None),
                'view_count': info_dict.get('view_count', None),
                'like_count': info_dict.get('like_count', None),
                'dislike_count': info_dict.get('dislike_count', None),
                'upload_date': info_dict.get('upload_date', None),
                'uploader': info_dict.get('uploader', None),
                'channel_id': info_dict.get('channel_id', None),
                'channel_url': info_dict.get('channel_url', None),
                'tags': info_dict.get('tags', None),
                'thumbnail': info_dict.get('thumbnail', None),
                'video_url': info_dict.get('webpage_url', None),
                'formats': info_dict.get('formats', [])
            }
            return video_info
    except Exception as e:
        print(f"Error: {e}")
        return None
