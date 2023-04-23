from twython import Twython
import datetime
from time import sleep 
from PIL import Image, ImageDraw, ImageFont

######## CHECK STATUS ##################
def checkStipend():
	openStipend = open("/path/to/stipendStatus.txt","r")
	if (openStipend.readline() == "True"): 
		openStipend.close()
		return True
	else:
		openStipend.close()
		return False
		
def wasStipendDone():
	checkRepeat = open("/path/to/wasStipendDone.txt","r")
	if (checkRepeat.readline() == "True"):
		checkRepeat.close()
		return True
	else:
		checkRepeat.close()
		return False
		
def isNewSem():
	global now, S1, S2, S3
	prevSem = 0
	nowSem = 0
	nowMonth = now.month
	if(nowMonth in S1):
		nowSem = 1
	elif(nowMonth in S2):
		nowSem = 2
	elif(nowMonth in S3):
		nowSem = 3
	else:
		nowSem = 0
	checkSem = open("/path/to/isNewSem.txt","r")
	lastSem = int(checkSem.read())
	if(lastSem in S1):
		prevSem = 1
	elif(lastSem in S2):
		prevSem = 2
	elif(lastSem in S3):
		prevSem = 3
	else:
		prevSem = 0
	if(prevSem == nowSem):
		checkSem.close()
		return False
	else:
		checkSem.close()
		return True

######## INITIALIZATION ####################
C_key = ''
C_secret = ''
A_token = ''
A_secret = ''
now = datetime.datetime.now()
stipendbot = Twython(C_key,C_secret,A_token,A_secret)
tweet_media = open('/path/to/img/DAILY.png','rb')

######## SEM ID CREATION ###############
S1 = [9,10,11,12,1]
S2 = [2,3,4,5,6]
S3 = [7,8]


if int(now.strftime("%m")) in S1:
	doWrite = False
	with open("/path/to/isFirstCheckDone.txt","r") as f:
		if (f.readline() == "False"):
			doWrite = True
	if (doWrite == True):
		with open("/path/to/isFirstCheckDone.txt","w+") as f:
			with open("/path/to/currSem.txt","w+") as g:
				g.write(str(now.year%100) + str((now.year+1)%100))
			f.write("True")
	currSem = open("/path/to/currSem.txt","r")
	sem_id = "1S" + str(currSem.read().split('\n')[0])
	currSem.close()
elif int(now.strftime("%m")) in S2:
    with open("/path/to/isFirstCheckDone.txt","w+") as f:
        if (f.readline() == "True"):
            f.write("False")
    currSem = open("/path/to/currSem.txt","r")
    sem_id = "2S" + str(currSem.read().split('\n')[0])
    currSem.close()
elif int(now.strftime("%m")) in S3:
	currSem = open("/path/to/currSem.txt","r")
	sem_id = "3S" + str(currSem.read().split('\n')[0])
	currSem.close()
else:
	print("what the fuck")


######## TWEET CONTENT ##################
message = "It has been "+ str((datetime.date.today()-datetime.date(2023,2,13)).days) + " days since the start of the sem.\n" + "For sem " + sem_id + ", as of " + now.strftime('%B') + " " +str(now.day) +", "+str(now.year) + ":"
print("Current Semester: " + '\t' + sem_id)
print("Current Time: " + '\t' + '\t' + now.strftime('%B %d, %I:%M %p'))
print("Tweet text: " + '\t' + '\t' + message)
print("Stipend status: " + '\t' + str(checkStipend()))
print("Is New Sem: " + '\t' + '\t' + str(isNewSem()))

####### STIPEND CHECK ###################
if(isNewSem() == True):
	stipendOverride = open("/path/to/stipendStatus.txt","w")
	stipendOverride.write("False")
	stipendOverride.close()
else:
	pass
if(checkStipend() == False):
	img_msg = "WALA PA RING STIPEND"+'\n'+"FOR SEM " + sem_id + " DAY " + str((datetime.date.today()-datetime.date(2023,2,13)).days)
else:
	img_msg = "MAY STIPEND NA"+'\n'+"FOR SEM " + sem_id	 + " DAY " + str((datetime.date.today()-datetime.date(2023,2,13)).days)	

####### IMAGE CREATION #################
W,H = (1000,1000)
img = Image.open('/path/to/img/stipendbot-template.png')
fnt = ImageFont.truetype('/path/to/fonts/Montserrat-SemiBold.ttf', 72)
d = ImageDraw.Draw(img)
w, h = d.textsize(img_msg, font=fnt)
d.text(((W-w)/2,700), img_msg, font=fnt, anchor="ms" , align="center", fill=(0, 0, 0))
img.save('/path/to/img/DAILY.png')

####### TWEETING #######################
lastMonthCheck = open("/path/to/isNewSem.txt","w")
lastMonthCheck.write(str(now.month))
lastMonthCheck.close()

if(checkStipend() == False):
	repeatFile = open("/path/to/wasStipendDone.txt", "w")
	repeatFile.write("False")
	repeatFile.close()
	if(now.hour ==  15) and (now.minute == 0):
		tweet_media = open("/path/to/img/DAILY.png", "rb")
		response = stipendbot.upload_media(media=tweet_media)
		stipendbot.update_status(status=message, media_ids=[response['media_id']]) 
		print('''
		| \t \t \t \t \t|
		|\tStipend status updated.\t\t|
		| \t \t \t  \t\t|
		''')
	else:
		print("\nProfessor Oak: There is a time and place for everything.")
			
elif(checkStipend() == True):
	if(wasStipendDone() == False):
		message = "It has been "+ str((datetime.date.today()-datetime.date(2023,2,13)).days) + " days since the start of the sem.\n" +"For sem " + sem_id + ", as of " + now.strftime('%B') + " " +str(now.day) +", "+str(now.year) + now.strftime(' %I:%M %p:')
		tweet_media = open("/path/to/img/DAILY.png", "rb")
		response = stipendbot.upload_media(media=tweet_media)
		stipendbot.update_status(status=message, media_ids=[response['media_id']]) 
		print('''
		| \t \t \t \t \t|
		|\tStipend status updated.\t\t|
		| \t \t \t  \t\t|
		''')
		repeatFile = open("/path/to/wasStipendDone.txt", "w")
		repeatFile.write("True")
		repeatFile.close()
	else:
		if(now.hour ==  15) and (now.minute == 0) and (checkStipend() == False):
			tweet_media = open("/path/to/img/DAILY.png", "rb")
			response = stipendbot.upload_media(media=tweet_media)
			stipendbot.update_status(status=message, media_ids=[response['media_id']]) 
			print('''
			| \t \t \t \t \t|
			|\tStipend status updated.\t\t|
			| \t \t \t  \t\t|
			''')
		else:
			print("\nProfessor Oak: There is a time and place for everything.")
else:
	print("how did u even get here")
