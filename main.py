import sqlite3
import telebot
from telebot import types

# Database connection
conn = sqlite3.connect('presents.db')
cursor = conn.cursor()

# Constants for conversation states
GENDER, AGE_GROUP, OCCASION, SORT = range(4)

# Bot initialization
bot = telebot.TeleBot('5897120145:AAEgh8bZr72solVQt3p405rUQod9Bz1-HWs')


# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_markup.add('Male', 'Female', 'Other')
    bot.send_message(message.chat.id, 'Welcome to the Present Bot! Please select the gender:', reply_markup=reply_markup)
    bot.register_next_step_handler(message, gender)


# Gender selection handler
def gender(message):
    args = [message.text]
    print(args)
    reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_markup.add('0-12', '12-18', '18-27', '27-45', '45+')
    bot.send_message(message.chat.id, 'Please select the age group:', reply_markup=reply_markup)
    bot.register_next_step_handler(message, age_group, args)


# Age group selection handler
def age_group(message, *args):
    args_new = list(args).append(message.text)
    reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_markup.add('Birthday', 'Anniversary', 'Christmas', 'Other')
    bot.send_message(message.chat.id, 'Please select the occasion:', reply_markup=reply_markup)
    bot.register_next_step_handler(message, occasion, args_new)


# Occasion selection handler
def occasion(message, *args):
    print(args)
    args_new = list(args).append(message.text)
    reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_markup.add('Cost: Ascending', 'Cost: Descending')
    bot.send_message(message.chat.id, 'Please select the sorting order:', reply_markup=reply_markup)
    bot.register_next_step_handler(message, present_options, args_new)


# Present options handler
def present_options(message, *args):
    sort_order = message.text
    args = list(args)
    # Fetch present options from the database based on user selections
    query = "SELECT * FROM presents WHERE gender=? AND age_group=? AND occasion=?"
    params = (args[0], args[1], args[2])
    if sort_order == 'Cost: Ascending':
        query += " ORDER BY cost ASC"
    else:
        query += " ORDER BY cost DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()

    # Generate response message with present options
    response = "Here are some present options:\n\n"
    for row in results:
        response += f"Name: {row[1]}\nCost: {row[2]}\n\n"

    bot.send_message(message.chat.id, response, reply_markup=types.ReplyKeyboardRemove())


# Cancel command handler
@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.chat.id, 'You have canceled the present selection.', reply_markup=types.ReplyKeyboardRemove())


# Main function to start the bot
def main():
    # Create presents table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS presents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gender TEXT,
        age_group TEXT,
        occasion TEXT,
        name TEXT,
        cost REAL
    )''')

    # Insert sample data into the database
    cursor.execute('''
        INSERT INTO presents (gender, age_group, occasion, name, cost)
        VALUES
            ('male', '0-12', 'birthday', 'Toy car', 10.0),
            ('male', '0-12', 'birthday', 'Action figure', 15.0),
            ('female', '0-12', 'birthday', 'Doll', 12.0),
            ('female', '0-12', 'birthday', 'Art set', 20.0),
            ('other', '0-12', 'birthday', 'Board game', 18.0),
            ('male', '12-18', 'graduation', 'Watch', 50.0),
            ('male', '12-18', 'graduation', 'Sports equipment', 40.0),
            ('female', '12-18', 'graduation', 'Jewelry', 60.0),
            ('female', '12-18', 'graduation', 'Perfume', 45.0)
    ''')
    conn.commit()

    bot.polling()


if __name__ == '__main__':
    main()
