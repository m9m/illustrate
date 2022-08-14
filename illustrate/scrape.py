import requests
import asyncio


class ScrapeUtilities:
    def __init__(self, db, settings):
        self.db = db
        self.settings = settings
        self.s = requests.sessions.session()
        self.running = True
        self.coinwatch_api_key = self.settings["coinwatch_api_key"]

    async def operation_dispatcher(self):
        """
        Dispatches and loops each individual function to keep Service information updated
        """
        for default in ["btc_price", "eth_price", "eth_gas", "ens"]:
            await self.db.enter_service_data(default, value="")
        while self.running:
            await self.btc_price_operations()
            await self.eth_price_operations()
            await self.eth_gas_operations()
            await self.ens_operations()
            await asyncio.sleep(self.settings["webhook_update_intervals"])

    async def btc_price_operations(self):
        """
        Updates BTC price
        """
        response = self.s.post(
            "https://api.livecoinwatch.com/coins/single",
            headers={
                "x-api-key": self.coinwatch_api_key,
                "Content-Type": "application/json",
            },
            json={"currency": "USD", "code": "BTC", "meta": False},
        )
        await self.db.update_service_data(
            "btc_price", value=round(response.json()["rate"], 2)
        )

    async def eth_price_operations(self):
        """
        Updates ETH Price
        """
        response = self.s.post(
            "https://api.livecoinwatch.com/coins/single",
            headers={
                "x-api-key": self.coinwatch_api_key,
                "Content-Type": "application/json",
            },
            json={"currency": "USD", "code": "ETH", "meta": False},
        )
        await self.db.update_service_data(
            "eth_price", value=round(response.json()["rate"], 2)
        )

    async def eth_gas_operations(self):
        """
        Updates ETH gas
        """
        response = self.s.get("https://ethgasstation.info/api/ethgasAPI.json").json()
        await self.db.update_service_data(
            "eth_gas",
            value=f"Fast: {response['fastest']/10} gwei ({response['fastestWait']}m)\\n"
            f"Average: {response['average']/10} gwei ({response['avgWait']}m)\\n"
            f"Low: {response['safeLow']/10} gwei ({response['safeLowWait']}m)\\n",
        )

    async def ens_operations(self):
        """
        TODO Add ENS data grabbing
        """
        await self.db.update_service_data("ens", value="Placeholder")
