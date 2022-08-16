"""
Read LICENSE.md for licensing information
"""
import asyncio
import json
import requests

class HookUtilities:
    """
    Post webhook data to webhook urls
    """
    def __init__(self, database, settings):
        self.database = database
        self.running = True
        self.session = requests.sessions.session()
        self.settings = settings
        self.webhook_json_data = settings["webhook_json_data"]
        self.database_keys_reverse = {
            "btc_price": "Bitcoin Price",
            "eth_price": "Ethereum Price",
            "eth_gas": "Ethereum Gas",
            "ens": "ENS Data",
        }

    async def _send(self, data_name, webhook_url):
        """
        Send a data_name value to a specific webhook url

        Args:
            data_name (str): the data_name used as a key value
            channel (str): the webhook url to send the embed to
        """
        value = await self.database.retrieve_service_data(data_name)
        self.session.post(
            webhook_url,
            json=json.loads(
                self.webhook_json_data.replace(
                    "TITLE_VALUE", self.database_keys_reverse[value[0]]
                ).replace("DATA_VALUE", value[1])
            ),
        )

    async def loop(self):
        """
        Create an infinite loop for constantly retrieving and sending data to enabled webhooks
        """
        while self.running:
            enabled_webhooks = await self.database.retrieve_all_enabled_webhooks()
            for hook in enabled_webhooks:
                if hook[1]:
                    await self._send(hook[0], hook[1])
            await asyncio.sleep(self.settings["webhook_update_intervals"])
