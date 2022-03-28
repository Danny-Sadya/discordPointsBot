import discord
from discord.ext import commands

import config
from modules.discord_commands import *
from modules.instagram_commands import *
from modules.twitter_commands import *
from modules.commands import *
from modules.general_commands import *
from modules.messages_handling import *
from modules.db.db_executor import DbExecutor
import json


bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=discord.Intents.all())
tdict = {}
with open('states.json', 'r') as f:
    c_keys = json.load(f).keys()


def set_setup_state_to_false():
    with open('states.json', 'r') as f:
        states = json.load(f)
    states['start_setup'] = False
    with open('states.json', 'w') as f:
        json.dump(states, f, indent=4)


@bot.event
async def on_ready():
    print('Ready')
    print(bot.get_all_members())


@bot.command()
async def start_setup(ctx):
    global db_executor
    await gen_start_setup.start_setup(ctx, bot, db_executor)


@bot.command()
async def server_name(ctx):
    global db_executor
    set_setup_state_to_false()
    await get_server_name.server_name(ctx, bot, db_executor)


@bot.event
async def on_message(message):
    global db_executor
    if not message.author.bot:
        await handle_on_message.on_message(message, db_executor)
        await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    global db_executor
    await handle_on_member_join.on_member_join(member, db_executor)


@bot.event
async def on_voice_state_update(member, before, after):
    global tdict
    global db_executor
    await handle_on_voice_state_update.on_voice_state_update(member, before, after, tdict, db_executor)


@bot.event
async def on_raw_reaction_add(member):
    global db_executor
    await handle_on_raw_reaction_add.on_raw_reaction_add(member, db_executor)


@bot.command()
async def admin_help(ctx):
    if ctx.author.id == config.ADMIN_ID:
        global db_executor
        await command_help.help(ctx)
    else:
        await ctx.reply("You don't have access to this command")


@bot.command()
async def contest_name(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_contest_name.contest_name(ctx, bot, db_executor)


@bot.command()
async def contest_start_date(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_contest_start_date.contest_start_date(ctx, bot, db_executor)


@bot.command()
async def contest_end_date(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_contest_end_date.contest_end_date(ctx, bot, db_executor)


@bot.command()
async def start_contest(ctx):
    global db_executor
    await contest_start_contest.start_contest(ctx, bot, db_executor)


@bot.command()
async def end_contest(ctx):
    global db_executor
    await contest_end_contest.end_contest(ctx, bot, db_executor)


@bot.command()
async def pause_contest(ctx):
    global db_executor
    await contest_pause_contest.pause_contest(ctx, bot, db_executor)


# @bot.command()
# async def registration(ctx, command=None):
#         global db_executor
#         await command_registration.registration(ctx, command, db_executor, bot)


@bot.command()
async def registration_active(ctx):
    global db_executor
    await contest_registration_acive.registration_active(ctx, bot, db_executor)


@bot.command()
async def registration_ended(ctx):
    global db_executor
    await contest_registration_ended.registration_ended(ctx, bot, db_executor)


@bot.command()
async def reset_scores(ctx):
    global db_executor
    await com_reset_scores.reset_scores(ctx, bot, db_executor)


@bot.command()
async def check_score(ctx):
    global db_executor
    await com_check_score.check_score(ctx, bot, db_executor)


@bot.command()
async def give_points(ctx):
    global db_executor
    await com_give_points.give_points(ctx, bot, db_executor)


@bot.command()
async def transfer_points(ctx):
    global db_executor
    await com_transfer_points.transfer_points(ctx, bot, db_executor)


@bot.command()
async def point_name(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_point_name.point_name(ctx, bot, db_executor)


@bot.command()
async def all_scores(ctx):
    global db_executor
    await com_all_scores.all_scores(ctx, bot, db_executor)


@bot.command()
async def leader_board(ctx):
    global db_executor
    await com_leader_board.leader_board(ctx, db_executor)


@bot.command()
async def top_ten(ctx):
    global db_executor
    await com_top_ten.top_ten(ctx, db_executor)


@bot.command()
async def select_winner(ctx):
        global db_executor
        await com_select_winner.select_winner(ctx, bot, db_executor)


@bot.command()
async def setup_instagram(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_setup_instagram.setup_instagram(ctx, bot, db_executor)


@bot.command()
async def setup_instagram_hashtag(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_setup_instagram_hashtag.setup_instagram_hashtag(ctx, bot, db_executor)


@bot.command()
async def setup_twitter(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_setup_twitter.setup_twitter(ctx, bot, db_executor)


@bot.command()
async def setup_twitter_hashtag(ctx):
    global db_executor
    set_setup_state_to_false()
    await gen_setup_twitter_hashtag.setup_twitter_hashtag(ctx, bot, db_executor)


@bot.command()
async def resetstatistics(ctx):
    global db_executor
    await command_resetstatistics.resetstatistics(ctx, db_executor)


@bot.command()
async def discord_score_invite(ctx):
    global db_executor
    await cdiscord_score_invite.score_invite(ctx, bot, db_executor)


@bot.command()
async def discord_score_react(ctx):
    global db_executor
    await cdiscord_score_react.score_react(ctx, bot, db_executor)


@bot.command()
async def discord_score_sent_message(ctx):
    global db_executor
    await cdiscord_score_sent_message.score_sent_message(ctx, bot, db_executor)


@bot.command()
async def discord_score_time(ctx):
    global db_executor
    await cdiscord_score_time.score_time(ctx, bot, db_executor)


@bot.command()
async def instagram_score_hashtag(ctx):
    global db_executor
    await cinstagram_score_hashtag.score_instagram_hashtag(ctx, bot, db_executor)


@bot.command()
async def instagram_score_follow(ctx):
    global db_executor
    await cinstagram_score_follow.score_instagram_follow(ctx, bot, db_executor)


@bot.command()
async def instagram_score_comment(ctx):
    global db_executor
    await cinstagram_score_comment.score_instagram_comment(ctx, bot, db_executor)


@bot.command()
async def instagram_score_like(ctx):
    global db_executor
    await cinstagram_score_like.score_instagram_like(ctx, bot, db_executor)


@bot.command()
async def twitter_score_hashtag(ctx):
    global db_executor
    await ctwitter_score_hashtag.score_twitter_hashtag(ctx, bot, db_executor)


@bot.command()
async def twitter_score_quote_tweet(ctx):
    global db_executor
    await ctwitter_score_quote_tweet.score_twitter_quote_tweet(ctx, bot, db_executor)


@bot.command()
async def twitter_score_retweet(ctx):
    global db_executor
    await ctwitter_score_retweet.score_twitter_retweet(ctx, bot, db_executor)


@bot.command()
async def twitter_score_twit_tagged(ctx):
    global db_executor
    await ctwitter_score_twit_tagged.score_twitter_twit_tagged(ctx, bot, db_executor)


@bot.command()
async def twitter_score_tweet_like(ctx):
    global db_executor
    await ctwitter_score_tweet_like.score_twitter_tweet_like(ctx, bot, db_executor)


@bot.command()
async def twitter_score_follow(ctx):
    global db_executor
    await ctwitter_score_twit_follow.score_twit_follow(ctx, bot, db_executor)


db_executor = DbExecutor()
bot.run(config.BOT_TOKEN)
