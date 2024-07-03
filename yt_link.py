from youtube_transcript_api import YouTubeTranscriptApi

video_id = '2e5pQqBvGco&t'

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    for entry in transcript:
        print(entry['text'])

except Exception as e:
    print(f"An error occurred: {e}")
