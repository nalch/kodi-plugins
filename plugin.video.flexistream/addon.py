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
    streams = []

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


def build_menu():
    """Build the plugin's menu from the streams"""
    song_list = []

    for title, stream_config in build_streams().items():
        stream_settings = {'url': '', 'fanart_image': ''}
        stream_settings.update(stream_config)
        li = xbmcgui.ListItem(
            label=title,
            thumbnailImage=stream_settings['fanart_image']
        )
        li.setProperty('fanart_image', stream_settings['fanart_image'])
        li.setProperty('IsPlayable', 'true')
        url = build_url({
            'url': stream_settings['url'],
            'mode': 'stream',
            title: title
        })

        song_list.append((url, li, False))

    xbmcplugin.addDirectoryItems(addon_handle, song_list, len(song_list))
    xbmcplugin.setContent(addon_handle, 'songs')
    xbmcplugin.endOfDirectory(addon_handle)


def play_stream(url):
    """Play a url using Kodi's API"""
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)


def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)

    if mode is None:
        build_menu()
    elif mode[0] == 'stream':
        play_stream(args['url'][0])


if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    main()
