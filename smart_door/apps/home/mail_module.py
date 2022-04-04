def alert_admin(admin_email, subject, message, image_paths):
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
    for image_name in image_paths:
        with open(image_paths[image_name], 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name=image_name)
        msg.attach(image)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(email_username, password)
            smtp.sendmail(email_username, admin_email, msg.as_string())
        except:
            pass