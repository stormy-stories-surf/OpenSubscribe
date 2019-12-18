
/* create and set database */
DROP DATABASE IF EXISTS OpenSubscribe;
CREATE DATABASE OpenSubscribe;
USE OpenSubscribe;

/* table which stores the subscriber data */
DROP TABLE subscriber;

CREATE TABLE subscriber (
   id INT AUTO_INCREMENT primary key NOT NULL,
   mailaddress text NOT NULL,
   subscribeID text NOT NULL,
   unsubscribeID text NOT NULL,
   confirmationMailSent boolean,
   subscribtionConfirmed boolean
);

/* table which stores the timestamp of the
   last subscribtion to avoid DDOS */
DROP TABLE lastSubscribtion;

CREATE TABLE lastSubscribtion (
   id INT AUTO_INCREMENT primary key NOT NULL,
   timeOfLastSubscribtion text NOT NULL
);

/* CREATE USERS */
DROP USER IF EXISTS 'ConfirmSubscribtionUser'@'localhost'
DROP USER IF EXISTS 'SubscribtionFormUser'@'localhost'
DROP USER IF EXISTS 'SendMailsUser'@'localhost'

CREATE USER 'ConfirmSubscribtionUser'@'localhost' IDENTIFIED BY '<PUT_YOUR_CONFIRM_SUBSCRIBTION_USER_PASSWORD_HERE>';
CREATE USER 'SubscribtionFormUser'@'localhost' IDENTIFIED BY '<PUT_YOUR_SUBSCRIBTION_FORM_USER_PASSWORD_HERE>';
CREATE USER 'SendMailsUser'@'localhost' IDENTIFIED BY '<PUT_YOUR_SEND_MAILS_USER_PASSWORD_HERE>';

/* GRANT ACCESS TO TABLES */
GRANT UPDATE ON OpenSubscribe.subscriber TO 'ConfirmSubscribtionUser'@'localhost’;

GRANT INSERT ON OpenSubscribe.subscriber TO 'SubscribtionFormUser'@'localhost’;
GRANT SELECT ON OpenSubscribe.subscriber TO 'SubscribtionFormUser'@'localhost’;
GRANT SELECT ON OpenSubscribe.lastSubscribtion TO 'SubscribtionFormUser'@'localhost’;

GRANT SELECT ON OpenSubscribe.subscriber TO 'SendMailsUser'@'localhost’;
GRANT UPDATE ON OpenSubscribe.subscriber TO 'SendMailsUser'@'localhost’;