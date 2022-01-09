import sys
import yaml
from urllib.parse import parse_qs, urlencode

import xbmcaddon
import xbmcgui
import xbmcplugin


def build_url(query):
    """Compose url from baseurl and the actual query"""
    base_url = sys.argv[0]
    return base_url + '?' + urlencode(query)


def build_streams():
    """Query streams from the configuration file and settings"""
    addon = xbmcaddon.Addon()
    streams = {}

    config_path = addon.getSetting('stream_config')
    if config_path:
        with open(config_path, 'r') as config_file:
            try:
                streams = yaml.safe_load(config_file)['streams']
            except KeyError:
                raise ValueError(
                    'Config file should have a root key called "streams"'
                )
    return streams


def guess_stream_type(config):
    """Try to guess the stream type based on the config item"""
    if 'type' in config:
        return config['type']

    if config['url'].endswith('mp3'):
        return 'audio'

    return 'video'


def build_menu(content_type='audio'):
    """Build the plugin's menu from the streams"""
    item_list = []

    for title, stream_config in build_streams().items():
        stream_type = guess_stream_type(stream_config)
        if stream_type != content_type:
            continue

        stream_settings = {'url': '', 'fanart_image': ''}
        stream_settings.update(stream_config)
        li = xbmcgui.ListItem(
            label=title,
            thumbnailImage=stream_settings['fanart_image']
        )
        li.setProperty('fanart_image', stream_settings['fanart_image'])
        li.setProperty('IsPlayable', 'true')
        li.setInfo(stream_type, {})
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
    args = parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)
    content_type = args.get('content_type', 'audio')

    if mode is None:
        build_menu(content_type)
    elif mode[0] == 'stream':
        play_stream(args['url'][0])


if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    main()
