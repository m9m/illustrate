

# illustrate
_Simplistic & powerful crypto analytics_


https://github.com/m9m/illustrate/assets/95250150/c4e148ed-add8-41e9-9a11-9426dac57d7d

<img width="485" alt="Screen Shot 2022-09-21 at 1 49 49 AM" src="https://user-images.githubusercontent.com/95250150/191434388-64014130-1311-4dcb-ad95-c78945cbba65.png">

## Overview:
the illustrate project is meant to give the tools necessary to paint a picture of the cryptocurrency scene. This involves coin prices, coin history, NFTS, ENS data, and more, all in a graphical representation.

illustrate's flagship discord bot is a minimalistic, open source Discord bot that serves as a customizable engine for server-owners and crypto enthusiasts. illustrate’s UI and setup process is easy to follow, and visually appealing as a personal or public analytics platform. With scaling in mind, the bot comes bundled with a sqlite database wrapper for higher production means, and can support dozens of servers at once. Any webhooks in a server that illustrate has access to can be linked to a type of analytic for an easy-access and plug & play setup.

## Features:
* Bitcoin Price
* Ethereum Price
* ~Ethereum Gas~ (discontinued as of July 2023 due to provider shutdown)
* Edit update interval for all data, which runs asyncronously

## Roadmap:
* ENS Data
* MATIC Data
* Slack Bot
* More mediums for cryptocurrency data

## Installation:
illustrate's Discord bot is available through pypi by the following command

```
pip install illustrate
```

or on some mac/linux distributions

```
pip3 install illustrate
```

## Example:
```python
from illustrate import IllustrateBot, IllustrateCogs
import json

settings = {
    "discord_bot_token": "xxxxx.xxx.xxxx-xxxxx-xxxx", # edit this value
    "webhook_update_intervals": 300, # edit this value
    "coinwatch_api_key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx", # edit this value
    "webhook_json_data": json.dumps({
        "username": "illustrate",
        "embeds": [
            {
                "title": "TITLE_VALUE", 
                "description": "DATA_VALUE",
                "color": 1127128
            }
        ]
    })
}
illustrate_bot = IllustrateBot(settings)
illustrate_bot.add_cog(IllustrateCogs(illustrate_bot))
illustrate_bot.run()
```

### Legal & Third Parties Used
Discord API ([Terms of Service](https://discord.com/terms) | [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy) | [Developer Terms](https://discord.com/developers/docs/policies-and-agreements/terms-of-service))

Live Coin Watch API ([Public API](https://www.livecoinwatch.com/tools/api) | [Terms of Service](https://www.livecoinwatch.com/legal/terms#api))

ETH Gas Station API ([Homepage](https://ethgasstation.info/) | [Parent Project](https://concourseopen.com/))

Py-cord ([Github](https://github.com/Pycord-Development/pycord) | [License](https://github.com/Pycord-Development/pycord/blob/master/LICENSE))

Requests ([Github](https://github.com/psf/requests) | [License](https://github.com/psf/requests/blob/main/LICENSE))

Python and all of its Subsequent Standard Libraries ([Homepage](https://www.python.org/) | [License](https://docs.python.org/3/license.html))




