import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv

def kirim_email(subject, pesan, penerima, lampiran=None):
    try:
        # config
        pengirim_email = 'isi_email_pengirim'
        password = 'Password_Email'
        smtp_server = 'Server_Email'
        smtp_port = Port 
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(pengirim_email, password)

        msg = MIMEMultipart()
        msg['From'] = pengirim_email
        msg['To'] = ', '.join(penerima)
        msg['Subject'] = subject

        msg.attach(MIMEText(pesan, 'plain'))

        if lampiran:
            attachment = open(lampiran, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % lampiran)
            msg.attach(part)

        server.sendmail(pengirim_email, penerima, msg.as_string())
        print("Email berhasil dikirim")
    except Exception as e:
        print("Email gagal dikirim:", str(e))
    finally:
        server.quit()

def baca_csv(nama_file):
    penerima = []
    with open(nama_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            penerima.append(row[0])
    return penerima

load_csv = 'email_tb.csv'

subject = 'TES3'
pesan = 'Dikirim dengan file CSV'
lampiran = 'lampiran.pdf' 

penerima = baca_csv(load_csv)
kirim_email(subject, pesan, penerima, lampiran)
