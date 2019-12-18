import smtplib


def send_email(email, msg):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('rizzmi.test@gmail.com', '123e456123e456')
    smtpObj.sendmail("justkiddingboat@gmail.com", email, msg)
    smtpObj.quit()
