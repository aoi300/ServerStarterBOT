from asyncio import tasks
import subprocess
# インストールした discord.py を読み込む
import discord
import asyncio
import os
import sys
import time
import mcstatus
from mcstatus import JavaServer

#presence用
idle = discord.Game("サーバー停止中")
starting = discord.Game("サーバー起動中")


server1 = JavaServer.lookup("自分のIP")
try:
    status = server1.status()
    print("サーバーオンライン")
except:
    print("サーバーオフライン")

os.chdir('C:\spigot')

# TOKENとサーバーの情報
TOKEN = 'DISCORDトークン'
f_name = 'JAVAの名前 ○○.jar'
maxMemory = '10G'  # 任意の最大メモリ割り当てサイズ
minMemory = '10G'  # 任意の最小メモリ割り当てサイズ

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content=True
client = discord.Client(intents=intents)

# サーバー操作用
class server_process:

    def __init__(self, f_name, maxMemory,minMemory):
        self.server = None
        self.command = ["java", "-server",f'-Xms{minMemory}', f'-Xmx{maxMemory}', "-jar", f_name, "nogui"]

    def start(self):
        self.server = subprocess.Popen(self.command, stdin=subprocess.PIPE)

    def stop(self):
        input_string = "stop"
        self.server.communicate(input_string.encode())

    def kill(self):
        self.server.terminate()

    def server_is_running(self):
        if self.server is None: return False
        if self.server.poll() is None:
            return True
        elif self.server.poll() is not None:
            return False
        else:
            return False

    def server_is_None(self):
        if self.server is None:
            return True
        else:
            return False

    def get(self):
        return self.server.poll()

# サーバー操作用
server = server_process(f_name, maxMemory, minMemory)

#活動監視
@tasks.loop(seconds=1)
async def server_checker():
    while (True):
        if server.server_is_running() is True:
            await client.change_presence(activity=starting, status=discord.Status.online)
        else:
            await client.change_presence(activity=idle, status=discord.Status.idle)
        await asyncio.sleep(1)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print(client.user.name)
    print(client.user.id)
    server_checker.start()
    #client.loop.create_task(server_checker())
    #await client.change_presence(activity=idle, status=discord.Status.idle)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    if message.author.bot:
        return

    global server

    print(f"In Channel {message.channel}:\n{message.author.name} ({message.author}) wrote: {message.content}")
    global server

    if message.content == 'r.start':
        if server.server_is_running() is False:
            await message.channel.send('サーバー起動します...')
            server.start()
        else:
            await message.channel.send('既に起動中です')
    elif message.content == "r.kill": # 緊急停止用
        if server.server_is_None() is True:
            await message.channel.send('サーバープロセスが存在しません')
        else:
            emoji_o = '🇴'
            kill_ms = await message.channel.send('強制終了しますか？')
            await kill_ms.add_reaction(emoji_o)

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '🇴'

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await kill_ms.edit(content='処理がタイムアウトしました')
            else:
                await kill_ms.edit(content='強制終了しました')
                server.kill()
            await kill_ms.clear_reactions()

    elif message.content == 'r.stop': # 通常停止用
        if server.server_is_running() is True:
            await message.channel.send('終了します')
            server.stop()
        else:
            await message.channel.send('既に終了しています')

    elif message.content == 'r.status':
        try:
            status = server1.status() #server開いてるかのコマンド
            print("ステータスリクエスト")
            await message.channel.send('サーバーはオンラインです')
        except:
            print("ステータスリクエスト")
            await message.channel.send('サーバーはオフラインです')

    elif message.content == 'r.player':
        try:
            status = server1.status()
            print("プレイヤーリクエスト")
            await message.channel.send("サーバーには{0}人います".format(status.players.online))
        except:
            print("サーバーオフライン")
            await message.channel.send("サーバーを起動してください")

    

    #デバッグ用コマンドのためコメントアウト
    #elif message.content == 'r.get':
        #await message.channel.send(server.server_is_running())

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

