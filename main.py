import os
import discord
import requests
import asyncio
from bs4 import BeautifulSoup
from keep_alive import keep_alive


client = discord.Client()

async def getLatestGrrmBlog():
  latestDate = ''
  await client.wait_until_ready()
  botId = client.get_channel(int(os.environ['CHANNELID']))

  while not client.is_closed():
    source = requests.get('https://georgerrmartin.com/notablog/').text
    soup = BeautifulSoup(source, 'lxml')
    post = soup.find('div', class_='post-main')
    postTitle = post.h1.text
    postDate = post.find('div', class_='thedate').text
    postUrl=post.find('a', href=True)['href']

    if latestDate != postDate:
      textMessage = '>>> ' + '**Not A Blog Just Updated**\nTitle: ' + postTitle +'\nDate: ' + postDate +'\nlink: '+ postUrl
      await botId.send(textMessage)

    latestDate = postDate
    print(latestDate)
    await asyncio.sleep(60 * 10)

  
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


client.loop.create_task(getLatestGrrmBlog())
keep_alive()
client.run(os.environ['TOKEN'])