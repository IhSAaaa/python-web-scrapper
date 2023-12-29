import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL target
url = 'https://omnihotelier.com/'

# Mengambil halaman web menggunakan requests
response = requests.get(url)

# Mengecek apakah permintaan berhasil
if response.status_code == 200:
    # Menggunakan BeautifulSoup untuk parsing halaman
    soup = BeautifulSoup(response.text, 'html.parser')

    # Menemukan elemen atau data yang ingin Anda ambil
    # Contoh: Mengambil semua tautan pada halaman
    links = soup.find_all('a')

    # Menyimpan tautan ke dalam list
    link_list = [link.get('href') for link in links]

    # Membuat DataFrame menggunakan pandas
    df = pd.DataFrame({'Links': link_list})

    # Menyimpan DataFrame ke dalam file Excel
    df.to_excel('output.xlsx', index=False)
    print('Data berhasil disimpan ke dalam file Excel.')
else:
    print('Gagal mengambil halaman. Kode status:', response.status_code)
