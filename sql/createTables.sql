
/* create and set database */
CREATE DATABASE OpenSubscribe;
USE DATABASE OpenSubscribe;

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

/* GRANT ACCESS TO TABLES */
