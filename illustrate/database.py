import sqlite3


class DatabaseUtilities:
    def __init__(self):
        # create re-usable connection object and try to REGISTER tables
        self.db = self._create_connection()
        self._register_tables()

    def _create_connection(self, db_file="./data.db"):
        """
        Creates a db file and a connection object. Usually used internally.

        Args:
            db_file (str): filename

        Returns:
            connection: database object
        """
        self.db = sqlite3.connect(
            db_file,
        )
        return self.db

    def _register_tables(self):
        """
        Creates two default tables. Usually used internally.
        """
        t1 = """CREATE TABLE IF NOT EXISTS GuildSettingsInformation (
                id integer PRIMARY KEY,
                btc_price_webhook VARCHAR(40),
                eth_price_webhook VARCHAR(40),
                eth_gas_webhook VARCHAR(40),
                ens_webhook VARCHAR(40),
                btc_price_webhook_enabled boolean DEFAULT \"FALSE\",
                eth_price_webhook_enabled boolean DEFAULT \"FALSE\",
                eth_gas_webhook_enabled boolean DEFAULT \"FALSE\",
                ens_webhook_enabled boolean DEFAULT \"FALSE\"
                ); """
        t2 = """CREATE TABLE IF NOT EXISTS ServiceData (
                data_name VARCHAR(20) PRIMARY KEY,
                value VARCHAR(200)
                ); """
        c = self.db.cursor()
        c.execute(t1)
        self.db.commit()
        c = self.db.cursor()
        c.execute(t2)
        self.db.commit()

    async def enter_service_data(self, data_name, value):
        """
        INSERTS data rows into the database. Not used for updating or replacing data.

        Args:
            data_name (str): the identifier of the data served as a primary key value.
            value (str, int): value of the entry that goes into column 2 (value)
        """
        sql = f"INSERT INTO ServiceData(data_name,value) VALUES(?,?)"
        cur = self.db.cursor()
        try:
            cur.execute(sql, (data_name, value))
            self.db.commit()
        except sqlite3.IntegrityError:
            # record already exists
            pass

    async def update_service_data(self, data_name, value):
        """
        UPDATE data rows in the database. Used for updating existing data to new values.

        Args:
            data_name (str): the identifier of the data served as a primary key value.
            value (str, int): value of the entry that goes into column 2 (value)
        """
        sql = f"""UPDATE ServiceData
                SET value = ?
                WHERE data_name = ?
                """
        cur = self.db.cursor()
        cur.execute(sql, (value, data_name))
        self.db.commit()

    async def retrieve_service_data(self, data_name):
        """
        GET a value from the database that is assigned to the data name

        Args:
            data_name (str): the identifier of the data served as a primary key value.

        Returns:
            str,int: the data assigned to the data_name primary key
        """
        sql = f"SELECT * FROM ServiceData WHERE data_name=?"
        cur = self.db.cursor()
        cur.execute(sql, (data_name,))
        self.db.commit()
        row = cur.fetchall()
        return row[0]

    async def enter_information(self, user_id, **kwargs):
        """
        INSERTS data rows into the database. Not used for updating or replacing data.

        Args:
            user_id (str): the identifier of the data as a primary key integer.
            **kwargs: key, value pair where the key identifies the column and value becomes the default data stored for the entry
        """
        sql = f"INSERT INTO GuildSettingsInformation(id,{','.join(kwarg[0] for kwarg in kwargs.items())}) VALUES({','.join('?' for _ in range(len(kwargs)+1))})"
        cur = self.db.cursor()
        try:
            cur.execute(sql, [user_id] + [kwarg[1] for kwarg in kwargs.items()])
            self.db.commit()
        except sqlite3.IntegrityError:
            # record already exists
            pass

    async def update_information(self, user_id, key, value):
        """
        UPDATE data rows into the database. Not used for updating or replacing data

        Args:
            user_id (int): the identifier of the data as a primary key integer.
            key (str): the column identifier
            value (str,id): the value to insert where the column and row identify
        """
        sql = f"""UPDATE GuildSettingsInformation
                SET {key} = ?
                WHERE id = ?"""
        cur = self.db.cursor()
        cur.execute(
            sql,
            (
                value,
                user_id,
            ),
        )
        self.db.commit()

    async def retrieve_from_id(self, user_id):
        """
        Retrieve all the row data assigned to a user_id

        Args:
            user_id (int): the identifier of the data as a primary key integer.

        Returns:
            str,int: all data from the row with the param user_id
        """
        sql = f"SELECT * FROM GuildSettingsInformation WHERE id=?"
        cur = self.db.cursor()
        cur.execute(sql, (user_id,))
        self.db.commit()
        row = cur.fetchall()
        return row[0]

    async def _data_grab(self, key, sql):
        """
        Grabs specific webhook urls under conditions and labels it under a key. Not referenced externally.

        Args:
            key (str): the key to label the data under
            sql (str): the sql data to execute

        Returns:
            List[List[key, webhook_url]]: list of key, webhook_url data
        """
        cur = self.db.cursor()
        cur.execute(sql, ())
        self.db.commit()
        rows = cur.fetchall()
        return [[key, row[0]] for row in rows]

    async def retrieve_all_enabled_webhooks(self):
        """
        Retrieves all enabled webhook urls associated with each data type.

        Returns:
            List[List[str,int]]: list of lists containing [data_name, webhook_url]
        """
        data1 = await self._data_grab(
            "btc_price",
            "SELECT btc_price_webhook FROM GuildSettingsInformation WHERE btc_price_webhook_enabled=1",
        )
        data2 = await self._data_grab(
            "eth_price",
            "SELECT eth_price_webhook FROM GuildSettingsInformation WHERE eth_price_webhook_enabled=1",
        )
        data3 = await self._data_grab(
            "eth_gas",
            "SELECT eth_gas_webhook FROM GuildSettingsInformation WHERE eth_gas_webhook_enabled=1",
        )
        data4 = await self._data_grab(
            "ens",
            "SELECT ens_webhook FROM GuildSettingsInformation WHERE ens_webhook_enabled=1",
        )
        return data1 + data2 + data3 + data4
