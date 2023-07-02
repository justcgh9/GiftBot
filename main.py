import sqlite3
import telebot
from telebot import types
# This is my program
# Database connection
conn = sqlite3.connect('presents.db')
cursor = conn.cursor()

# Constants for conversation states
GENDER, AGE_GROUP, OCCASION, SORT = range(4)

# Bot initialization
bot = telebot.TeleBot('5897120145:AAEgh8bZr72solVQt3p405rUQod9Bz1-HWs')

WELCOME_MESSAGE = u'Welcome to the Gift Assistant Bot! 🎁\nThis bot will help you to choose a present for your ' \
                  u'relatives and friends. Based on person characteristics, such as age, gender, interests, ' \
                  u'and occasion information it will select the most appropriate gift options.\n' \ 
                  u'✔ To start, use command - /gift\n' \
                  u'✖ To interrupt, use the command - /cancel'


MISTAKE_MESSAGE = u'error 404, start again\n'\
                  u'To start use command - /gift\n' \
                  u'To abort use command - /cancel'


# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, WELCOME_MESSAGE)


def error(id):
    bot.send_message(id, MISTAKE_MESSAGE)


# Gift command handler
@bot.message_handler(commands=['gift'])
def gift(message):
    reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_markup.add('👩 Female', '👨 Male', 'Other')
    bot.send_message(message.chat.id, 'Welcome to the Present Bot! Please select the gender:', reply_markup=reply_markup)
    bot.register_next_step_handler(message, gender)


# Gender selection handler
def gender(message):
    if message.text == '/cancel':
        cancel(message)
    else:
        try:
            args = [(message.text).split()[1]]
            reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            reply_markup.add('👶 0-7', '🧒 7-12', '👧👦 12-18', '🧑 18-27', '👩👨 27-45', '🧓 45+')
            bot.send_message(message.chat.id, 'Please select the age group:', reply_markup=reply_markup)
            bot.register_next_step_handler(message, age_group, args)
        except Exception as e:
            error(message.chat.id)


# Age group selection handler
def age_group(message, *args):
    if message.text == '/cancel':
        cancel(message)
    else:
        try:
            args[0].append((message.text).split()[1])
            reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            reply_markup.row('🎂 Birthday', '🎄🎅 Christmas', '🧑‍🎓 Graduation')
            reply_markup.row("💐 Women's day", '🎖 Defender of the Fatherland day')
            reply_markup.row('💍 Wedding', '❤ Anniversary', '🥂 Other')
            bot.send_message(message.chat.id, 'Please select the occasion:', reply_markup=reply_markup)
            bot.register_next_step_handler(message, occasion, args)
        except Exception as e:
            error(message.chat.id)


# Occasion selection handler
def occasion(message, *args):
    if message.text == '/cancel':
        cancel(message)
    else:
        try:
            args[0][0].append((message.text).split()[1])
            reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            reply_markup.add('Cost: Ascending⬆', 'Cost: Descending⬇')
            bot.send_message(message.chat.id, 'Please select the sorting order:', reply_markup=reply_markup)
            bot.register_next_step_handler(message, present_options, args)
        except Exception as e:
            error(message.chat.id)


# Present options handler
def present_options(message, *args):
    if message.text == '/cancel':
        cancel(message)
    else:
        try:
            conn = sqlite3.connect('presents.db')
            cursor = conn.cursor()
            sort_order = message.text[:-1]
            # Fetch present options from the database based on user selections
            query = "SELECT * FROM presents WHERE gender=? AND age_group=? AND occasion=?"
            params = (args[0][0][0][0], args[0][0][0][1], args[0][0][0][2])
            if sort_order == 'Cost: Ascending':
                query += " ORDER BY cost ASC"
            else:
                query += " ORDER BY cost DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()
            # Generate response message with present options
            response = "Here are some present options:\n\n"
            for row in results:
                print(row)
                response += f"Name: {row[4]}\nCost: {row[6]}\n\n"

            bot.send_message(message.chat.id, response, reply_markup=types.ReplyKeyboardRemove())
        except Exception as e:
            error(message.chat.id)


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

    conn.commit()
    bot.polling()


if __name__ == '__main__':
    main()
