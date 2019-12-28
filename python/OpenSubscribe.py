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
            mailTemplatesDir = data["MAIL_TEMPLATES_DIR"]
            confirmSubscribtionData = data["CONFIRM_SUBSCRIBTION"]
            confirmSubscribtionSqlUser = confirmSubscribtionData["SQL_USER"]
            confirmSubscribtionSqlPW = confirmSubscribtionData["SQL_PASSWORD"]
            subscribtionFormData = data["SUBSCRIBTION_FORM"]
            subscribtionFormSqlUser = subscribtionFormData["SQL_USER"]
            subscribtionFormSqlPW = subscribtionFormData["SQL_PASSWORD"]
            sendConfirmSubscribtionMailsData = data["SEND_CONFIRM_SUBSCRIBTION_MAILS"]
            sendConfirmSubscribtionMailsSqlUser = sendConfirmSubscribtionMailsData["SQL_USER"]
            sendConfirmSubscribtionMailsSqlPW = sendConfirmSubscribtionMailsData["SQL_PASSWORD"]
            unsubscribeData = data["UNSUBSCRIBE"]
            unsubscribeSqlUser = unsubscribeData["SQL_USER"]
            unsubscribeSqlPW = unsubscribeData["SQL_PASSWORD"]

        print("Setup done")

        for filename in ["mail-templates/confirmSubscribtion.html",
                         "mail-templates/confirmSubscribtion.txt",
                         "mail-templates/newBlogPost.txt",
                         "php/ConfirmSubscribtion.php",
                         "php/SubscribtionForm.php",
                         "php/Unsubscribe.php",
                         "python/OpenSubscribe.py",
                         "sql/setupDatabase.sql"
                         ]:
            self.replaceStringInFile(filename, "<PUT_YOUR_URL_HERE>", urlWebsite)
            self.replaceStringInFile(filename, "<PUT_YOUR_SMTP_SERVER_HERE>", smtpServer)
            self.replaceStringInFile(filename, "<PUT_YOUR_SMTP_PORT_HERE>", smtpPort)
            self.replaceStringInFile(filename, "<PUT_YOUR_MAIL_TEMPLATES_DIR_HERE>", mailTemplatesDir)
            self.replaceStringInFile(filename, "<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>", smtpSenderMailAddress)
            self.replaceStringInFile(filename, "<PUT_YOUR_SENDER_PASSWORD_HERE>", smtpSenderPassword)
            self.replaceStringInFile(filename, "<PUT_YOUR_CONFIRM_SUBSCRIBTION_USER_PASSWORD_HERE>", confirmSubscribtionSqlPW)
            self.replaceStringInFile(filename, "<PUT_YOUR_SUBSCRIBTION_FORM_USER_PASSWORD_HERE>", subscribtionFormSqlPW)
            self.replaceStringInFile(filename, "<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>", sendConfirmSubscribtionMailsSqlPW)
            self.replaceStringInFile(filename, "<PUT_YOUR_UNSUBSCRIBE_USER_PASSWORD_HERE>", unsubscribeSqlPW)

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

    def sendNewSubscribtionInfoMail(self, receipientData_):
        # get individual data from receipientData_
        id = receipientData_[0]
        mailaddress = receipientData_[1]
        subscribeID = receipientData_[2]
        unsubscribeID = receipientData_[3]
        print("ID : " + str(id))
        print("Mail : " + mailaddress)
        print("subscribeID : " + subscribeID)
        print("unsubscribeID : " + unsubscribeID)

        # Create the plain-text and HTML version of your message
        with open("<PUT_YOUR_MAIL_TEMPLATES_DIR_HERE>/newSubscribtionInfo.txt", 'r') as file:
            text = file.read()
            text = text.replace("<MAILADDRESS>", mailaddress)
            text = text.replace("<SUBSCRIBE_ID>", subscribeID)
            text = text.replace("<UNSUBSCRIBE_ID>", unsubscribeID)

        with open("<PUT_YOUR_MAIL_TEMPLATES_DIR_HERE>/newSubscribtionInfo.html", 'r') as file:
            html = file.read()
            html = html.replace("<MAILADDRESS>", mailaddress)
            html = html.replace("<SUBSCRIBE_ID>", subscribeID)
            html = html.replace("<UNSUBSCRIBE_ID>", unsubscribeID)

        # set variables and send mail
        subject = "There is a new subscriber to your website!"
        fromMail = self.sender_email
        toMail = "info@stormy-stories.surf"
        ccMail = ""
        bccMail = ""

        self.sendMail(subject, fromMail, toMail, ccMail, bccMail, text, html)

    def sendUnsubscribedInfoMail(self, receipientData_):
        # get individual data from receipientData_
        id = receipientData_[0]
        mailaddress = receipientData_[1]
        print("ID : " + str(id))
        print("Mail : " + mailaddress)

        # Create the plain-text and HTML version of your message
        with open("<PUT_YOUR_MAIL_TEMPLATES_DIR_HERE>/unsubscribedInfo.txt", 'r') as file:
            text = file.read()
            text = text.replace("<MAILADDRESS>", mailaddress)

        with open("<PUT_YOUR_MAIL_TEMPLATES_DIR_HERE>/unsubscribedInfo.html", 'r') as file:
            html = file.read()
            html = html.replace("<MAILADDRESS>", mailaddress)

        # set variables and send mail
        subject = "Someone unSubscribed from your mail-newsletter of your website!"
        fromMail = self.sender_email
        toMail = "info@stormy-stories.surf"
        ccMail = ""
        bccMail = ""

        self.sendMail(subject, fromMail, toMail, ccMail, bccMail, text, html)


    def sendConfirmSubscribtionMail(self, receipientData_):
        # get individual data from receipientData_
        id = receipientData_[0]
        mailaddress = receipientData_[1]
        subscribeID = receipientData_[2]
        unsubscribeID = receipientData_[3]
        print("ID :  " + str(id))
        print("Mail : " + mailaddress)
        print("subscribeID : " + subscribeID)
        print("unsubscribeID : " + unsubscribeID)

        # Create the plain-text and HTML version of your message
        with open("<PUT_YOUR_MAIL_TEMPLATES_DIR_HERE>/confirmSubscribtion.txt", 'r') as file:
            text = file.read()
            text = text.replace("<SUBSCRIBE_ID>", subscribeID)
            text = text.replace("<UNSUBSCRIBE_ID>", unsubscribeID)

        with open("<PUT_YOUR_MAIL_TEMPLATES_DIR_HERE>/confirmSubscribtion.html", 'r') as file:
            html = file.read()
            html = html.replace("<SUBSCRIBE_ID>", subscribeID)
            html = html.replace("<UNSUBSCRIBE_ID>", unsubscribeID)

        # set variables and send mail
        subject = "Please confirm your subscribtion for STORMY-STORIES.SURF"
        fromMail = self.sender_email
        toMail = mailaddress
        ccMail = ""
        bccMail = "info@stormy-stories.surf"

        self.sendMail(subject, fromMail, toMail, ccMail, bccMail, text, html)

    def sendMail(self, subject_, from_, to_, cc_, bcc_, contentTXT_, contentHTML_):
        try:
            message = MIMEMultipart(subject_)
            message["Subject"] = subject_
            message["From"] = from_
            message["To"] = to_
            message["Cc"] = cc_
            message["Bcc"] = bcc_

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(contentTXT_, "plain")
            part2 = MIMEText(contentHTML_, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            self.server.sendmail(from_, to_, message.as_string())
            print("Successfully sent email from " + from_ + " to " + to_)

        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def smtpClose(self):
        self.server.quit()

    def sendConfirmSubscribtionMails(self):
        self.smtpLogin()
        mailAddresses = self.getMailAddressesWithoutConfirmation()
        for mailAddress in mailAddresses:
            self.sendConfirmSubscribtionMail(mailAddress)
            self.sendNewSubscribtionInfoMail(mailAddress)
            id = mailAddress[0]
            self.updateConfirmationMailSent(id)
        self.smtpClose()

    def sendUnsubscribedMails(self):
        self.smtpLogin()
        mailAddresses = self.getUnsubscribedMailAddresses()
        for mailAddress in mailAddresses:
            self.sendUnsubscribedInfoMail(mailAddress)
            id = mailAddress[0]
            self.updateUnSubscribedMailSent(id)
        self.smtpClose()

    def infoMailDeamon(self):
        while (True):
            self.sendConfirmSubscribtionMails()
            self.sendUnsubscribedMails()
            time.sleep(30)

    def getUnsubscribedMailAddresses(self):
        myresult = ""
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="SendMailsUser",
                passwd="<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>",
                database="OpenSubscribe"
            )

            mycursor = mydb.cursor()
            mycursor.execute( "SELECT id, mailaddress, subscribeID, unsubscribeID FROM subscriber WHERE unSubscribed = 1 AND unSubscribedMailSent = 0 ")
            myresult = mycursor.fetchall()

        except Error as error:
            print(error)

        finally:
            mycursor.close()
            mydb.close()
            return myresult


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
            mycursor.execute( "SELECT id, mailaddress, subscribeID, unsubscribeID FROM subscriber WHERE confirmationMailSent = 0 ")
            myresult = mycursor.fetchall()

        except Error as error:
            print(error)

        finally:
            mycursor.close()
            mydb.close()
            return myresult

    def updateUnSubscribedMailSent(self, id_):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="SendMailsUser",
                passwd="<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>",
                database="OpenSubscribe"
            )

            mycursor = mydb.cursor()
            query = "UPDATE subscriber SET mailaddress = '', unSubscribedMailSent = 1 WHERE id = %s"
            mycursor.execute(query, (id_,))

            # accept the changes
            mydb.commit()

        except Error as error:
            print(error)

        finally:
            mycursor.close()
            mydb.close()

    def updateConfirmationMailSent(self,subscriberID_):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="SendMailsUser",
                passwd="<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>",
                database="OpenSubscribe"
            )

            mycursor = mydb.cursor()
            query = "UPDATE subscriber SET confirmationMailSent = 1 WHERE id = %s"
            mycursor.execute(query, (subscriberID_,))

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
            '--infoMailD', action='store_true',
             help='Runs a never ending service that sends confirm-subscribtion ' +
                  'mails for every new subscribtion and info mails for every '+
                  'new confirmed mail address and every unsubscribed mail address')

        args = parser.parse_args()
        return args

def main():
    s = OpenSubscribe()
    args = s.parseArgs()
    if args.setup:
        s.setup("config/config_stormy_stories.json")
    if args.infoMailD:
        s.infoMailDeamon()


if __name__ == '__main__':
    main()
