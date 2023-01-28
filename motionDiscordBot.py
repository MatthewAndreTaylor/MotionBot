import discord
from discord.ext import tasks
import capture
import cv2
import datetime


class MotionBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.firstFrame = capture.npary()
        self.currFrame = None
        self.isDetecting = True
        self.channelId = 1234 # Your chosen channel id (Discord devtools)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        general = self.get_channel(self.channelId)
        await general.send('Just Dropped in the chat')

    async def setup_hook(self):
        self.my_task.start()

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!help'):
            await message.channel.send(
                'Security Bot use `!capture` to get a camera snapshot. Detects differences in room state. Use `!start` to restart the detection and `!stop` to turn off detection')

        if message.content.startswith('!start'):
            self.isDetecting = True
            self.firstFrame = capture.npary()
            await message.channel.send('Restarted detection')

        if message.content.startswith('!stop'):
            self.isDetecting = False
            await message.channel.send('Stopped detection')

        if message.content.startswith('!capture'):
            if self.currFrame is not None:
                cv2.imwrite('/home/matt/Downloads/img.jpg', self.currFrame)
                picture = discord.File('/home/matt/Downloads/img.jpg')
                await message.channel.send(file=picture)

    @tasks.loop(seconds=2) # Delay between captures
    async def my_task(self):
        if not self.isDetecting:
            return

        # Take a capture and compare it to the initial capture
        self.currFrame = capture.npary()
        if capture.isOccupied(self.firstFrame, self.currFrame):
            general = self.get_channel(self.channelId)
            await general.send(
                f'Room is Occupied. Current time: {datetime.datetime.now()}')
            cv2.imwrite('/home/matt/Downloads/img.jpg', self.currFrame)
            picture = discord.File('/home/matt/Downloads/img.jpg')
            await general.send(file=picture)

        # After the comparison set the initial frame to the current frame
        self.firstFrame = self.currFrame

    @my_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()


intents = discord.Intents.default()
intents.message_content = True
client = MotionBot(intents=intents)

try:
    client.run("Token")
except discord.HTTPException as e:
    raise e
