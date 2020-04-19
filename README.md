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
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'test1@test.de', '10', '20', true, true, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'test2@test.de', '11', '21', true, true, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'test3@test.de', '12', '22', true, false, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'test4@test.de', '13', '23', false, true, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'test5@test.de', '14', '24', false, false, false, false);
INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed, unSubscribed, unSubscribedMailSent) VALUES (NULL, 'test6@test.de', '15', '25', true, true, false, false);
`

### Prepare Newsletter
Open Terminal navigate to OpenSubscribe directory and execute

1. Execute setup
2. Prepare Newsletter
`
python3 python/OpenSubscribe.py setup --configFileName config/config_stormy_stories.surf
python3 python/OpenSubscribe.py prepareNewsletter --url "https://stormy-stories.surf/2017/irland-2017-brandon-bay-stradbally/" --path "~/Desktop/Archived/Hobbys & Projekte/IT/Blog/repos/stormy-stories-newsletter-mails/mails/posts/2017/ireland-irland/11-06-brandon-bay-stradbally"
`
