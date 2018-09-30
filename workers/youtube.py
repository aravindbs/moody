import argparse
import yaml

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

with open("../config.yml", "r") as f:
    config = yaml.load(f)

DEVELOPER_KEY = config['YOUTUBE']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q='tamil comedy',
    part='id,snippet',
    maxResults=1
  ).execute()

  videos = []
  channels = []
  playlists = []

  for search_result in search_response.get('items', []):
    #print(search_result)
    #print(search_result['thumbnails']['default']['url'])
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s (%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append('%s (%s)' % (search_result['snippet']['title'],
                                   search_result['id']['channelId']))
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['playlistId']))

  print ('Videos:\n', '\n'.join(videos), '\n')
  print ('Channels:\n', '\n'.join(channels), '\n')
  print ('Playlists:\n', '\n'.join(playlists), '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()


    youtube_search(args)
