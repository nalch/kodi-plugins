![Build status](https://travis-ci.org/nalch/kodi-plugins.svg?branch=master)
# kodi-plugins
Collection of the nalch kodi repository and plugins

## Usage
In order to use the plugins install the repository. Do that by downloading the repository zip in the root folder to your 
machine and selecting it on `My Addons > Install from ZIP`.
After that the plugins can be installed from the repository.  

## Plugins
[FlexiStream](plugin.audio.flexistream/README.md) - A plugin to easily manage a frontend for various audio streams using a config file

## Development
1. Start the development by initializing the environment: `make init`
2. Make your changes
3. Run the tests: `make test`
4. Update the plugin version in `addon.xml`
5. Update the plugin distribution zip and repository description: `make update-addons && make repository`