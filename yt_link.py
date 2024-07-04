from youtube_transcript_api import YouTubeTranscriptApi
import re

def transcript(link):
    pattern = r'v=([A-Za-z0-9]*)'
    matches = re.findall(pattern, link)
    strings=list()
    if matches:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(matches)

            for entry in transcript:
                strings.append(entry['text'])

            return ' '.join(strings)
        except Exception as e:
            print(f"An error occurred: {e}")
