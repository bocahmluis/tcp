import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

def kirim_email(subject, pesan, penerima, pengirim_email, password, smtp_server, smtp_port):
    try:
        # Setup
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(pengirim_email, password)

       
        msg = MIMEMultipart()
        msg['From'] = pengirim_email
        msg['To'] = ', '.join(penerima)
        msg['Subject'] = subject
        msg.attach(MIMEText(pesan, 'plain'))

        # Kirim
        server.sendmail(pengirim_email, penerima, msg.as_string())

        print("Berhasil dikirim")
    except Exception as e:
        print("Gagal Mengirim:", str(e))
    finally:
        
        server.quit()

def baca_csv(nama_file):
    penerima = []
    with open(nama_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            penerima.append(row[0])  
    return penerima

nama_file_csv = 'email_tb.csv'

# config
pengirim_email = 'bocah@smknusa.com'
password = 'sukses.2024'
smtp_server = 'mail.smknusa.com'
smtp_port = 26  

# Isi Pesan
subject = 'Penawaran PT TCP  - 5'
pesan = 'Halo pesan di kirim dari PT TCP, dan daftar list dari file csv'
penerima = baca_csv(nama_file_csv)
kirim_email(subject, pesan, penerima, pengirim_email, password, smtp_server, smtp_port)
