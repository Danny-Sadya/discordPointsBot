import discord
import auth_data
import asyncio
import time
from db_executor import DbExecutor
import bot_messages


class DiscordBot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.lock = asyncio.Lock()
        self.db_executor = DbExecutor()
        self.tdict = {}
        self.bot_id = 0

    async def on_ready(self):
        print(f'Logged as {self.user}')
        self.bot_id = self.user.id
        gld = self.guilds[0]
        await gld.text_channels[0].send(bot_messages.messages['init_message'])
        invites = await gld.invites()
        for inv in invites:
            self.db_executor.set_user_invite_code(int(inv.inviter.id), str(inv.code))
            self.db_executor.set_user_invite_code_uses(int(inv.inviter.id), int(inv.uses))

    async def on_member_join(self, member):
        print(f'{member.name} has join the channel')
        self.db_executor.add_id(int(member.id))
        if not self.db_executor.is_user_already_invited(int(member.id)):
            gld = self.guilds[0]
            invite_codes = await gld.invites()
            for invite_code in invite_codes:
                self.db_executor.set_user_invite_code(int(invite_code.inviter.id), str(invite_code.code))
                for inviter_data in self.db_executor.get_invites_data():
                    if not self.db_executor.is_user_already_invited(int(member.id)):
                        if inviter_data[0] == invite_code.code:
                            if int(invite_code.uses) > inviter_data[1]:
                                print(f'{member.name} joined by {invite_code.inviter.name} refferal link')
                                self.db_executor.set_user_invite_code_uses(int(invite_code.inviter.id), int(invite_code.uses))
                                self.db_executor.set_user_status_to_invited(int(member.id))
                                self.db_executor.update_points(int(invite_code.inviter.id), 1)
                    else:
                        break
        else:
            print(f'{member.name} had been earlier invited')

    async def on_message(self, payload):
        if payload.author.id != self.bot_id:
            if payload.content == "/points":
                points = self.db_executor.get_user_points(int(payload.author.id))
                await payload.reply(f'Currently you have {points} points')

            elif payload.content == '/help':
                await payload.reply(bot_messages.messages['/help'])

            elif payload.type.name != 'new_member':
                print(f'Message: {payload.content}')
                self.db_executor.update_points(int(payload.author.id), 0.1)

    async def on_voice_state_update(self, member, before, after):
        author = member.id
        if before.channel is None and after.channel is not None:
            print('Connection to voice chat inited', member, member.id)
            t1 = time.time()
            self.tdict[author] = t1
        elif before.channel is not None and after.channel is None and author in self.tdict:
            t2 = time.time()
            print('Connection to voice chat closed', member, member.id)
            print(t2 - self.tdict[author])
            del self.tdict[author]
            print('Need to update user points')

    async def on_raw_reaction_add(self, payload):
        print('Raw reaction was added')
        self.db_executor.update_points(payload.user_id, 1)


if __name__ == "__main__":
    intent = discord.Intents.default()
    intent.members = True
    bot = DiscordBot(intents=intent)
    bot.run(auth_data.config['token'])
