# OpenSubscribe
A python and php implementation of a tooling for handling E-Mail subscribtions / newsletters on your website.

**PROJECT STATUS : IN DEVELOPMENT**
<br />
<img src="docs/pictures/UnderConstructionIcon.png" width="15%">

## Roadmap

### v0.1.0

- [x] implement GoTo.php to forward to link
- [x] make GoTo.php to increase counter in database
- [x] implement --prepareNewsletter
- [x] add newsletter-entry table to log which mails are sent
- [x] implement OpenSubscribe --sendNewsletter
- [x] test OpenSubscribe --sendNewsletter
- [ ] fix bug : if you create two newsletters with same path the newsletterMail data will have the wrong newsletter ID
- [x] only send mails to which are not yet sent = 1
- [x] update logo in website and all mails
- [x] make mail-templates compatible to Outlook html rendering
- [x] rendering of logo for confirmSubscrtiption mail  in google-mail
- [x] rendering of logo for newsletter mail t-online mail
- [ ] add unsubscription confirmed html
- [x] use OpenSubscribe in newsletter page
- [x] update 'sent' field in database with 'sendNewsletter'
- [ ] update 'allMailsSent' field in database with 'sendNewsletter'
- [ ] Run through testing phase:
  - [ ] Check if confirm subscribtion mail is received and displayed well formatted
  - [ ] Check if confirm subscribtion mail is not shown as spam / junk
  - [ ] Check if 'new subscriber mail' is received by info@
  - [ ] Check if newsletter mail is not received if subscribtion is not confirmed
  - [ ] Check if clicking the confirm-subscription links updates the subscribtionConfirmed field in the database
  - [ ] Check if clicking the confirm-subscription redirects to the subscribtion confirmed page, which is displayed well formatted
  - [ ] Check if newsletter mail is received if subscribtion is confirmed
  - [ ] Check if newsletter mail is well formatted
  - [ ] Check if newsletter mail is not shown as spam / junk
  - [ ] Check if clicking the links inside the mail redirect to the new blog-post
  - [ ] Check if clicking the links increments the clickCounter field in database
  - [ ] Check if clicking the unsubscription link removes mail-address from database
  - [ ] Check if clicking the unsubscription links updates the unSubscribed field in the database
  - [ ] Check if clicking the unsubscription link redirects to the unsubscribtion confirmed page, which is displayed well formatted
  - [ ] Check if newsletter mail is received if subscribtion is confirmed
  - [ ] Test the above steps for
    - [x] AOL Mail
    - [x] Gmail.com
    - [x] GMX.de
    - [x] Outlook.com
    - [x] t-online.de
    - [x] web.de
    - [x] yahoo.com
    - [ ] Outlook Desktop Application
    - [ ] Outlook Office 365
    - [ ] Mail Client on IPhone
    - [ ] Mail Client on IPad
    - [ ] Mail Client on Android Phone
    - [ ] Mail Client on Android Tablet
    - [ ] Thunderbird
    - [ ] Firefox
    - [ ] Google Chrome
    - [ ] Opera
    - [ ] Microsoft Internet Explorer
    - [ ] Microsoft Edge


# v0.2.0
- [ ] test for already existing database entries during prepareNewsletter
- [ ] get newsletterMailID from insert

# vX.Y.Z
- [ ] sent newsletter automatically at a given time
- [ ] remove hardcoded passwords from all source-code
- [ ] add unit-test to test against logo picture cannot be found
- [ ] add unit-test to test against bug : if you create two newsletters with same path the newsletterMail data will have the wrong newsletter ID

## Setup
```
pip3 install python-secrets
cd /etc/OpenSubscribe/
sudo su
git stash
git pull
python3 python/OpenSubscribe.py setup --configFileName config/config_stormy_stories.json
mysql < sql/setupDatabase.sql
cp -v php/Unsubscribe.php /var/www/html/
cp -v php/ConfirmSubscribtion.php /var/www/html/
cp -v php/GoTo.php /var/www/html/
cp -v php/SubscribtionForm.php /var/www/html/wp-content/themes/radcliffe/OpenSubscribe/
cp -v systemd/OpenSubscribeInfoMailD.service /etc/systemd/system/
systemctl daemon-reload
systemctl restart OpenSubscribeInfoMailD.service
systemctl status OpenSubscribeInfoMailD.service
exit
```

### Install dependencies
pip3 install mysql-connector-python

### Fill config.json

Replace `<PUT_YOUR_URL_HERE>` with your website URL in
 - `mail-templates/confirmSubscribtion.html`
 - `mail-templates/confirmSubscribtion.txt`

Replace `<PUT_YOUR_CONFIRM_SUBSCRIBTION_USER_PASSWORD_HERE>` with your password of sql user ConfirmSubscribtionUser in
 - `php/ConfirmSubscribtion.php`

Replace `<PUT_YOUR_SUBSCRIBTION_FORM_USER_PASSWORD_HERE>` with your password of sql user SubscribtionFormUser in
 - `php/SubscribtionForm.php`

Replace `<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>` with your password of sql user SendMailsUser in
 - `python/OpenSubscribe.py`

Replace
 - `<PUT_YOUR_SMTP_SERVER_HERE>` with the domain name of your smtp server
 - `<PUT_YOUR_SMTP_PORT_HERE>` with the port number of your smtp server
 - `<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>` with the mail address shall be used for sending the subscribtion mails
 - `<PUT_YOUR_SENDER_PASSWORD_HERE>` with the password of the mail address shall be used for sending the subscribtion mails

in
 - `python/SendConfirmSubscribtionMails.py`


##  Test SendNewsletter

### Add some subscribers to your database

Add some subscribers to your database, either by using the php form or by manually executing some sql commands

`
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'info+test1@stormy-stories.surf', 'abc10def', 'fed20cba', true, true, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'info+test2@stormy-stories.surf', 'abc11def', 'fed21cba', true, true, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'info+test3@stormy-stories.surf', 'abc12def', 'fed22cba', true, false, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'info+test4@stormy-stories.surf', 'abc13def', 'fed23cba', false, true, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'info+test5@stormy-stories.surf', 'abc14def', 'fed24cba', false, false, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'info+test6@stormy-stories.surf', 'abc15def', 'fed25cba', true, true, false, false);
`

### Prepare Newsletter
Open Terminal navigate to OpenSubscribe directory and execute

1. Execute setup
2. Prepare Newsletter
`
python3 python/OpenSubscribe.py setup --configFileName "config/config_stormy_stories.json"
python3 python/OpenSubscribe.py prepareNewsletter --configFileName "config/config_stormy_stories.json" --path "/home/anon/Desktop/Archived/Hobbys & Projekte/IT/Blog/repos/stormy-stories-newsletter-mails/mails/posts/2017/ireland-irland/11-06-brandon-bay-stradbally"
python3 python/OpenSubscribe.py sendNewsletter --configFileName "config/config_stormy_stories.json"
`
