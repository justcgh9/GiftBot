import sqlite3


class Database:
    def __init__(self):
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
