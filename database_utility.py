import sqlite3
from cfg import MISTAKE_MESSAGE

age_groups = {
    '0-7': 1,
    '7-12': 2,
    '12-18': 3,
    '18-27': 4,
    '27-45': 5,
    '45+': 6
}
genders = {
    'Male': 2,
    'Female': 1,
    'Other': 3
}
occasions = {
    'Birthday': 1,
    'Christmas': 2,
    'Graduation': 3,
    "Women's day": 4,
    'Defender of the Fatherland day': 5,
    'Wedding': 6,
    'Anniversary': 7,
    'Other': 8
}


class Database:
    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the database connection and creates a table if it doesn't exist.

        :param self: Reference the object itself
        :return: Nothing
        """
        self.conn = sqlite3.connect('presents_new.db')
        self.cursor = self.conn.cursor()
        self.response = ''
        self.age = None
        self.gender = None
        self.occasion = None

    def initialize_connection(self):

        """
        The initialize_connection function creates a connection to the presents.db database and returns a connection and cursor objects.

        :param self: Represent the instance of the class
        :return: A connection and cursor to the database
        """
        self.conn = sqlite3.connect('presents_new.db')
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
        self.gender = params[0]
        self.age = params[1]
        self.occasion = params[2]
        gender_id = genders[params[0]]
        age_group_id = age_groups[params[1]]
        occasion_id = occasions[params[2]]
        query = f"SELECT present_id FROM presents_gender WHERE gender_id={gender_id}"
        self.cursor.execute(query)
        results_gender = self.cursor.fetchall()
        query = f"SELECT present_id FROM presents_age WHERE age_group_id={age_group_id}"
        self.cursor.execute(query)
        results_age = self.cursor.fetchall()
        query = f"SELECT present_id FROM presents_occasion WHERE occasion_id={occasion_id}"
        self.cursor.execute(query)
        results_occasion = self.cursor.fetchall()
        results = list(set(results_occasion) & set(results_gender) & set(results_age))
        self.response = "Here are some present options:\n\n"
        answers = {}
        presents = []
        for result in results:
            query = f"SELECT name,cost FROM presents WHERE present_id={result[0]}"
            self.cursor.execute(query)
            final_results_iter = self.cursor.fetchall()
            answers[final_results_iter[0][0]] = final_results_iter[0][1]
        if sort_order == 'Cost: Ascending':
            for key, value in sorted(answers.items(), key=lambda x: x[1]):
                self.response += key + " " + str(int(value)) + "\n\n"
                presents.append([key, value])
            return presents
        elif sort_order == 'Cost: Descending':
            for key, value in sorted(answers.items(), key=lambda x: x[1], reverse=True):
                self.response += key + " " + str(int(value)) + "\n\n"
                presents.append([key, value])
            return presents
        else:
            self.response = MISTAKE_MESSAGE
            return None

    def nullify_response(self):
        """
        The nullify_response function sets the response attribute to an empty string.
        This is useful for when you want to clear out a previous response, or if you want
        to make sure that the bot doesn't respond with anything.

        :param self: Represent the instance of the class
        :return: An empty string
        """
        self.response = ''
        self.age = None
        self.gender = None
        self.occasion = None