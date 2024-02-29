import os
import requests
import csv
import re
import time

def cari_url(nama_pt):
    try:
        
        api_key = 'AIzaSyDtZB7i3tmq2wAlaOc0pY1hzsNol7v8jMg'
        search_engine_id = 'b6d88b063427d4849'
        api_endpoint = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={nama_pt.replace(' ', '+')}"
        respons = requests.get(api_endpoint)
        time.sleep(1)
        
        # Cek
        if respons.status_code == 200:
            data = respons.json()
            
            # url awal
            if 'items' in data:
                hasil_awal = data['items'][0]
                url_pt = hasil_awal['link']
                return url_pt
            else:
                print("URL pt tidak ditemukan.")
                return None
        else:
            print("Gagal request API:", respons.status_code)
            return None
    except Exception as e:
        print("kesalahan pencarian PT:", str(e))
        return None

def cari_telephone(url_pt):
    try:
        # cari info di dalam web berdasarkan url
        respons_pt = requests.get(url_pt)
        teks_pt = respons_pt.text
        
        # cari email
        format_email = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        hasil_email = format_email.search(teks_pt)
        
        if hasil_email:
            email_pt = hasil_email.group(0)
        else:
            email_pt = None

        # telephone
        kode_telp = re.compile(r'tel:\+[\d\s()-]+')
        hasil_telp = kode_telp.search(teks_pt)
        
        if hasil_telp:
            telepon_pt = hasil_telp.group(0)
        else:
            telepon_pt = None
        
        return email_pt, telepon_pt
    except Exception as e:
        print("Terjadi kesalahan saat mencari informasi kontak pt:", str(e))
        return None, None

def cari_info(nama_pt):
    try:
        
        url_pt = cari_url(nama_pt)
        
        if url_pt:
            print("URL pt:", url_pt)
            
            # Mencari informasi kontak pt
            email_pt, telepon_pt = cari_telephone(url_pt)
            if email_pt:
                print("Email:", email_pt)
            else:
                print("Email tidak ditemukan.")
                
            if telepon_pt:
                print("Nomor telepon:", telepon_pt)
            else:
                print("Nomor telepon kosog.")
                
            # Mengembalikan data pt
            return [nama_pt, url_pt, email_pt, telepon_pt]
        else:
            print("URL tidak ditemukan.")
            return [nama_pt, None, None, None]
    except Exception as e:
        print("Terjadi kesalahan:", str(e))
        return [nama_pt, None, None, None]

# Fungsi untuk membaca data dari file CSV
def baca_data_csv(nama_file):
    data_csv = []
    try:
        # Dapatkan path absolut ke file CSV
        path_csv = os.path.join(os.path.dirname(__file__), nama_file)
        
        # Buka file CSV dan baca data
        with open(path_csv, 'r') as file:
            pembaca = csv.reader(file)
            next(pembaca)  
            for baris in pembaca:
                nama_pt = baris[0]  
                data_csv.append(cari_info(nama_pt))
    except Exception as e:
        print("file csv gagal di baca/load:", str(e))
    return data_csv

# buat file output
def tulis_data_csv(data, nama_file):
    try:
        path_csv = os.path.join(os.path.dirname(__file__), nama_file)
        
        with open(path_csv, 'w', newline='') as file:
            write = csv.writer(file)
            write.writerow(['Nama pt', 'URL', 'Email', 'Telp'])
            write.writerows(data)
        print(f"Export hasil ke {nama_file}")
    except Exception as e:
        print("Eror :", str(e))

nama_csv = 'data_pt.csv'  
data_csv = baca_data_csv(nama_csv)

export_ke_csv = 'hasil.csv'
tulis_data_csv(data_csv, export_ke_csv)
