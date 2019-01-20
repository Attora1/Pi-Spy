#!/usr/bin/python3.4

import subprocess
import numpy as np
import imutils
import os
from twilio.rest import Client
import cv2
import time
import mysql.connector

DidDoubleCheck = False
DidDoubleCheckOut = False

def CheckIfPackageIsThere():
	bashCommand = "fswebcam -d /dev/video1 -r 1280x720 image.jpg"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

        # load the image and convert it to grayscale
	image = cv2.imread("image.jpg")
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # compute the Scharr gradient magnitude representation of the images
        # in both the x and y direction using OpenCV 2.4
	ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
	gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
	gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

        # subtract the y-gradient from the x-gradient
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)

        # blur and threshold the image
	blurred = cv2.blur(gradient, (9, 9))
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

        # construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # perform a series of erosions and dilations
	closed = cv2.erode(closed, None, iterations = 4)
	closed = cv2.dilate(closed, None, iterations = 4)

        # find the contours in the thresholded image, then sort the contours
        # by their area, keeping only the largest one

	cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	try:
		c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
	except IndexError as e:
		BoxNotDetected()
		quit()
        #The box is found here
	BoxDetected()
def BoxDetected():
	# get phone number from profile table
	print("Getting phone Number")
	getPhoneNumber = "SELECT phone_number FROM Profile ORDER BY ID DESC LIMIT 1;"
	cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
	cursor = cnx.cursor(buffered=True)
	cursor.execute(getPhoneNumber)
	phone_number = cursor.fetchall()[0][0]
	cursor.close
	cnx.close()
	print("Phone Number: " + phone_number)
	
	print("Getting max value")
	getLastID = "SELECT MAX(Id) FROM Info;"
	cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
	cursor = cnx.cursor(buffered=True)
	cursor.execute(getLastID)
	all = cursor.fetchall()[0][0]
	cursor.close
	cnx.close()
	if (all == None):
		print("Apparently database is empty")
		#add row and text user make phone number variable
#		sendNewPackageText(phoneNumber)
		enter_time = int(time.time())
		# grab current image then move it into enter url folder and rename it to something unique

		cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
		cursor = cnx.cursor(buffered=True)
		try:
			os.rename('image.jpg', 'enter_image/image' + str(enter_time) + ".jpg")
		except FileNotFoundError as e:
			pass

		add_package = ("INSERT INTO Info "
			"(isPackagePresent, enter_url, enter_timestamp) "
			"VALUES (%s, %s, %s)")
		package_data = ("True", "image" + str(enter_time) + ".jpg", enter_time)
		cursor.execute(add_package, package_data)
		cnx.commit()
		cursor.close
		cnx.close()
		sendNewPackageText(phone_number)
	else:
		print("Not empty")
		#check bool
		print("Checking bool")
		GetLastBool = "SELECT isPackagePresent FROM Info ORDER BY ID DESC LIMIT 1;"
		cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
		cursor = cnx.cursor(buffered=True)
		cursor.execute(GetLastBool)
		LastBool = cursor.fetchall()[0][0]
		cursor.close
		cnx.close()		
		if(LastBool == "True"):
			print("Package still there, exiting")
			print(LastBool)
			quit()
		else:
	                #Text user number should still be in scope
			
			print("Package went missing :( adding new entity")
			#add row recheck for false positives
			enter_time = int(time.time())
                	# grab current image then move it into enter url folder and rename it to something unique

			cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
			cursor = cnx.cursor(buffered=True)
			try:
				os.rename('image.jpg', 'enter_image/image' + str(enter_time) + ".jpg")
			except FileNotFoundError as e:
				pass

			add_package = ("INSERT INTO Info "
				"(isPackagePresent, enter_url, enter_timestamp) "
				"VALUES (%s, %s, %s)")
			package_data = ("True", "image" + str(enter_time) + ".jpg", enter_time)
			cursor.execute(add_package, package_data)
			cnx.commit()
			cursor.close
			cnx.close()
			sendNewPackageText(phone_number)

def BoxNotDetected():
	print("Getting phone Number")
	getPhoneNumber = "SELECT phone_number FROM Profile ORDER BY ID DESC LIMIT 1;"
	cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
	cursor = cnx.cursor(buffered=True)
	cursor.execute(getPhoneNumber)
	phone_number = cursor.fetchall()[0][0]
	cursor.close
	cnx.close()
	print("Phone Number: " + phone_number)
	
	#get the users number too
	print("Box not detected")
	CurrentTime = int(time.time())
	getLastID = "SELECT MAX(Id) FROM Info;"
	cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
	cursor = cnx.cursor(buffered=True)
	cursor.execute(getLastID)
	all = cursor.fetchall()[0][0]
	print("All is " + str(all))
	cursor.close
	cnx.close()
	if (all == None):
		print("DB is empty, ignoring")
		quit()  #it is empty do nothing
	else:
		print("Db contains at least one item, checking bool")
		#it contains something check bool
		GetLastBool = "SELECT isPackagePresent FROM Info ORDER BY ID DESC LIMIT 1;"
		cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
		cursor = cnx.cursor(buffered=True)
		cursor.execute(GetLastBool)
		LastBool = cursor.fetchall()[0][0]		
		cursor.close
		cnx.close()
		if(LastBool == "True"):
			retrievePackageText(phone_number)
			#Text user because package might have been stolen!
			print("Bool is true, editing database")
			fileName = 'image' + str(CurrentTime) + '.jpg'
			print("filename is set to " + fileName)
			#bool is true do everything
			try:
				os.rename('image.jpg', 'exit_image/image' + str(CurrentTime) + ".jpg")
			except FileNotFoundError as e:
                        	pass
			print("Trying to update database")
			UpdateDB = "UPDATE Info SET isPackagePresent = 'False', exit_url =\'" + fileName +  "\', exit_timestamp = " + str(CurrentTime)  + " WHERE id = " + str(all)  + ";"
			#update_values = (fileName, CurrentTime, all)

#			UpdateDB = ("UPDATE Info, SET"
#				"(isPackagePresent, exit_url, exit_timestamp) "
#				"VALUES ('False', %s, %d)")

#			UpdateDBdata = (str(CurrentTime) + '.jpg', all)

			print("Current query is " + UpdateDB)
			cnx = mysql.connector.connect(user='root', password='PiSpy',host='127.0.0.1',database='Pi_Spy')
			cursor = cnx.cursor(buffered=True)
			cursor.execute(UpdateDB)
			cnx.commit()
			cursor.close
			cnx.close()
			
			
		else:
			#bool is false do nothing
			print("Bool is false exiting")
			quit()


def sendNewPackageText(clientNumber):
	account_sid = 'AC722fba748e992463888ef58dd6bf2216'
	auth_token = '8970619b03e7cfbf1430bcb81bff73a9'
	client = Client(account_sid, auth_token)

	message = client.messages \
		.create(
			body="Good afternoon. You have a package at your house available for pickup. Please see Pi-Spy logs for details",
			from_='+19478004230',
			to='+' + clientNumber
			)

    
	



def retrievePackageText(clientNumber):
	account_sid = 'AC722fba748e992463888ef58dd6bf2216'
	auth_token = '8970619b03e7cfbf1430bcb81bff73a9'
	client = Client(account_sid, auth_token)
	
	message = client.messages \
		.create(
			body="Good afternoon. Someone has picked up your package today, was it you? (Yes/No)",
			from_='+19478004230',
			to='+' + clientNumber
			)


CheckIfPackageIsThere()
