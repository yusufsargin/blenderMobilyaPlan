import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Send:
    def __init__(self, To, ImgFolder, name):
        self.To = To
        self.ImgFolder = ImgFolder
        self.From = 'yusufsargin9@gmail.com'
        self.Name = name

    def sendEmail(self):
        print('ELEMENT ' + self.To, self.ImgFolder, self.Name)

        # img_data = open('D:\\blenderRenderImage\\yusufsargin9@gmail.com_123.png', 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Teşekkür Ederiz.'
        msg['From'] = 'yusufsargin9@gmail.com'
        msg['To'] = ['sarginlar@gmail.com']

        text = MIMEText("Teşekkür Ederiz.")
        msg.attach(text)
        # image = MIMEImage(img_data, name=self.Name)
        # msg.attach(image)

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.starttls()
        s.ehlo()
        s.login('yusufsargin9@gmail.com', 'sargin_966')
        s.sendmail('yusufsargin9@gmail.com', 'sarginlar@gmail.com', msg.as_string())
        s.quit()
