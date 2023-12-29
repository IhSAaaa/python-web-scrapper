import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
from io import BytesIO

# URL target
url = 'https://omnihotelier.com/'

# Mengambil halaman web menggunakan requests
response = requests.get(url)

# Mengecek apakah permintaan berhasil
if response.status_code == 200:
    # Menggunakan BeautifulSoup untuk parsing halaman
    soup = BeautifulSoup(response.text, 'html.parser')

    # Menemukan elemen atau data yang ingin Anda ambil
    # Contoh: Mengambil semua tautan dan gambar pada halaman
    links = soup.find_all('a')
    images = soup.find_all('img')

    # Menyimpan tautan ke dalam list
    link_list = [link.get('href') for link in links]

    # Membuat DataFrame untuk tautan
    df_links = pd.DataFrame({'Links': link_list})

    # Menyimpan DataFrame tautan ke dalam file Excel
    df_links.to_excel('links_output.xlsx', index=False)
    print('Data tautan berhasil disimpan ke dalam file Excel.')

    # Menyimpan gambar ke dalam folder lokal
    for img_index, img in enumerate(images):
    img_url = img.get('src')

    # Cek apakah URL gambar adalah data URI
    if img_url.startswith('data:image'):
        # Mendapatkan tipe gambar dan data base64 dari URL
        img_type, img_data = img_url.split(';base64,')
        img_type = img_type.split(':')[-1]

        # Mendekode data base64
        img_data_decoded = base64.b64decode(img_data)
        
        # Membuat nama file gambar
        img_name = f'image_{img_index}.{img_type}'

        # Menyimpan gambar ke dalam folder lokal
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data_decoded)
        print(f'Gambar {img_name} berhasil diunduh.')
    else:
        # Jika bukan data URI, lakukan seperti yang telah Anda lakukan sebelumnya
        img_response = requests.get(img_url, stream=True)

        if img_response.status_code == 200:
            # Mendapatkan nama file dari URL gambar
            img_name = f'image_{img_index}.jpg'  # Ganti ekstensi sesuai dengan tipe gambar yang diharapkan

            # Menyimpan gambar ke dalam folder lokal
            with open(img_name, 'wb') as img_file:
                for chunk in img_response.iter_content(chunk_size=128):
                    img_file.write(chunk)
            print(f'Gambar {img_name} berhasil diunduh.')
        else:
            print(f'Gagal mengunduh gambar. Kode status: {img_response.status_code}')
else:
    print('Gagal mengambil halaman. Kode status:', response.status_code)
