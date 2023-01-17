import discord
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
print(token)
intents = discord.Intents.all()
intents.message_content = True
#luu du lieu kieu nha que :)) xin loi rat nhieu
is_set_role = {}
class myClient(discord.Client):
    # default_channel = myClient.get_channel(1057350032975745085)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = int(os.getenv('DEFAULT'))
        self.ownerSever = int(os.getenv('OWNER'))
        self.Colder = int(os.getenv('COLDER'))
        self.get_role_message = int(os.getenv('ROLEMESS'))
        print(self.default, self.ownerSever, self.Colder, self.get_role_message, type(self.default))
        self.react_to_role = {
            discord.PartialEmoji(name ='0️⃣'): 'Khác',
            discord.PartialEmoji(name='1️⃣'): '2k1',
            discord.PartialEmoji(name='2️⃣'): '2k2',
            discord.PartialEmoji(name='3️⃣'): '2k3',
            discord.PartialEmoji(name='4️⃣'): '2k4'
        }
        print('ok')
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message: discord.Message):
        print(*message.mentions)
        #if bot don't do anything
        if message.author == self.user: return
        #add_reaction:
        emoji = discord.utils.get(message.guild.emojis, name = 'khoc')
        await message.add_reaction(emoji)
        #if start with command
        if message.content.startswith('#hello'):
            await message.reply('Lo con cac')
        #if tag anyone
        for user in self.users:
            if user.mentioned_in(message):
                await message.reply(f'Uhm doi ti {user.name} dang vao')
    
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self.get_role_message: return
        mem = payload.member
        #find the guild the message belongs to
        guild = self.get_guild(payload.guild_id)
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        id = guild.id
        if id not in is_set_role:
            is_set_role[id] = set()
        try:
            role = self.react_to_role[payload.emoji]
        except:
            return
        print(role)
        if role != None:
            if mem in is_set_role[id]:
                await message.remove_reaction(payload.emoji, mem)
                return
            await mem.add_roles(discord.utils.get(guild.roles, name = role))
            is_set_role[id].add(mem)
    async def on_raw_reaction_remove(self, payload):
        pass
    async def on_member_join(self, mem):
        default_channel = self.get_channel(self.default)
        await default_channel.send(f'Chao mung {mem} den voi ao lang, nho chon role o kenh role')

    async def on_member_remove(self, mem):
        default_channel = self.get_channel(self.default)
        await default_channel.send(f'Khong tien ban {mem}, cut')   

client = myClient(intents = intents)
client.run(token)