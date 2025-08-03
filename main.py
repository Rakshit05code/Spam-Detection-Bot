import os
import discord
import pandas as pd
from discord.ext import commands
import sqlite3
from dotenv import load_dotenv
import pickle

df = pd.read_csv("final_dataset.csv")

load_dotenv()  # loads the .env file
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # your bot token from .env

with open("spam_classifier.pkl", "rb") as f:
    spam_model = pickle.load(f)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Set up (or connect to) a SQLite DB for warnings
conn = sqlite3.connect('warnings.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS warnings (user_id INTEGER PRIMARY KEY, count INTEGER)')
conn.commit()

def check_spam(content):
    """
    Predict if the message content is spam using the loaded ML model.
    Returns True if spam, False otherwise.
    Assumes model predicts 1 for spam, 0 for not spam.
    """
    prediction = spam_model.predict([content])
    print(f"DEBUG spam check: '{content}' => Prediction: {prediction[0]}")
    return prediction[0] == 1

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    c.execute('SELECT count FROM warnings WHERE user_id=?', (member.id,))
    row = c.fetchone()
    count = (row[0] + 1) if row else 1
    c.execute('REPLACE INTO warnings (user_id, count) VALUES (?, ?)', (member.id, count))
    conn.commit()

    await ctx.send(f"{member.mention} warned. Total warnings: {count}")
    if count >= 3:
        await member.kick(reason="Reached 3 warnings!")
        await ctx.send(f"{member.mention} was kicked for reaching three warnings.")

@bot.event
async def on_message(message):
    try:
        if message.author == bot.user or not message.guild:
            return

        print(f"Received message from {message.author}: {message.content}")

        if check_spam(message.content):
            c.execute('SELECT count FROM warnings WHERE user_id=?', (message.author.id,))
            row = c.fetchone()
            count = (row[0] + 1) if row else 1
            c.execute('REPLACE INTO warnings (user_id, count) VALUES (?, ?)', (message.author.id, count))
            conn.commit()

            await message.channel.send(f"{message.author.mention} — please avoid spamming. Warning: {count}/3")
            if count >= 3:
                await message.author.kick(reason="Spam: 3 warnings reached")
                await message.channel.send(f"{message.author.mention} was kicked for spamming.")

        await bot.process_commands(message)
    except Exception as e:
        print(f"Error handling message: {e}")


bot.run(TOKEN)
