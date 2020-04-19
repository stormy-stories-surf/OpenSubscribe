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
- [ ] implement OpenSubscribe --sendNewsletter
- [ ] test OpenSubscribe --sendNewsletter
- [ ] get newsletterMailID from insert

# v0.2.0
- [ ] test for already existing database entries during prepareNewsletter

# vX.Y.Z
- [ ] sent newsletter automatically at a given time
- [ ] remove hardcoded passwords from all source-code
- [ ] add unit-test to test against logo picture cannot be found

## Setup
```
pip3 install python-secrets
cd /etc/OpenSubscribe/
sudo su
git stash
git pull
python3 python/OpenSubscribe.py --configFileName config/config_stormy_stories.json setup
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
