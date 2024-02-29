from flask import Flask, render_template, request, redirect, url_for 
import smtplib #modul u/ kirim email melalui protokol SMTP
from email.mime.multipart import MIMEMultipart # u/ bikin pesan email multipart.
from email.mime.text import MIMEText
import csv # u/ load csv

#buat objek 
app = Flask(__name__)

def kirim_email(subject, pesan, penerima, pengirim_email, password, smtp_server, smtp_port):
    try:
        # setting pengaturan
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(pengirim_email, password)

        # buat pesan/objeck
        msg = MIMEMultipart()
        msg['From'] = pengirim_email
        msg['To'] = ', '.join(penerima)
        msg['Subject'] = subject
        msg.attach(MIMEText(pesan, 'plain'))

        # Kirim
        server.sendmail(pengirim_email, penerima, msg.as_string())

        return True, "Email berhasil dikirim"
    except Exception as e:
        return False, "Gagal mengirim email: " + str(e)
    finally:
        server.quit()

def baca_csv(nama_file):
    penerima = []
    with open(nama_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            penerima.append(row[0])  
    return penerima

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        pesan = request.form['pesan']
        nama_file_csv = 'email_tb.csv'
        pengirim_email = 'bocah@smknusa.com'
        password = 'sukses.2024'
        smtp_server = 'mail.smknusa.com'
        smtp_port = 26
        penerima = baca_csv(nama_file_csv)
        success, message = kirim_email(subject, pesan, penerima, pengirim_email, password, smtp_server, smtp_port)
        if success:
            return redirect(url_for('index', result='success'))
        else:
            return redirect(url_for('index', result='failed', message=message))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
