from discord.ui import View, Select, Button
import discord
import time


class SettingsView(View):
    timeout_embed = discord.Embed(
        title="Timeout",
        description="The panel has timed out. Use `/setup` again to display a new instance.",
        color=discord.Color.dark_purple(),
    )

    def __init__(self, db):
        self.db = db
        self.time_delta = time.time()

        # transfer between both visual menu names and the databse urls
        self.webhook_name_to_urls = {}
        self.webhook_urls_to_name = {}

        # links the select menu placeholder text to the database value
        self.db_keys = {
            "Bitcoin Price": "btc_price_webhook",
            "Ethereum Price": "eth_price_webhook",
            "Ethereum Gas": "eth_gas_webhook",
            "ENS Data": "ens_webhook",
        }

        # define the main select menu
        self.tool_select = Select(
            placeholder="Setting",
            options=[
                discord.SelectOption(label="Bitcoin Price"),
                discord.SelectOption(label="Ethereum Price"),
                discord.SelectOption(label="Ethereum Gas"),
                discord.SelectOption(label="ENS Data"),
            ],
            row=0,
        )
        self.tool_select.callback = self.tool_select_callback

        # define the cancel/back button
        self.cancel_button = Button(
            label="Save",
            emoji="↩️",
            style=discord.ButtonStyle.blurple,
            row=1,
            disabled=True,
        )
        self.cancel_button.callback = self.cancel_button_callback

        # defne the enable/disable button
        self.on_off_button = Button(
            label="Disabled",
            emoji="❌",
            style=discord.ButtonStyle.gray,
            row=1,
            disabled=True,
        )
        self.on_off_button.callback = self.on_off_button_callback

        # define the bottom webhook select menu
        self.webhook_select = Select(
            placeholder="#------------",
            options=[discord.SelectOption(label="null")],
            row=2,
            disabled=True,
        )
        self.webhook_select.callback = self.webhook_select_callback

        super().__init__(
            self.tool_select,
            self.cancel_button,
            self.on_off_button,
            self.webhook_select,
        )

    async def _ui_state_one(self):
        """
        Used internally. The default state for the menu.
        """
        self.tool_select.disabled = False
        self.cancel_button.disabled = True
        self.on_off_button.disabled = True
        self.webhook_select.disabled = True
        self.webhook_select.placeholder = "#------------"

    async def _ui_state_two(self, interaction):
        """
        Used internally. The default state for the menu.

        Args:
            interaction (): default paramter from the discord callback
        """
        self.tool_select.disabled = True
        self.cancel_button.disabled = False
        self.on_off_button.disabled = False
        self.webhook_select.disabled = False

        # get all the webhooks in the entire sevrer
        webhooks = await interaction.guild.webhooks()
        for webhook in webhooks:
            self.webhook_name_to_urls[webhook.name] = webhook.url
            self.webhook_urls_to_name[webhook.url] = webhook.name

        # clear select menu options and add all the new webhooks
        self.webhook_select.options = []
        for webhook in webhooks:
            temp_counter = 0
            temp_name = webhook.name
            while temp_name in [option.label for option in self.webhook_select.options]:
                temp_counter += 1
                temp_name = webhook.name + " #" + str(temp_counter)
            self.webhook_select.add_option(label=temp_name)

        # get the row of data from the db containing all data
        # column 1 = id, 2-5 = webhook urls, 6-9 = enabled bool
        db_data = await self.db.retrieve_from_id(interaction.guild_id)
        # link placeholder (selected value) to the corresponding database webhook url
        active_webhook = db_data[
            list(self.db_keys).index(self.tool_select.placeholder) + 1
        ]
        # get the current enabled/disabled value for the corresponding selected value
        button_setting = db_data[
            list(self.db_keys).index(self.tool_select.placeholder) + 5
        ]

        self.webhook_select.placeholder = (
            self.webhook_urls_to_name[active_webhook]
            if active_webhook
            else "#------------"
        )
        if button_setting:
            self.on_off_button.label = "Enabled"
            self.on_off_button.emoji = "✅"
            self.on_off_button.style = discord.ButtonStyle.green
        else:
            self.on_off_button.label = "Disabled"
            self.on_off_button.emoji = "❌"
            self.on_off_button.style = discord.ButtonStyle.gray

    async def _update(self, interaction):
        global timeout_embed
        """
        Used internally. Update the current panel to a new state or update the view in general.

        Args:
            interaction (): default paramter from the discord callback
        """
        if time.time() - self.time_delta > 600:
            self.clear_items()
            await interaction.response.edit_message(view=self, embed=timeout_embed)
            del self
        else:
            await interaction.response.edit_message(view=self)

    async def tool_select_callback(self, interaction):
        """
        Callback function when the main select menu is used.

        Args:
            interaction (): default paramter from the discord callback
        """
        self.tool_select.placeholder = self.tool_select.values[0]
        await self._ui_state_two(interaction)
        await self._update(interaction)

    async def cancel_button_callback(self, interaction):
        """
        Callback function when the cancel/back button is pressed

        Args:
            interaction (): default paramter from the discord callback
        """
        await self._ui_state_one()
        await self._update(interaction)

    async def webhook_select_callback(self, interaction):
        """
        Callback function when the webhook select menu is used

        Args:
            interaction (): default paramter from the discord callback
        """
        value = self.webhook_select.values[0]
        self.webhook_select.placeholder = value
        await self.db.update_information(
            interaction.guild_id,
            self.db_keys[self.tool_select.placeholder],
            self.webhook_name_to_urls[value],
        )
        await self._update(interaction)

    async def on_off_button_callback(self, interaction):
        """
        Callback function when the check / x button is pressed

        Args:
            interaction (): default paramter from the discord callback
        """
        # alternating visual switch with uploading value to db
        if self.on_off_button.label == "Disabled":
            self.on_off_button.label = "Enabled"
            self.on_off_button.emoji = "✅"
            self.on_off_button.style = discord.ButtonStyle.green
            await self.db.update_information(
                interaction.guild_id,
                self.db_keys[self.tool_select.placeholder] + "_enabled",
                True,
            )
        else:
            self.on_off_button.label = "Disabled"
            self.on_off_button.emoji = "❌"
            self.on_off_button.style = discord.ButtonStyle.gray
            await self.db.update_information(
                interaction.guild_id,
                self.db_keys[self.tool_select.placeholder] + "_enabled",
                False,
            )
        await self._update(interaction)
