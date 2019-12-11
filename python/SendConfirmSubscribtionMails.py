def main():
    print("python main function")

    s = SubscribtionMgt("<PUT_YOUR_SMTP_SERVER_HERE>", <PUT_YOUR_SMTP_PORT_HERE>, "<PUT_YOUR_SENDER_MAIL_ADDRESS_HERE>", "<PUT_YOUR_SENDER_PASSWORD_HERE>")
    s.smtpLogin()
    
    s.smtpClose()

if __name__ == '__main__':
    main()
