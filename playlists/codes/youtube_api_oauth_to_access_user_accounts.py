# Youtube Tutorial https://www.youtube.com/watch?v=vQQEaSnQ_bs

import os, pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def privateData():
    client_secrets_path = os.path.abspath("codes/client_secrets.json")
    # token.pickle stores the user's credentials from previously successful logins
    credentials = None
    if os.path.exists("token.pickle"):
        print("Loading Credentials from file...")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
        else:
            print("Fetching New Tokens...")
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json",
                # client_secrets_path,
                scopes=["https://www.googleapis.com/auth/youtube.readonly"],
            )

            flow.run_local_server(
                port=8080, prompt="consent", authorization_prompt_message="Go Authenticate!"
            )
            credentials = flow.credentials

            # Save the credentials for the next run
            with open("token.pickle", "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)

    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.channels().list(
    part="status, contentDetails", mine=True
    )
    response = request.execute()
    up = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    # upload = up[0]
    # up1 = upload['contentDetails']
    # up2 = up1['relatedPlaylists']['uploads']

    request = youtube.playlistItems().list(
        part="status, contentDetails", playlistId=up
    )

    response = request.execute()
    unsorted_private_videos = []
    for item in response["items"]:
        vid_id = item["contentDetails"]["videoId"]
        yt_link = f"https://youtu.be/{vid_id}"
        unsorted_private_videos.append(yt_link)
        print(yt_link)
    
    context = {
        'unsorted_private_videos' : unsorted_private_videos
    }
    return context