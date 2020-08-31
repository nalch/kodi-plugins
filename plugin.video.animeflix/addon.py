import sys
import urllib
import urlparse
import yaml

import xbmcaddon
import xbmcgui
import xbmcplugin


def build_url(query):
    """Compose url from baseurl and the actual query"""
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)


def build_streams():
    """Query streams from the configuration file and settings"""
    addon = xbmcaddon.Addon()
    streams = {}

    ep = "485"
    url_templ = "https://animeflix.io/api/episode?episode_num={}&slug=one-piece"

    for _ in range(10):
        ep_dict = requests.get(url_templ.format(ep)).json()
        title = ep_dict["data"]["current"]["title"]
        thumbnail = ep_dict["data"]["current"]["thumbnail"]
        ep = ep_dict["data"]["next"]["episode_num"]
        ep_id = ep_dict["data"]["current"]["id"]

        url = requests.get("https://animeflix.io/api/videos?episode_id=" + str(ep_id)).json()[0]["file"]
        streams[ep + ". " + title] = {
            "url": url,
            "fanart_image": thumbnail,
        }

    return streams


def guess_stream_type(config):
    """Try to guess the stream type based on the config item"""
    if 'type' in config:
        return config['type']

    if config['url'].endswith('mp3'):
        return 'audio'

    return 'video'


def build_menu(content_type='video'):
    """Build the plugin's menu from the streams"""
    item_list = []

    for title, stream_config in build_streams().items():
        stream_settings = {'url': '', 'fanart_image': ''}
        stream_settings.update(stream_config)
        li = xbmcgui.ListItem(
            label=title,
            thumbnailImage=stream_settings['fanart_image']
        )
        li.setProperty('fanart_image', stream_settings['fanart_image'])
        li.setProperty('IsPlayable', 'true')
        li.setInfo(guess_stream_type(stream_config), {})
        url = build_url({
            'url': stream_settings['url'],
            'mode': 'stream',
            title: title
        })

        item_list.append((url, li, False))

    xbmcplugin.addDirectoryItems(addon_handle, item_list, len(item_list))
    xbmcplugin.setContent(
        addon_handle,
        'songs' if content_type == 'audio' else 'movies'
    )
    xbmcplugin.endOfDirectory(addon_handle)


def play_stream(url):
    """Play a url using Kodi's API"""
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)


def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)
    content_type = args.get('content_type', 'video')

    if mode is None:
        build_menu(content_type)
    elif mode[0] == 'stream':
        play_stream(args['url'][0])


if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    main()
