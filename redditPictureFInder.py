import Tkinter, tkFileDialog, praw, urllib
from Tkinter import *

user_agent = ("NaturePhotoGrabber Bot 0.1")
client_id = ("GIBQVGfUC2mtAA")
client_secret = ("a7Mo43y0-vIFojIF_Buw6Ea0ZeU")

def getImages(subName, numImages, saveDir):
	#get a reddit instance
	r = praw.Reddit(user_agent = user_agent, 
					client_id = client_id,
					client_secret = client_secret)

	#get a subreddit instance
	subreddit = r.subreddit(subName)

	number = 1
	#max number of submissions to search
	maxSubmissions = 100
	for submission in subreddit.hot(limit = maxSubmissions):
		#go through the top posts downloading their preview images (if they have one)
		#stops after the requested number of images are obtained or after 100 submissions have been searched. Whichever comes first
		if hasattr(submission, "preview"):
			url =  submission.preview['images'][0]['source']['url']
			filename = saveDir + "/redditPic" + str(number) + ".jpg"
			#saves the image at the location of 'filename'
			urllib.urlretrieve(url, filename)
			number = number + 1
			if number > numImages:
				return
	return


#Create interface using Tkinter

root = Tkinter.Tk()
root.wm_title("ImageImporter For Reddit")

root.minsize(400,150);

runningState = StringVar()
runningState.set("Ready")
#---------------------------------------------------------

subFrame = Frame(root)
subFrame.pack()

subLabel = Label(subFrame, text = "www.reddit.com/r/")
subLabel.pack(side = LEFT)

subEntry = Entry(subFrame, relief = SUNKEN)
subEntry.pack(side = RIGHT)
#---------------------------------------------------------

numFrame = Frame(root)
numFrame.pack()

numLabel = Label(numFrame, text = "Number of images: ")
numLabel.pack(side = LEFT)

numEntry = Entry(numFrame, relief = SUNKEN)
numEntry.pack(side = RIGHT)
#---------------------------------------------------------

directory = StringVar()
directory.set("C:/Users/Trevor/Documents/bgPics")

def openFileBrowser():
	newDir = tkFileDialog.askdirectory()
	if newDir != "":
		directory.set(newDir)

fileFrame = Frame(root)
fileFrame.pack()

browseButton = Button(fileFrame, command = openFileBrowser, text = "Save To:", relief = RAISED)
browseButton.pack(side = LEFT)

fileLabel = Label(fileFrame, textvariable = directory)
fileLabel.pack(side = RIGHT)
#---------------------------------------------------------
#frame included just for padding

paddingFrame = Frame(root, height = 10)
paddingFrame.pack()
#---------------------------------------------------------

def submitCallback():
	runningState.set("Working...")
	root.update()
	subreddit = subEntry.get()
	numPics = int(numEntry.get());
	saveDirectory = fileLabel.cget("text")
	getImages(subreddit, numPics, saveDirectory)
	runningState.set("Ready")

submitButton = Button(root, command = submitCallback, text = "GO", relief = RAISED)
submitButton.pack()
#---------------------------------------------------------

stateLabel = Label(root, textvariable = runningState)
stateLabel.pack()


root.mainloop()
