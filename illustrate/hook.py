import requests
import json
import asyncio


class HookUtilities:
    def __init__(self, db, settings):
        self.db = db
        self.running = True
        self.s = requests.sessions.session()
        self.settings = settings
        self.webhook_json_data = settings["webhook_json_data"]
        self.db_keys_reverse = {
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
        value = await self.db.retrieve_service_data(data_name)
        self.s.post(
            webhook_url,
            json=json.loads(
                self.webhook_json_data.replace(
                    "TITLE_VALUE", self.db_keys_reverse[value[0]]
                ).replace("DATA_VALUE", value[1])
            ),
        )

    async def loop(self):
        """
        Create an infinite loop for constantly retrieving and sending data to enabled webhooks
        """
        while self.running:
            enabled_webhooks = await self.db.retrieve_all_enabled_webhooks()
            for hook in enabled_webhooks:
                if hook[1]:
                    await self._send(hook[0], hook[1])
            await asyncio.sleep(self.settings["webhook_update_intervals"])
