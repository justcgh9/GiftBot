import openai
import telebot

bot = telebot.TeleBot('5897120145:AAEgh8bZr72solVQt3p405rUQod9Bz1-HWs')
openai.api_key = "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"

WELCOME_MESSAGE = u'Welcome to the Present Bot!\nThis bot will assist you to chose a present\n' \
                  u'To start use command - /gift\n' \
                  u'To abort use command - /cancel'


# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, WELCOME_MESSAGE)


# GPT-3.5 model parameters
MODEL_NAME = 'text-davinci-003'

# Initial prompt to fine-tune GPT
INITIAL_PROMPT = """You are a gift assistant bot. I can help you choose a gift for someone.
Please provide me with the following information:
1. Gender of the person (male, female, other)
2. Age of the person
3. Interests or hobbies of the person
4. Occasion for the gift

For example:
- Gender: female
- Age: 30
- Interests: cooking, reading
- Occasion: birthday

Once I have the information, I will generate some gift recommendations for you.
"""


# Generate gift recommendations using OpenAI GPT-3.5
def generate_gift_recommendations(input_text):
    response = openai.Completion.create(
        engine=MODEL_NAME,
        prompt=input_text,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()


# Handle Telegram messages
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, INITIAL_PROMPT)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.strip()
    bot.reply_to(message, "Generating gift recommendations...")

    # Split the user input into separate lines for gender, age, interests, and occasion
    lines = user_input.split('\n')
    gender = lines[0].split(': ')[1]
    age = lines[1].split(': ')[1]
    interests = lines[2].split(': ')[1]
    occasion = lines[3].split(': ')[1]

    # Create a prompt using the user's input
    prompt = f"Gender: {gender}\nAge: {age}\nInterests: {interests}\nOccasion: {occasion}"

    # Generate gift recommendations based on the prompt
    recommendations = generate_gift_recommendations(prompt)

    # Send the gift recommendations back to the user
    bot.send_message(message.chat.id, recommendations)


# Start the bot
bot.polling()

