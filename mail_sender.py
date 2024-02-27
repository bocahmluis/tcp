import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

def kirim_email(subject, pesan, penerima, pengirim_email, password, smtp_server, smtp_port):
    try:
        # konfigurasi
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(pengirim_email, password)

        # Pesan
        msg = MIMEMultipart()
        msg['From'] = pengirim_email
        msg['To'] = ', '.join(penerima)
        msg['Subject'] = subject
        msg.attach(MIMEText(pesan, 'plain'))

        # Kirim
        server.sendmail(pengirim_email, penerima, msg.as_string())

        print("Berhasil dikirim")
    except Exception as e:
        print("Gagal Dikirim:", str(e))
    finally:
        
        server.quit()

def baca_csv(nama_file):
    penerima = []
    with open(nama_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            penerima.append(row[0])  
    return penerima
    
# ambil list dari file csv
nama_file_csv = 'email_tb.csv'

# config
pengirim_email = 'isi_email_pengirim'
password = 'Password_Email'
smtp_server = 'Server_Email'
smtp_port = Port  

# Isi Pesan
subject = 'Text Untuk Subject'
pesan = 'Halo pesan di kirim dari PT ABC, dan daftar list dari file csv'
penerima = baca_csv(nama_file_csv)
kirim_email(subject, pesan, penerima, pengirim_email, password, smtp_server, smtp_port)
