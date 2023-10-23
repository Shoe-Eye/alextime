from pytube import YouTube


video_list = [
    # "https://www.youtube.com/watch?v=n-d2bXjelfs",
    # "https://www.youtube.com/watch?v=rz5Wa_duvo8",
    # "https://www.youtube.com/watch?v=bfn16TDAOgk",
    # "https://www.youtube.com/watch?v=IGNDwRXD0r0",
    # "https://www.youtube.com/watch?v=4OQyj-c7ld4",
    # "https://www.youtube.com/watch?v=lQgeNrc0RWI",
    # "https://www.youtube.com/watch?v=0PUTmln7LwU",
    # "https://www.youtube.com/watch?v=5JXH3g259pQ",
    # "https://www.youtube.com/watch?v=HGfHqEfBUJE",
    # "https://www.youtube.com/watch?v=L04HO58wtYg",
    # "https://www.youtube.com/watch?v=rGnL7DIVxi4",
    # "https://www.youtube.com/watch?v=AC5dRsBHQrs",
    # "https://www.youtube.com/watch?v=K3MDlTpa3Vo",
    # "https://www.youtube.com/watch?v=psPX7jsP_CA",
    # "https://www.youtube.com/watch?v=P4fQecH-bmc",
    # "https://www.youtube.com/watch?v=F-DA-ErBXo4",
    # "https://www.youtube.com/watch?v=A6KLJ45fiRY",
    # "https://www.youtube.com/watch?v=gSm_bJOZtlo",
    # "https://www.youtube.com/watch?v=P6CHf4cUVJY",
    # "https://www.youtube.com/watch?v=sEnj6mBw2Qo",
    # "https://www.youtube.com/watch?v=8Vh_sFwh3tg",
    # "https://www.youtube.com/watch?v=4mixQgUqVYE",
    # "https://www.youtube.com/watch?v=aV_ywFlcRpE",
    # "https://www.youtube.com/watch?v=G7Mf7rnZAVg",
    # "https://www.youtube.com/watch?v=uPbS6F2wgAQ",
]


def download_youtube_video(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


for video in video_list:
    download_youtube_video(video)
