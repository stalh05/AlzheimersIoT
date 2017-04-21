import time
import requests
from requests import *
import NotificationRecipientContactInfo

class EventSender():

    def __init__(self):
        self.emailAddresses = NotificationRecipientContactInfo.emailAddresses
        self.phoneNumbers = NotificationRecipientContactInfo.phoneNumbers
        self.emailAPIURL = "http://email_sender:5000/email"
        self.SMSAPIURL = "http://sms_sender:5000/sms"
        self.GoogleSendURL = "http://google_sender:5000/googleSend"
        self.baseURL = 'http://api:8080/api/'
        self.endpointNames = ['gps', 'wemo', 'journal', 'medicineLogger', 'memoryGame']

    def loopForever(self):
        while(True):
            for endpointName in self.endpointNames:
                fileName = "APIFiles/" + endpointName + ".txt"
                newestAPIGet = get(self.baseURL + endpointName).content.decode()
                hasAPIChanged = self.readAndCompareDataFile(fileName, newestAPIGet)
                if(hasAPIChanged):
                    self.writeDataToFile(fileName, newestAPIGet)
                    self.sendNotifications("there has been an update in " + endpointName)
            time.sleep(5)

    def readAndCompareDataFile(self, fileName, newestAPIGet):
        with open(fileName, 'r') as file:
            hasAPIChanged = False
            oldAPIInfo = file.read()
            if oldAPIInfo != newestAPIGet:
                hasAPIChanged = True
        file.close()
        return hasAPIChanged

    def writeDataToFile(self, fileName, newestAPIGet):
        with open(fileName, "w") as file:
            file.write(newestAPIGet)
            file.close()
        return

    def sendNotifications(self, message):
        self.sendEmailOrSMS(message, self.phoneNumbers, self.SMSAPIURL)
        self.sendEmailOrSMS(message, self.emailAddresses, self.emailAPIURL)
        requests.post(self.GoogleSendURL, data={"message": message})
        return

    def sendEmailOrSMS(self, message, recipients, APIURL):
        for recipient in recipients:
            payload = {"message":message,"recipient":recipient}
            requests.post(APIURL, data=payload)
        return

if __name__ == "__main__":
    eventSender = EventSender()
    eventSender.loopForever()