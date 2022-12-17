

# illustrate
_Simplistic & powerful crypto analytics through Discord_

<img width="485" alt="Screen Shot 2022-09-21 at 1 49 49 AM" src="https://user-images.githubusercontent.com/95250150/191434388-64014130-1311-4dcb-ad95-c78945cbba65.png">

## Overview:
illustrate is a minimalistic, open source Discord bot that serves as a customizable front-end for server-owners and crypto enthusiasts. illustrate’s UI and setup process is easy to follow, and visually appealing as a personal or public analytics platform. With availability in mind, the bot comes bundled with a sqlite database wrapper for higher production means, and can support dozens of servers at once.

## Features:
* Bitcoin Price
* Ethereum Price
* EThereum Gas

## Roadmap:
* ENS Data
* MATIC Data

## Installation:
illustrate is available through pypi by the following command

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
    "discord_bot_token": "xxxxx.xxx.xxxx-xxxxx-xxxx",
    "webhook_update_intervals": 300,
    "coinwatch_api_key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx",
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

### Third Party Services
Discord API ([Terms of Service](https://discord.com/terms) | [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy) | [Developer Terms](https://discord.com/developers/docs/policies-and-agreements/terms-of-service))

Live Coin Watch API ([Public API](https://www.livecoinwatch.com/tools/api) | [Terms of Service](https://www.livecoinwatch.com/legal/terms#api))

ETH Gas Station API ([Homepage](https://ethgasstation.info/) | [Parent Project](https://concourseopen.com/))

### Linked Libraries
Py-cord ([Github](https://github.com/Pycord-Development/pycord) | [License](https://github.com/Pycord-Development/pycord/blob/master/LICENSE))

Requests ([Github](https://github.com/psf/requests) | [License](https://github.com/psf/requests/blob/main/LICENSE))

Python and all of its Subsequent Standard Libraries ([Homepage](https://www.python.org/) | [License](https://docs.python.org/3/license.html))




