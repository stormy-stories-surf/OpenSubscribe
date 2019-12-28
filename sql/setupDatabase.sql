
/* create and set database */
DROP DATABASE IF EXISTS OpenSubscribe;
CREATE DATABASE OpenSubscribe;
USE OpenSubscribe;

/* table which stores the subscriber data */
DROP TABLE IF EXISTS subscriber;

CREATE TABLE subscriber (
   id INT AUTO_INCREMENT primary key NOT NULL,
   mailaddress text NOT NULL,
   subscribeID text NOT NULL,
   unsubscribeID text NOT NULL,
   confirmationMailSent boolean,
   subscribtionConfirmed boolean,
   unSubscribed boolean,
   unSubscribedMailSent boolean
);

/* table which stores the timestamp of the
   last subscribtion to avoid DDOS */
DROP TABLE IF EXISTS lastSubscribtion;

CREATE TABLE lastSubscribtion (
   id INT AUTO_INCREMENT primary key NOT NULL,
   timeOfLastSubscribtion text NOT NULL
);

/* CREATE USERS */
DROP USER IF EXISTS 'ConfirmSubscribtionUser'@'localhost';
DROP USER IF EXISTS 'SubscribtionFormUser'@'localhost';
DROP USER IF EXISTS 'SendMailsUser'@'localhost';
DROP USER IF EXISTS 'UnsubscribeUser'@'localhost';

CREATE USER 'ConfirmSubscribtionUser'@'localhost' IDENTIFIED BY 'TfLtK36uNteCBGhR8Bx9CNfP6tgNw6DXpy3vfVDJSXmyGvuxBLQNivCXP8cb4S8f';
CREATE USER 'SubscribtionFormUser'@'localhost' IDENTIFIED BY 'qKRDZBx3pKajwahSkZxarSYViTPSAprY3nHwn5P7MSPHnDQE35YGXKpVWUq4KR9n';
CREATE USER 'SendMailsUser'@'localhost' IDENTIFIED BY '2rdhVmePV3uZ7GqEWEWXRWekCXSrwSrHbSkvqksWbsDMeqr8jwAxsDT9VSKEqDQh';
CREATE USER 'UnsubscribeUser'@'localhost' IDENTIFIED BY 'LJ5jF8jGhkedA4Vn7xqADu37zFSZSJKc6jPvLwrHUY6geuNyaLogw2s324nUWvMC';

/* GRANT ACCESS TO TABLES */
GRANT UPDATE ON OpenSubscribe.subscriber TO 'ConfirmSubscribtionUser'@'localhost';
GRANT SELECT ON OpenSubscribe.subscriber TO 'ConfirmSubscribtionUser'@'localhost';

GRANT INSERT ON OpenSubscribe.subscriber TO 'SubscribtionFormUser'@'localhost';
GRANT SELECT ON OpenSubscribe.subscriber TO 'SubscribtionFormUser'@'localhost';
GRANT SELECT ON OpenSubscribe.lastSubscribtion TO 'SubscribtionFormUser'@'localhost';

GRANT SELECT ON OpenSubscribe.subscriber TO 'SendMailsUser'@'localhost';
GRANT UPDATE ON OpenSubscribe.subscriber TO 'SendMailsUser'@'localhost';

GRANT UPDATE ON OpenSubscribe.subscriber TO 'UnsubscribeUser'@'localhost';
GRANT SELECT ON OpenSubscribe.subscriber TO 'UnsubscribeUser'@'localhost';
