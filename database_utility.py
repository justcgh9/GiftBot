import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('presents_alt.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS presents (
                        present_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        cost REAL
                    )''')
        self.conn.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS gender (
                                gender_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                gender TEXT
                            )''')
        self.conn.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS age (
                                age_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                age_group_name TEXT
                            )''')
        self.conn.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS occasion (
                                occasion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                occasion_name TEXT
                            )''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS presents_gender (
                                present_id INTEGER,
                                gender_id INTEGER,
                                FOREIGN KEY (present_id) REFERENCES presents(present_id),
                                FOREIGN KEY (gender_id) REFERENCES gender(gender_id),
                                PRIMARY KEY(present_id,gender_id)
                            )''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS presents_age (
                                present_id INTEGER,
                                age_group_id INTEGER,
                                FOREIGN KEY (present_id) REFERENCES presents(present_id),
                                FOREIGN KEY (age_group_id) REFERENCES age(age_group_id),
                                PRIMARY KEY(present_id,age_group_id)
                            )''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS presents_occasion (
                                present_id INTEGER,
                                occasion_id INTEGER,
                                FOREIGN KEY (present_id) REFERENCES presents(present_id),
                                FOREIGN KEY (occasion_id) REFERENCES occasion(occasion_id),
                                PRIMARY KEY(present_id,occasion_id)
                            )''')
        self.conn.commit()
        """
        The __init__ function is called when the class is instantiated.
        It sets up the database connection and creates a table if it doesn't exist.

        :param self: Reference the object itself
        :return: Nothing
        """
        self.conn = sqlite3.connect('presents.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS presents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                cost REAL,
                gender TEXT,
                age_group TEXT,
                occasion TEXT
            )''')
        self.response = ''
        self.conn.commit()

    def initialize_connection(self):

        """
        The initialize_connection function creates a connection to the presents.db database and returns a connection and cursor objects.

        :param self: Represent the instance of the class
        :return: A connection and cursor to the database
        """
        self.conn = sqlite3.connect('presents.db')
        self.cursor = self.conn.cursor()

    def select_query(self, sort_order, params):

        """
        The select_query function works as a query for the database to extract the presents options
        that respond to the following parameters

        :param self: Refer to the object that is calling the function
        :param sort_order: Determine whether the results are sorted in ascending or descending order
        :param params: Pass in the parameters for the query
        :return: A list of tuples that represents bots response to the user
        """
        self.initialize_connection()
        query = "SELECT * FROM presents WHERE gender=? AND age_group=? AND occasion=?"
        if sort_order == 'Cost: Ascending':
            query += " ORDER BY cost ASC"
        else:
            query += " ORDER BY cost DESC"

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        self.response = "Here are some present options:\n\n"
        for row in results:
            print(row)
            self.response += f"Name: {row[1]}\nCost: {row[2]}\n\n"

    def nullify_response(self):
        """
        The nullify_response function sets the response attribute to an empty string.
        This is useful for when you want to clear out a previous response, or if you want
        to make sure that the bot doesn't respond with anything.

        :param self: Represent the instance of the class
        :return: An empty string
        """
        self.response = ''
