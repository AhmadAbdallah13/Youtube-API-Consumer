import re
from googleapiclient.discovery import build
from datetime import timedelta


def length(youtube_link):
    api_key = "AIzaSyATc3O3L9kFH2w1kmKyQK4AbCWQ4_m72UE"
    service = build("youtube", "v3", developerKey=api_key)
    hours_pattern = re.compile(r"(\d+)H")
    minutes_pattern = re.compile(r"(\d+)M")
    seconds_pattern = re.compile(r"(\d+)S")

    playlistId = youtube_link.split("list=",1)[1]

    total_seconds = 0

    nextPageToken = None
    while True:
        pl_request = service.playlistItems().list(
            part="contentDetails",
            playlistId=playlistId,
            maxResults=50,
            pageToken=nextPageToken,
        )
        pl_response = pl_request.execute()

        vid_ids = []
        for item in pl_response["items"]:
            vid_ids.append(item["contentDetails"]["videoId"])

        vid_request = service.videos().list(part="contentDetails", id=",".join(vid_ids))

        vid_response = vid_request.execute()

        for item in vid_response["items"]:
            duration = item["contentDetails"]["duration"]

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            vid_seconds = timedelta(
                hours=hours, minutes=minutes, seconds=seconds
            ).total_seconds()

            total_seconds += vid_seconds

        nextPageToken = pl_response.get("nextPageToken")
        if not nextPageToken:
            break

    total_seconds = int(total_seconds)

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    length = {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }
    return length
