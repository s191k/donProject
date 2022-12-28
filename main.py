import random
import string

from donationalerts import Alert
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

personal_token = ""
mail_ru_pochta = ""
mail_ru_app_pass = ""
path_to_pass_file = ""  # or made generation online ?
minimum_expected_amount = 200
expected_currency = "RUB"

alert = Alert(personal_token)

def get_pass_from_file_and_delete(file_path):
    if file_path != "":
        with open(file_path, "r",encoding="utf-8") as file:
            curr_pass = file.readline()
            other_lines = file.readlines()
        with open(file_path, "w",encoding="utf-8") as file:
            file.writelines(other_lines)
    else: #это просто для примера
        curr_pass=''.join(random.choices(string.ascii_uppercase, k=10))

    return curr_pass

#TODO передавать path файла ?
def sent_mail(mail_from,mail_pass,mail_to):
    # create message object instance
    msg = MIMEMultipart()
    message = get_pass_from_file_and_delete(path_to_pass_file)
    # setup the parameters of the message
    password = mail_pass
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = "Data for vpn"
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #create server
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg['To']))

print("apps started")
@alert.event()
def new_donation(event):
    # print(1)
    print(event)
    parsed_amount_of_money = float(event.amount)
    if event.currency == expected_currency and parsed_amount_of_money >= minimum_expected_amount:
        sent_mail(mail_ru_pochta, mail_ru_app_pass,mail_to=event.message)