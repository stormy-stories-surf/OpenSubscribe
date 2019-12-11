# OpenSubscribe
A python and php implementation of a tooling for handling E-Mail subscribtions / newsletters on your website.

**PROJECT STATUS : IN DEVELOPMENT**
<img src="docs/pictures/UnderConstructionIcon.png" width="20%">
## Setup
Replace `https://yourURL.com` with your website URL in
 - `mail-templates/confirmSubscribtion.html`
 - `mail-templates/confirmSubscribtion.txt`

Replace `<PUT_YOUR_PASSWORD_HERE>` with your password in
 - `php/ConfirmSubscribtion.php`
 - `php/SubscribtionForm.php`
 - `python/OpenSubscribe.py`
 - `python/SendConfirmSubscribtionMails.py`

Replace
 - `<PUT_YOUR_SMTP_SERVER_HERE>` with the domain name of your smtp server
 - `<PUT_YOUR_SMTP_PORT_HERE>` with the port number of your smtp server
 - `<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>` with the mail address shall be used for sending the subscribtion mails
 - `<PUT_YOUR_SENDER_PASSWORD_HERE>` with the password of the mail address shall be used for sending the subscribtion mails

in
 - `python/SendConfirmSubscribtionMails.py`
