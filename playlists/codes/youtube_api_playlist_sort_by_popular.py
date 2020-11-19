from googleapiclient.discovery import build

def sortByPopularity(youtube_link):
    api_key = "AIzaSyATc3O3L9kFH2w1kmKyQK4AbCWQ4_m72UE"
    service = build("youtube", "v3", developerKey=api_key)
    playlist_id = youtube_link.split("list=",1)[1]
    videos = []
    nextPageToken = None


    while True:
        pl_request = service.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken,
        )
        pl_response = pl_request.execute()

        vid_ids = []
        for item in pl_response["items"]:
            vid_ids.append(item["contentDetails"]["videoId"])

        vid_request = service.videos().list(part="statistics", id=",".join(vid_ids))

        vid_response = vid_request.execute()

        for item in vid_response["items"]:
            vid_views = item["statistics"]["viewCount"]
            vid_id = item["id"]
            yt_link = f"https://youtu.be/{vid_id}"

            videos.append({"views": int(vid_views), "url": yt_link})

        nextPageToken = pl_response.get("nextPageToken")
        if not nextPageToken:
            break

    videos.sort(key=lambda sorting: sorting["views"], reverse=True)
    context = {
        "videos": videos
    }
    return context
    
    # for vid in videos:
    #     print(vid["url"], vid["views"])