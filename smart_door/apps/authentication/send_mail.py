def sendResetMail(dist_mail, link):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    msg = MIMEMultipart()
    email_username = 'trackerelearning@gmail.com'
    password = 'ElearningTrackerService'
    message = f'Access this link to reset your password: 127.0.0.1:8000/reset_pass/{link}'
    text = MIMEText(message)
    msg['Subject'] = "Reset Password Link"
    msg['From'] = email_username
    msg['To'] = dist_mail
    msg.attach(text)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(email_username, password)
            smtp.sendmail(email_username, dist_mail, msg.as_string())
        except:
            pass