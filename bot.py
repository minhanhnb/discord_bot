import discord as ds 
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

intents = ds.Intents.default()
intents.message_content = True

client = ds.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot is logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "feedback" in message.content.lower():
        print(f"📩 Found feedback: {message.content}")

        data = {
            "username": str(message.author),
            "channel_discord": str(message.channel),
            "channel": "discord",
            "content": message.content,
            "project_name": message.guild.name if message.guild else "Direct Message",
        }

        try:
            response = requests.post(WEBHOOK_URL, json=data)
            if response.status_code in [200, 204]:
                await message.channel.send(" Feedback received!")
            else:
                await message.channel.send(" Failed to send feedback.")
        except Exception as e:
            print(" Error sending to webhook:", e)

client.run(DISCORD_TOKEN)
