from cfg import WELCOME_MESSAGE, MISTAKE_MESSAGE, BOT_TOKEN, CANCEL_MESSAGE
import telebot
from database_utility import Database
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """
    The start function is the first function that will be called when a user
    starts interacting with the bot. It sends a welcome message to the user and
    provides them with instructions on how to use it.
    :param message: Get the message object from the user
    :return: The gender function
    """
    bot.send_message(message.chat.id, WELCOME_MESSAGE)


def error(id):
    """
    The error function is called when the user enters an invalid command.
    It sends a message to the user explaining that they have entered an invalid command.

    :param id: Send the message to a specific user
    :return: The message that the user made a mistake
    """
    bot.send_message(id, MISTAKE_MESSAGE)


# Gift command handler
@bot.message_handler(commands=['gift'])
def gift(message):
    """
    The gift function is the first function that gets called when a user starts interacting with the bot.
    It sends a welcome message and asks for gender input from the user. It then calls on gender() to handle
    the next step in this process.

    :param message: Get the message sent by the user
    :return: The gender function
    """
    db = Database()
    reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_markup.add('👩 Female', '👨 Male', '💅 Other')
    bot.send_message(message.chat.id, 'Welcome to the Present Bot!Please select the gender:', reply_markup=reply_markup)
    bot.register_next_step_handler(message, gender, db)


def gender(message, db):
    """
    The gender function is the first step in the process of creating a new user.
    It takes as input a message object and an SQLite database connection, and it
    returns nothing. It prompts the user to select their gender from a list of
    options, then passes that information along with the message object to age_group.

    :param message: Get the message sent by the user
    :param db: Pass the database object to the next function
    :return: The gender of the user
    """
    if message.text == '/cancel':
        cancel(message)
    else:
        try:
            args = [message.text.split()[1]]
            reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            reply_markup.add('👶 0-7', '🧒 7-12', '👧👦 12-18', '🧑 18-27', '👩👨 27-45', '🧓 45+')
            bot.send_message(message.chat.id, 'Please select the age group:', reply_markup=reply_markup)
            bot.register_next_step_handler(message, age_group, args, db=db)
        except Exception as e:
            error(message.chat.id)


def age_group(message, *args, db):
    """
    The age_group function is the second step in the process of selecting a gift.
    It takes as input a message object and an array of arguments, which are passed on to
    the next function. It also takes as input a database connection object, which is used
    to store data about users' preferences for future use.

    :param message: Get the message sent by the user
    :param args: Pass a variable number of arguments to the function
    :param db: Pass the database connection to the function
    :return: The age group of the recipient
    """

    if message.text == '/cancel':
        cancel(message)
    else:
        try:
            args[0].append(message.text.split()[1])
            reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

            a = ['0-7', '7-12', '12-18', '18-27', '27-45', '45+']

            reply_markup.row('🎂 Birthday', '🎄🎅 Christmas')
            if args[0][1] == '0-7':
                if args[0][0] == 'Female':
                    reply_markup.row("💐 Women's day", '🧑‍🎓 Graduation', '🥂 Other')
                elif args[0][0] == 'Male' or 'Other':
                    reply_markup.row('🧑‍🎓 Graduation', '🥂 Other')
            elif args[0][1] in ['7-12', '12-18']:

            if args[0][0] == 'Female':
                reply_markup.row('🎂 Birthday', '🎄🎅 Christmas')
                reply_markup.row("💐 Women's day", '🧑‍🎓 Graduation')
                reply_markup.row('💍 Wedding', '❤ Anniversary', '🥂 Other')
            elif args[0][0] == 'Male':
                reply_markup.row('🎂 Birthday', '🎄🎅 Christmas')
                reply_markup.row('🎖 Defender of the Fatherland day', '🧑‍🎓 Graduation', '🥂 Other')
                reply_markup.row('💍 Wedding', '❤ Anniversary', '🥂 Other')
            elif args[0][0] == 'Other':
                reply_markup.row('🎂 Birthday', '🎄🎅 Christmas', '🧑‍🎓 Graduation')
                reply_markup.row("💐 Women's day", '🎖 Defender of the Fatherland day')
                reply_markup.row('💍 Wedding', '❤ Anniversary', '🥂 Other')
            bot.send_message(message.chat.id, 'Please select the occasion:', reply_markup=reply_markup)
            bot.register_next_step_handler(message, occasion, args, db=db)
        except Exception as e:
            error(message.chat.id)


def occasion(message, *args, db):
    """
    The occasion function is the second step in the process of finding a restaurant.
    It takes as input a message object and an optional list of arguments, which are used to store information about
    the user's preferences. It also takes as input a database connection object, which is used to query the database for
    restaurants that match these preferences. The function first checks if the user has chosen to cancel their search by
    sending /cancel; if so, it calls on cancel() from bot_functions.py and returns None (see documentation for this function).
    If not, it tries appending an occasion type ()

    :param message: Get the chat id of the user
    :param args: Pass a variable number of arguments to a function
    :param db: Pass the database connection to the function
    :return: The present options
    """
    if message.text == '/cancel':
        cancel(message)
    else:
        try:
            text_lst = message.text.split()
            text = ''
            for i in range(1, len(text_lst) - 1):
                text += text_lst[i] + " "
            text += text_lst[-1]
            args[0][0].append(text)
            print(args[0][0])
            reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            reply_markup.add('Cost: Ascending ⬆', 'Cost: Descending ⬇')
            bot.send_message(message.chat.id, 'Please select the sorting order:', reply_markup=reply_markup)
            bot.register_next_step_handler(message, present_options, args, db=db)
        except Exception as e:
            error(message.chat.id)


def present_options(message, *args, db):
    """
    The present_options function is called when the user has selected a sorting option.
    It takes in the message object, which contains information about what was sent to the bot,
    and an arbitrary number of arguments (in this case only one), which are passed from
    the previous function. The first argument is a tuple containing all the parameters that were
    passed into select_query() in db_functions.py.

    :param message: Identify the user
    :param args: Pass a tuple of arguments to the function
    :param db: Pass the database object to the function
    :return: A tuple of three elements:
    """
    if message.text == '/cancel':
        cancel(message)
    else:
        sort_order = message.text[:-2]
        params = (args[0][0][0][0], args[0][0][0][1], args[0][0][0][2])
        db.select_query(sort_order, params)
        bot.send_message(message.chat.id, db.response, reply_markup=types.ReplyKeyboardRemove())
        db.nullify_response()


@bot.message_handler(commands=['cancel'])
def cancel(message):
    """
    The cancel function is used to cancel the current operation and return to the main menu.
    It sends a message with CANCEL_MESSAGE, which is defined in config.py, and removes any keyboard that may be present.

    :param message: Get the chat id of the user who sent a message
    :return: The cancel message
    """
    bot.send_message(message.chat.id, CANCEL_MESSAGE, reply_markup=types.ReplyKeyboardRemove())


def main():
    """
    The main function starts the work of the bot
    :return: It returns nothing
    """
    bot.polling()


if __name__ == '__main__':
    main()
