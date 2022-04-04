def alert_admin(admin_email, subject, message, image_path):
    from email.message import EmailMessage
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import os
    import smtplib
    msg = MIMEMultipart()
    email_username = 'trackerelearning@gmail.com'
    password = 'ElearningTrackerService'
    text = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email_username
    msg['To'] = admin_email

    msg.attach(text)
    with open(image_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename('cctv_footage'))
    msg.attach(image)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_username, password)
        smtp.sendmail(email_username, admin_email, msg.as_string())