#!/usr/bin/env python3
import os
import argparse
import time
import fileinput
import smtplib
import ssl
import json
import secrets
import string
import sys
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class SQLWrapper:
    def __init__(self, configFileName = "config/config.json"):
        with open(configFileName) as json_file:
            data = json.load(json_file)
            self.sqlHost = data["SQL_HOST"]
            self.sqlDatabase = data["SQL_DATABASE"]
            sendMailsData = data["SEND_MAILS"]
            self.sendMailsSqlUser = sendMailsData["SQL_USER"]
            self.sendMailsSqlPW = sendMailsData["SQL_PASSWORD"]
        self.databaseConnected = False

    def connect(self):
        try:
            self.mysqlConnector = mysql.connector.connect(
                host=self.sqlHost,
                user=self.sendMailsSqlUser,
                passwd=self.sendMailsSqlPW,
                database=self.sqlDatabase
            )
            self.databaseConnected = True

        except Error as error:
            print(error)

    def close(self):
        if self.databaseConnected:
            try:
                self.mysqlConnector.close()
                self.databaseConnected = False
            except Error as error:
                print(error)

    def getStatementTypeFromSQLQuery(self, sqlQuery_):
        statementType = sqlQuery_.partition(' ')[0]
        statementType = statementType.upper()
        allowedStatements = ["SELECT", "INSERT", "UPDATE"]
        if not statementType in allowedStatements :
            print("Error the given sql-query '{}' does not include any of the know sql-statement types. "
                  "Please use one of the following statements as the first word of your sql-query : {}!".format(sqlQuery_, allowedStatements))

        return statementType

    def executeSQLStatement(self, sqlQuery_, sqlValues_):
        statementType = self.getStatementTypeFromSQLQuery(sqlQuery_)

        if not self.databaseConnected:
            self.connect()

        if statementType == "SELECT":
            result = ""

        try:
            mysqlCursor = self.mysqlConnector.cursor()
            mysqlCursor.execute(sqlQuery_, sqlValues_)

            if statementType == "INSERT" or statementType == "UPDATE":
                self.mysqlConnector.commit()
            elif statementType == "SELECT":
                result = mysqlCursor.fetchall()

        except Error as error:
            print(error)

        finally:
            mysqlCursor.close()
            if statementType == "SELECT":
                return result

    def insert(self, sqlQuery_, sqlValues_):
        self.executeSQLStatement(sqlQuery_, sqlValues_)
        print("Successfully inserted query {} with values {}".format(sqlQuery_, sqlValues_))

    def select(self, sqlQuery_, sqlValues_):
        return self.executeSQLStatement(sqlQuery_, sqlValues_)

    def update(self, sqlQuery_, sqlValues_):
        self.executeSQLStatement(sqlQuery_, sqlValues_)
        print("Successfully updated query {} with values {}".format(sqlQuery_, sqlValues_))

    def __del__(self):
        self.close()

class Newsletter:
    def __init__(self, url, path, configFileName = "config/config.json"):
        self.path = path
        self.pathTXT = self.path + '/newBlogPost.txt'
        self.pathHTML = self.path + '/newBlogPost.html'
        self.url = url
        self.configFileName = configFileName
        self.clickCounterID = secrets.token_hex(64)
        self.creatNewsletterInDatabase()
        self.ID = self.getIDFromDatabase()

    def creatNewsletterInDatabase(self):
        sqlQuery = "INSERT INTO newsletter (url, pathTXT, pathHTML, clickCounterID, clickCounter, allMailsSent) VALUES (%s, %s, %s, %s, %s, %s)"
        sqlValues = (self.url, self.pathTXT, self.pathHTML, self.clickCounterID, 0, False)
        sqlWrapper = SQLWrapper(self.configFileName)
        sqlWrapper.insert(sqlQuery, sqlValues)
        print("Successfully created newsletter for url {}, pathTXT {} and pathHTML {}.".format(self.url, self.pathTXT, self.pathHTML))

    #todo : try to get this already from insert
    def getIDFromDatabase(self):
        sqlQuery = "SELECT id FROM newsletter WHERE url = %s AND pathTXT = %s"
        sqlValues = (self.url, self.pathTXT)
        sqlWrapper = SQLWrapper(self.configFileName)
        result = sqlWrapper.select(sqlQuery, sqlValues)
        return result[0][0]

    def getID(self):
        return self.ID


class NewsletterMail:
    def __init__(self, sqlResult):
        self.logID            = sqlResult[0]
        self.newsletterID     = sqlResult[1]
        self.url              = sqlResult[2]
        self.pathHTML         = sqlResult[3]
        self.pathTXT          = sqlResult[4]
        self.clickCounterID   = sqlResult[5]
        self.subscriberID     = sqlResult[6]
        self.mailaddress      = sqlResult[7]
        self.unsubscribeID    = sqlResult[8]

    def toString(self):
        print("-----------------------------")
        print("logID : {}".format(self.logID))
        print("newsletterID : {}".format(self.newsletterID))
        print("-----------------------------")
        print("url : {}".format(self.url))
        print("pathHTML : {}".format(self.pathHTML))
        print("pathTXT : {}".format(self.pathTXT))
        print("clickCounterID : {}".format(self.clickCounterID))
        print("subscriberID : {}".format(self.subscriberID))
        print("mailaddress : {}".format(self.mailaddress))
        print("unsubscribeID : {}".format(self.unsubscribeID))
        print("-----------------------------")

class OpenSubscribe:
    def __init__(self):
        self.sender_email = "<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>"
        self.sender_password = "<PUT_YOUR_SENDER_PASSWORD_HERE>"
        self.smtp_server = "<PUT_YOUR_SMTP_SERVER_HERE>"
        self.smtp_port = "<PUT_YOUR_SMTP_PORT_HERE>"

    def setup(self, args):
        with open(args.configFileName) as json_file:
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
            sendMailsData = data["SEND_MAILS"]
            sendMailsSqlUser = sendMailsData["SQL_USER"]
            sendMailsSqlPW = sendMailsData["SQL_PASSWORD"]
            unsubscribeData = data["UNSUBSCRIBE"]
            unsubscribeSqlUser = unsubscribeData["SQL_USER"]
            unsubscribeSqlPW = unsubscribeData["SQL_PASSWORD"]
            upDateClickCounterData = data["UPDATE_CLICK_COUNTER"]
            upDateClickCounterSqlUser = upDateClickCounterData["SQL_USER"]
            upDateClickCounterSqlPW = upDateClickCounterData["SQL_PASSWORD"]

        for filename in ["mail-templates/confirmSubscribtion.html",
                         "mail-templates/confirmSubscribtion.txt",
                         "mail-templates/newBlogPost.txt",
                         "php/ConfirmSubscribtion.php",
                         "php/SubscribtionForm.php",
                         "php/Unsubscribe.php",
                         "php/GoTo.php",
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
            self.replaceStringInFile(filename, "<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>", sendMailsSqlPW)
            self.replaceStringInFile(filename, "<PUT_YOUR_UNSUBSCRIBE_USER_PASSWORD_HERE>", unsubscribeSqlPW)
            self.replaceStringInFile(filename, "<PUT_YOUR_UPDATE_CLICK_COUNTER_USER_PASSWORD_HERE>", upDateClickCounterSqlPW)

        print("Setup done")


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

        self.sendMail(subject, fromMail, toMail, ccMail, bccMail, text, html, [])

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

        self.sendMail(subject, fromMail, toMail, ccMail, bccMail, text, html, [])


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
        # todo : remove
        # todo : fix to relative path
        #images = ['/etc/OpenSubscribe/mail-templates/images/logo_small.png']
        images = []

        self.sendMail(subject, fromMail, toMail, ccMail, bccMail, text, html, images)

    def sendMail(self, subject_, from_, to_, cc_, bcc_, contentTXT_, contentHTML_, images_):
        try:
            # Encapsulate the plain and HTML versions of the message body in an
            # 'alternative' part, so message agents can decide which they want to display.
            message = MIMEMultipart('alternative')
            message["Subject"] = subject_
            message["From"] = from_
            message["To"] = to_
            message["Cc"] = cc_
            message["Bcc"] = bcc_

            # Turn these into plain/html MIMEText objects
            partPlain = MIMEText(contentTXT_, "plain")
            partHtml = MIMEText(contentHTML_, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(partPlain)
            message.attach(partHtml)

            # todo : remove
            for image in images_:
                print("image path : "+ image)
                print("image file name " + os.path.splitext(os.path.basename(image))[0])
                # This example assumes the image is in the current directory
                fp = open(image, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', os.path.splitext(os.path.basename(image))[0])
                message.attach(msgImage)

            #self.server.sendmail(from_, to_, message.as_string())
            # wait here for the result to be available before continuing
            while self.server.sendmail(from_, to_, message.as_string()) is None:
                pass

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

    def infoMailDeamon(self, args):
        while (True):
            self.sendConfirmSubscribtionMails()
            self.sendUnsubscribedMails()
            time.sleep(30)

    def getUnsubscribedMailAddresses(self):
        sqlQuery = "SELECT id, mailaddress, subscribeID, unsubscribeID FROM subscriber WHERE unSubscribed = 1 AND unSubscribedMailSent = 0 "
        sqlValues = ()
        sqlWrapper = SQLWrapper(self.configFileName)
        return sqlWrapper.select(sqlQuery, sqlValues)

    def getMailAddressesWithoutConfirmation(self):
        sqlQuery = "SELECT id, mailaddress, subscribeID, unsubscribeID FROM subscriber WHERE confirmationMailSent = 0"
        sqlValues = ()
        sqlWrapper = SQLWrapper(self.configFileName)
        return sqlWrapper.select(sqlQuery, sqlValues)

    # todo : test
    def updateUnSubscribedMailSent(self, id_):
        sqlQuery = "UPDATE subscriber SET mailaddress = '', unSubscribedMailSent = 1 WHERE id = %s"
        sqlValues = (id_,)
        sqlWrapper = SQLWrapper(self.configFileName)
        sqlWrapper.update(sqlQuery, sqlValues)

    # todo : test
    def updateConfirmationMailSent(self,subscriberID_):
        sqlQuery = "UPDATE subscriber SET confirmationMailSent = 1 WHERE id = %s"
        sqlValues = (subscriberID_,)
        sqlWrapper = SQLWrapper(self.configFileName)
        sqlWrapper.update(sqlQuery, sqlValues)

    def createNewsletterMail(self, newsletterID_):
        subscriberIDs = self.getSubscriberIDsWithConfirmation()
        for subscriberID in subscriberIDs:
            sqlQuery = "INSERT INTO newsletterMail (newsletterID, subscriberID, sent) VALUES (%s, %s, %s)"
            sqlValues = (newsletterID_, subscriberID[0], False)
            sqlWrapper = SQLWrapper(self.configFileName)
            sqlWrapper.insert(sqlQuery, sqlValues)
            print("Successfully created newsletterMail for newsletterID {} and subscriberID {}.".format(newsletterID_, subscriberID[0]))

    def getSubscriberIDsWithConfirmation(self):
        sqlQuery = "SELECT id FROM subscriber WHERE subscribtionConfirmed = 1 AND unSubscribed = 0 "
        sqlValues = ()
        sqlWrapper = SQLWrapper(self.configFileName)
        return sqlWrapper.select(sqlQuery, sqlValues)

    # todo : test
    def prepareNewsletter(self, args):
        newsletter = Newsletter(args.url, args.path, args.configFileName)
        self.createNewsletterMail(newsletter.getID())
        print("Successfully prepared database entries for newsletter with ID {} for url {} and path {}.".format(newsletter.getID(), args.url, args.path))

    def sendAllPreparedNewsletters(self, args):
        sqlQuery = "SELECT newsletterMail.id AS logID, " \
                "newsletterMail.newsletterID, " \
                "newsletter.url, " \
                "newsletter.pathHTML, " \
                "newsletter.pathTXT, " \
                "newsletter.clickCounterID, " \
                "subscriber.id AS subscriberID, " \
                "subscriber.mailaddress, " \
                "subscriber.unsubscribeID " \
                "FROM ((newsletterMail " \
                "INNER JOIN subscriber ON newsletterMail.subscriberID = subscriber.id) " \
                "INNER JOIN newsletter ON newsletterMail.newsletterID = newsletter.id);"
        sqlValues = ()
        sqlWrapper = SQLWrapper(self.configFileName)
        myresult = sqlWrapper.select(sqlQuery, sqlValues)

        for mail in myresult:
            newsletterMail = NewsletterMail(mail)
            newsletterMail.toString()

    def sendNewsletterDEPRECATED(self):
        self.smtpLogin()

        try:
            from_ = "info@stormy-stories.surf"
            to_ = "info@stormy-stories.surf"
            message = MIMEMultipart("subject_")
            message["Subject"] = "subject_"
            message["From"] = from_
            message["To"] = to_
            message["Cc"] = ""
            message["Bcc"] = ""

            # Encapsulate the plain and HTML versions of the message body in an
            # 'alternative' part, so message agents can decide which they want to display.
            msgAlternative = MIMEMultipart('alternative')
            message.attach(msgAlternative)

            msgText = MIMEText('This is the alternative plain text message.')
            msgAlternative.attach(msgText)

            # We reference the image in the IMG SRC attribute by the ID we give it below
            msgText = MIMEText('<b>Some <i>HTML</i> tex</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
            msgAlternative.attach(msgText)

            # This example assumes the image is in the current directory
            fp = open('test.jpg', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            # Define the image's ID as referenced above
            msgImage.add_header('Content-ID', 'image1')
            message.attach(msgImage)

            self.server.sendmail(from_, to_, message.as_string())
            print("Successfully sent email from " + from_ + " to " + to_)

        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def parseArgs(self):
        parser = argparse.ArgumentParser()

        # ---------------------------

        parser.add_argument('--configFileName', default='config/config.json', help='Defines the path of the configuration json-file.')

        # ---------------------------

        subparsers = parser.add_subparsers()

        # --------------------------

        setup_parser = subparsers.add_parser('setup',
                                   help='Setup OpenSubscribe with options set in config.json')


        setup_parser.set_defaults(func=self.setup)


        # --------------------------

        infoMailD_parser = subparsers.add_parser('infoMailD',
                                   help='Runs a never ending service that sends confirm-subscribtion ' +
                                        'mails for every new subscribtion and info mails for every '+
                                        'new confirmed mail address and every unsubscribed mail address')


        infoMailD_parser.set_defaults(func=self.infoMailDeamon)

        # --------------------------

        sendNewsletter_parser = subparsers.add_parser('sendNewsletter',
                                   help='Runs a never ending service that sends confirm-subscribtion ' +
                                        'mails for every new subscribtion and info mails for every '+
                                        'new confirmed mail address and every unsubscribed mail address')


        sendNewsletter_parser.set_defaults(func=self.sendAllPreparedNewsletters)


        # --------------------------

        prepareNewsletter_parser = subparsers.add_parser('prepareNewsletter', aliases=['pN'],
                                   help='Creates a new Newsletter entry in the database, ' +
                                        'which can be send afterwards.')


        prepareNewsletter_parser.set_defaults(func=self.prepareNewsletter)
        prepareNewsletter_parser.add_argument('--url', help='TODO')
        prepareNewsletter_parser.add_argument('--path', help='TODO')


        #parser.add_argument(
        #    '--setup', action='store_true',
        #     help='Setup OpenSubscribe with options set in config.json')

        #parser.add_argument(
        #    '--infoMailD', action='store_true',
        #     help='Runs a never ending service that sends confirm-subscribtion ' +
        #          'mails for every new subscribtion and info mails for every '+
        #          'new confirmed mail address and every unsubscribed mail address')

        #parser.add_argument(
        #    '--sendNewsletter', action='store_true',
        #     help='')

        #parser.add_argument(
        #    '--prepareNewsletter', action='store_true',
        #     help='Creates a new Newsletter entry in the database, ' +
        #          'which can be send afterwards.')

        #parser.add_argument(
        #    '--url', action='store', dest="url",
        #     help='TODO ')

        #parser.add_argument(
        #    '--path',
        #     help='TODO ')

        args = parser.parse_args()
        self.configFileName = args.configFileName
        return args

def main():
    s = OpenSubscribe()
    args = s.parseArgs()

    #if args.setup:
    #    s.setup("config/config_stormy_stories.json")
    #if args.infoMailD:
    #    s.infoMailDeamon()
    #if args.sendNewsletter:
    #    s.sendNewsletter()

    if hasattr(args, 'func') and args.func:
        args.func(args)
    else:
        print("Missing sub-command. See help")
        sys.exit(1)

if __name__ == '__main__':
    main()


