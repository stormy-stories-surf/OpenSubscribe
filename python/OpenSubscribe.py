#!/usr/bin/env python3
import argparse
import time
import fileinput
import smtplib
import ssl
import json
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class OpenSubscribe:
    def __init__(self):
        self.sender_email = "<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>"
        self.sender_password = "<PUT_YOUR_SENDER_PASSWORD_HERE>"
        self.smtp_server = "<PUT_YOUR_SMTP_SERVER_HERE>"
        self.smtp_port = "<PUT_YOUR_SMTP_PORT_HERE>"

    def setup(self, configFileName_ = "config/config.json"):
        with open(configFileName_) as json_file:
            data = json.load(json_file)
            urlWebsite = data["URL_WEBSITE"]
            smtpServer = data["SMTP_SERVER"]
            smtpPort = data["SMTP_PORT"]
            smtpSenderMailAddress = data["SMTP_SENDER_MAIL_ADDRESS"]
            smtpSenderPassword = data["SMTP_SENDER_PASSWORD"]
            confirmSubscribtion = data["CONFIRM_SUBSCRIBTION"]
            confirmSubscribtionSqlUser = confirmSubscribtion["SQL_USER"]
            confirmSubscribtionSqlPW = confirmSubscribtion["SQL_PASSWORD"]
            subscribtionForm = data["SUBSCRIBTION_FORM"]
            subscribtionFormSqlUser = subscribtionForm["SQL_USER"]
            subscribtionFormSqlPW = subscribtionForm["SQL_PASSWORD"]
            sendConfirmSubscribtionMails = data["SEND_CONFIRM_SUBSCRIBTION_MAILS"]
            sendConfirmSubscribtionMailsSqlUser = sendConfirmSubscribtionMails["SQL_USER"]
            sendConfirmSubscribtionMailsSqlPW = sendConfirmSubscribtionMails["SQL_PASSWORD"]

        print("Setup done")

        for filename in ["mail-templates/confirmSubscribtion.html",
                         "mail-templates/confirmSubscribtion.txt",
                         "php/ConfirmSubscribtion.php",
                         "php/SubscribtionForm.php",
                         "python/OpenSubscribe.py",
                         "sql/setupDatabase.sql"
                         ]:
            self.replaceStringInFile(filename, "<PUT_YOUR_URL_HERE>", urlWebsite)
            self.replaceStringInFile(filename, "<PUT_YOUR_SMTP_SERVER_HERE>", smtpServer)
            self.replaceStringInFile(filename, "<PUT_YOUR_SMTP_PORT_HERE>", smtpPort)
            self.replaceStringInFile(filename, "<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>", smtpSenderMailAddress)
            self.replaceStringInFile(filename, "<PUT_YOUR_SENDER_PASSWORD_HERE>", smtpSenderPassword)
            self.replaceStringInFile(filename, "<PUT_YOUR_CONFIRM_SUBSCRIBTION_USER_PASSWORD_HERE>", confirmSubscribtionSqlPW)
            self.replaceStringInFile(filename, "<PUT_YOUR_SUBSCRIBTION_FORM_USER_PASSWORD_HERE>", subscribtionFormSqlPW)
            self.replaceStringInFile(filename, "<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>", sendConfirmSubscribtionMailsSqlPW)



    def replaceStringInFile(self, filename, old_string, new_string):
        with fileinput.FileInput(filename, inplace=True) as file:
            for line in file:
                print(line.replace(old_string, new_string), end='')

    def smtpLogin(self):
        # Create a secure SSL context
        self.context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.ehlo()  # Can be omitted
            self.server.starttls(context=self.context)  # Secure the connection
            self.server.ehlo()  # Can be omitted
            self.server.login(self.sender_email, self.sender_password)

        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def sendConfirmSubscribtionMail(self, receipientData_):
        mailaddress = receipientData_[0]
        subscribtionID = receipientData_[1]
        print("Mail : " + mailaddress)
        print("SubscribtionID : " + subscribtionID)

        try:
            #receipientsList = [receipient_]
            #receipients = ", ".join(receipientsList)
            receipients = mailaddress
            message = MIMEMultipart(
                "Please confirm your subscribtion for STORMY-STORIES.SURF")
            message["Subject"] = "Please confirm your subscribtion for STORMY-STORIES.SURF"
            message["From"] = self.sender_email
            message["To"] = receipients

            # Create the plain-text and HTML version of your message
            with open("mail-templates/confirmSubscribtion.txt", 'r') as file:
                text = file.read()
                text = text.replace("XXXXX", subscribtionID)

            with open("mail-templates/confirmSubscribtion.html", 'r') as file:
                html = file.read()
                html = html.replace("XXXXX", subscribtionID)

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            self.server.sendmail(
                self.sender_email, receipients, message.as_string())
            print("Successfully sent email")

        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def smtpClose(self):
        self.server.quit()

    def confirmDeamon(self):
        while (True):
            self.smtpLogin()
            mailAddresses = self.getMailAddressesWithoutConfirmation()
            for mailAddress in mailAddresses:
                self.sendConfirmSubscribtionMail(mailAddress)
            self.smtpClose()
            time.sleep(30)



    def getMailAddressesWithoutConfirmation(self):
        myresult = ""
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="SendMailsUser",
                passwd="<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>",
                database="OpenSubscribe"
            )

            mycursor = mydb.cursor()
            mycursor.execute( "SELECT mailaddress, subscribeID FROM subscriber WHERE confirmationMailSent = 0 ")
            myresult = mycursor.fetchall()

        except Error as error:
            print(error)

        finally:
            mycursor.close()
            mydb.close()
            return myresult

    def updateConfirmationMailSent(self,subscriberID_):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="SendMailsUser",
                passwd="<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>",
                database="OpenSubscribe"
            )

            mycursor = mydb.cursor()
            query = "UPDATE subscriber SET confirmationMailSent = 1 WHERE id = %1"
            data = (subscriberID_)
            mycursor.execute(query, data)

            # accept the changes
            mydb.commit()

        except Error as error:
            print(error)

        finally:
            mycursor.close()
            mydb.close()


    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--setup', action='store_true',
             help='Setup OpenSubscribe with options set in config.json')

        parser.add_argument(
            '--confirmD', action='store_true',
             help='Runs the confirm-subscribtion-mails daemon, which as a ' +
                  'never ending service checks the database for new subscribtions' +
                  'and sends a confirm-subscribtion mail for every new subscribtion')

        args = parser.parse_args()
        return args

def main():
    s = OpenSubscribe()
    args = s.parseArgs()
    if args.setup:
        s.setup("config/config_stormy_stories.json")
    if args.confirmD:
        s.updateConfirmationMailSent("1")
        #s.confirmDeamon()

if __name__ == '__main__':
    main()
