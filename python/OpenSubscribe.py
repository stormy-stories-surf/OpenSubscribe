#!/usr/bin/env python3
import argparse
import fileinput
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class OpenSubscribe:
    def __init__(self, smtpServer_, port_, smtpUser_, smtpPassword_):
        self.smtp_server = smtpServer_
        self.port = port_  # For starttls
        self.sender_email = smtpUser_
        self.password = smtpPassword_

    def setup(self, configFileName_ = "mail-templates/confirmSubscribtion.html"):
        print("Im in setup function")
        self.replaceStringInFile(configFileName_,
                            "<PUT_YOUR_URL_HERE>", "https://stormy-stories.surf")

    def replaceStringInFile(self, filename, old_string, new_string):
        with fileinput.FileInput(filename, inplace=True) as file:
            for line in file:
                print(line.replace(old_string, new_string), end='')

    def smtpLogin(self):
        # Create a secure SSL context
        self.context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.port)
            self.server.ehlo()  # Can be omitted
            self.server.starttls(context=self.context)  # Secure the connection
            self.server.ehlo()  # Can be omitted
            self.server.login(self.sender_email, self.password)

        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def sendConfirmSubscribtionMail(self, receipient_, subscribtionID_):
        try:
            receipientsList = [receipient_]
            receipients = ", ".join(receipientsList)
            message = MIMEMultipart(
                "Please confirm your subscribtion for STORMY-STORIES.SURF")
            message["Subject"] = "Please confirm your subscribtion for STORMY-STORIES.SURF"
            message["From"] = self.sender_email
            message["To"] = receipients

            # Create the plain-text and HTML version of your message
            with open('confirmSubscribtion.txt', 'r') as file:
                text = file.read()
                text = text.replace("XXXXX", subscribtionID_)

            with open('confirmSubscribtion.html', 'r') as file:
                html = file.read()
                html = html.replace("XXXXX", subscribtionID_)

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

    def getMailAddressesWithoutConfirmation(self):
        print("TO BE CONTINUED")

        import mysql.connector

        mydb = mysql.connector.connect(
            host="localhost",
            user="SendMailsUser",
            passwd="<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>",
            database="OpenSubscribe"
        )

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT mailaddress, subscribeID FROM subscriber WHERE confirmationMailSent = 0 ")

        myresult = mycursor.fetchall()

        for x in myresult:
            mailaddress = x[0]
            subscribeID = x[1]
            print("Mail : " + mailaddress)
            print("SubscribeID : " + subscribeID)

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--setup', action='store_true',
             help='Setup OpenSubscribe with options set in config.json')
        args = parser.parse_args()
        return args

def main():
    s = OpenSubscribe("<PUT_YOUR_SMTP_SERVER_HERE>", "<PUT_YOUR_SMTP_PORT_HERE>" , "<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>", "<PUT_YOUR_SENDER_PASSWORD_HERE>")
    args = s.parseArgs()
    if args.setup:
        s.setup()

if __name__ == '__main__':
    main()
