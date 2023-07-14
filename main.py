import openai
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import cfg
from cfg import WELCOME_MESSAGE, MISTAKE_MESSAGE, BOT_TOKEN, CANCEL_MESSAGE
import telebot
from database_utility import Database
from telebot import types
import sqlite3

c = sqlite3.connect('presents_new.db')

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = cfg.OPENAI_TOKEN

# These lists are for proper error handling
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

    """
    The slice_string function takes a string as input and returns the first sentence of that string.
    The function searches for the first capital letter in the text, then finds the last full stop (period)
    in that same text. It then slices out all characters between those two indices and returns them.

    :param text: Pass in the text to be sliced
    :return: The text between the first capital letter and the last full stop
    """
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
    bot.send_message(message.chat.id, 'Please select the gender:', reply_markup=reply_markup)
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
    The age_group function is the second step in the process of finding a gift.
    It takes as input a message from Telegram and an array of arguments, which are
    the gender and age group selected by the user. It then checks if these values
    are valid (i.e., they exist in our database) and sends back to the user a list
    of possible occasions for which they might want to buy gifts.

    :param message: Get the message sent by the user
    :param args: Pass the arguments from one function to another
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
    The occasion function is the second step in the process of selecting a gift.
    It takes as input a message object and an args tuple, which contains all of the information that has been collected so far.
    The function then checks if /cancel was entered by the user, and if it was, calls cancel(). Otherwise, it tries to add
    the occasion to args[0][0]. If this fails (i.e., because there is no such occasion), error() is called; otherwise present_options()
    is called with message and args as arguments.

    :param message: Get the chat id of the user
    :param args: Pass the list of arguments to the next function
    :param db: Pass the database connection to the next function
    :return: The present_options function
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
        The present_options function is used to present the user with a list of gift options.
        The function takes in a message object, and an arbitrary number of arguments (args).
        It then checks if the text in the message is equal to '/cancel'. If it is, it calls
        cancel(message) which will send a cancellation message back to the user. Otherwise,
        it sorts through all of its arguments and finds out what kind of presents are available for that person.

    :param message: Get the chat id of the user
    :param args: Send a non-keyworded variable-length argument list to the function
    :param db: Access the database
    :return: The list of presents from the database
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
            """
                       The elaborate function is used to elaborate on a gift idea.
                       It takes the call object as an argument and uses it to get the data from database.
                       Then it calls OpenAI API with appropriate parameters, which returns a response object.
                       The response object contains text of elaboration in its choices attribute, which is then sliced
                       into three sentences and sent back to user.

                   :param call: Get the data from the button that was pressed
                   :return: A string, that is a description of the gift
                   """
            # try:
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
            # except Exception as e:
            #     error(message.chat.id)


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
