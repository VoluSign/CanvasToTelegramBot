#install canvasapi, pyTelegramBotAPI

# Imports
import sys, os
import canvasapi
import telebot
from html.parser import HTMLParser
from canvasapi import Canvas, discussion_topic

#----# CANVAS #----#

#Class handles html to ascii conversion
class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, postContent):
        self.text += postContent

#bool for check
new = False

#Canvas API URL
API_URL = "!CANVAS BASE URL!"
#Canvas API key
API_KEY = "!CANVAS USER API KEY!"

#Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

COURSEID = "123456"

#Grab course 123456
course = canvas.get_course(COURSEID)

#Access the course's name
courseName = course.name

#For output
user = "Teacher"

#Opens txt file for check
aCheck = open("latest.txt","r")

aCheckStr = aCheck.read()

#Gets latest announcement
ann = canvas.get_announcements(context_codes=['course_{}'.format(COURSEID)])

#gets dumb stupid message from html
postContent = str(ann[0].__getattribute__("message"))

#Converts post from html to ascii
post = HTMLFilter()
post.feed(postContent)
finalPost = post.text

#Converts to string for following if statement
a = str(ann[0])

#stores message so it doesnt send repeating messages
if a != str(aCheckStr):
    new = True
    aCheckOverWrite = open("latest.txt","w+")
    aCheckOverWrite.write(a)
    aCheck.close()
    aCheckOverWrite.close()

#---------------------#

#if new = true, use to push message


#---# Telegram #---#

bot = telebot.TeleBot("!TELEGRAM BOT API KEY!")

#Handle commands: /link, /help, & /latest

@bot.message_handler(commands=['link'])
def handle_command(message):
    bot.reply_to(message, "Bot message: Here is a direct link to the canvas course. It will only work if you're logged in: https://gastoncs.instructure.com/courses/102829")
    
@bot.message_handler(commands=['help'])
def handle_command(message):
    bot.reply_to(message, "Bot message: The bot is Active. This bot was made in python by the one and only VoluSign. The source code for this bot can be found at https://github.com/VoluSign/CanvasToTelegramBot")   
    bot.reply_to(message, "Commands: /help, /link, /latest")

@bot.message_handler(commands=['latest'])
def handle_command(message):
    bot.reply_to(message, "Bot message: The following message will contain the most recent post to the Class of 2022 pertaining to scholarships:")
    bot.reply_to(message, f"{courseName} - {user}: {finalPost}")


#Bot sends latest post on start up (Trying to get automatic push if bool permits)
if new == True:
    bot.reply_to(message, f'Latest Announcement: {finalPost}')

#Starts server while script is running
bot.polling()





