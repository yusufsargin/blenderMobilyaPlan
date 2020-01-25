import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Send:
    def __init__(self, To, ImgFolder, name):
        self.To = 'sarginlar@gmail.com'
        self.ImgFolder = ImgFolder
        self.From = 'yusufsargin9@gmail.com'
        self.Name = name

    def sendEmail(self):
        print('ELEMENT ' + self.To, self.ImgFolder, self.Name)

        img_data = open(self.ImgFolder, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Teşekkür Ederiz.'
        msg['From'] = self.To
        msg['To'] = self.From

        text = MIMEText("Teşekkür Ederiz.")
        msg.attach(text)
        image = MIMEImage(img_data, name=self.Name)
        msg.attach(image)

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login('yusufsargin9@gmail.com', 'sargin_900')
        s.sendmail(self.From, self.To, msg.as_string())
        s.quit()
