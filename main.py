import openai
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import cfg
from cfg import WELCOME_MESSAGE, MISTAKE_MESSAGE, BOT_TOKEN, CANCEL_MESSAGE
import telebot
from database_utility import Database
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = cfg.OPENAI_TOKEN

age_groups = [
    '0-7',
    '7-12',
    '12-18',
    '18-27',
    '27-45',
    '45+'
]
genders = [
    'Male',
    'Female',
    'Other'
]
occasions = [
    'Birthday',
    'Christmas',
    'Graduation',
    "Women's day",
    'Defender of the Fatherland day',
    'Wedding',
    'Anniversary',
    'Other'
]




def slice_string(text):
    match = re.search('[A-Z]', text)  # Find the first capital letter
    if match:
        start_index = match.start()  # Get the index of the first capital letter
        end_index = text.rfind('.')  # Find the index of the last full stop

        if end_index > start_index:
            sliced_text = text[start_index:end_index]  # Slice the text
            return sliced_text

    return None


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
    db.nullify_response()
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
            if message.text.split()[1] not in genders:
                raise ValueError
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
            if args[0][1] not in age_groups:
                raise ValueError
            if args[0][1] == '0-7':
                reply_markup.row('🎂 Birthday', '🎄🎅 Christmas')
                if args[0][0] == 'Female':
                    reply_markup.row("💐 Women's day", '🧑‍🎓 Graduation', '🥂 Other')
                elif args[0][0] == 'Male' or 'Other':
                    reply_markup.row('🧑‍🎓 Graduation', '🥂 Other')
                else:
                    error(message.chat.id)
            elif args[0][1] in ['7-12', '12-18']:
                reply_markup.row('🎂 Birthday', '🎄🎅 Christmas')
                if args[0][0] == 'Female':
                    reply_markup.row("💐 Women's day", '🧑‍🎓 Graduation')
                    reply_markup.row('❤ Anniversary', '🥂 Other')
                elif args[0][0] == 'Male':
                    reply_markup.row('🎖 Defender of the Fatherland day', '🧑‍🎓 Graduation')
                    reply_markup.row('❤ Anniversary', '🥂 Other')
                elif args[0][0] == 'Other':
                    reply_markup.row("💐 Women's day", '🎖 Defender of the Fatherland day')
                    reply_markup.row('🧑‍🎓 Graduation', '❤ Anniversary', '🥂 Other')
                else:
                    error(message.chat.id)
            elif args[0][1] in ['18-27', '27-45', '45+']:
                if args[0][0] == "Female":
                    reply_markup.row('🎂 Birthday', '🎄🎅 Christmas')
                    reply_markup.row("💐 Women's day", '🧑‍🎓 Graduation')
                    reply_markup.row('💍 Wedding', '❤ Anniversary', '🥂 Other')
                elif args[0][0] == "Male":
                    reply_markup.row('🎂 Birthday', '🎄🎅 Christmas')
                    reply_markup.row('🧑‍🎓 Graduation', '🎖 Defender of the Fatherland day')
                    reply_markup.row('💍 Wedding', '❤ Anniversary', '🥂 Other')
                elif args[0][0] == 'Other':
                    reply_markup.row('🎂 Birthday', '🎄🎅 Christmas', '🧑‍🎓 Graduation')
                    reply_markup.row("💐 Women's day", '🎖 Defender of the Fatherland day')
                    reply_markup.row('💍 Wedding', '❤ Anniversary', '🥂 Other')
                else:
                    error(message.chat.id)
            else:
                error(message.chat.id)

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
            if text not in occasions:
                raise ValueError
            args[0][0].append(text)
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
        presents = db.select_query(sort_order, params)
        print(presents)
        reply_markup = InlineKeyboardMarkup(row_width=1)
        for present, cost in presents:
            reply_markup.add(InlineKeyboardButton(present + " " + str(cost) + "₽", callback_data=present))
        resp = 'Here are some presents options.\nFor additional info click on the option you want'
        bot.send_message(message.chat.id, resp, reply_markup=reply_markup)

        @bot.callback_query_handler(func=lambda call: True)
        def elaborate(call):
            try:
                input_text = f'You are a Gifts assistant bot, that can help One ' \
                             f'by describing a gift Idea in details. You should describe {call.data} and' \
                             f'how it suits a person of gender {db.gender} and age {db.age} for {db.occasion}. ' \
                             f'You should do it in three sentences. Mention key details of {call.data}, then ' \
                             f'mention how it suits ' \
                             f'this particular person. And in last sentence mention why it is good for {db.occasion}'
                print(input_text)
                response = openai.Completion.create(
                    engine=cfg.MODEL_NAME,
                    prompt=input_text,
                    max_tokens=200,
                    n=1,
                    stop=None,
                    temperature=1.0,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                print(presents)
                bot.send_message(message.chat.id, slice_string(response.choices[0].text.strip()))
            except Exception as e:
                error(message.chat.id)


@bot.message_handler(commands=['cancel'])
def cancel(message):
    """
    The cancel function is used to cancel the current operation and return to the main menu.
    It sends a message with CANCEL_MESSAGE, which is defined in config.py, and removes any keyboard that may be present.

    :param message: Get the chat id of the user who sent a message
    :return: The cancel message
    """
    bot.send_message(message.chat.id, CANCEL_MESSAGE, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    error(message.chat.id)


def main():
    """
    The main function starts the work of the bot
    :return: It returns nothing
    """
    bot.polling()


if __name__ == '__main__':
    main()
