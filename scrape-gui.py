import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
from io import BytesIO
import PySimpleGUI as sg
import cairosvg
import logging

# logging.basicConfig(filename='scraping_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_layout():
    layout = [
        [sg.Text('URL', size=(15, 1)), sg.InputText(key='-URL-', size=(30, 1))],
        [sg.Checkbox('Login', key='-LOGIN-', change_submits=True)],
        [sg.Text('Login URL', size=(15, 1)), sg.InputText(key='-URLLOGIN-', size=(30, 1), disabled=True)],
        [sg.Text('Username', size=(15, 1)), sg.InputText(key='-USERNAME-', size=(30, 1), disabled=True)],
        [sg.Text('Password', size=(15, 1)), sg.InputText(key='-PASSWORD-', password_char='*', size=(30, 1), disabled=True)],
        [sg.Text('Save Path', size=(15, 1)), sg.InputText(key='-SAVEPATH-', size=(30, 1)),
         sg.FolderBrowse('Browse', target='-SAVEPATH-')],
        [sg.Button('Submit'), sg.Button('Exit')]
    ]
    return layout

import logging

def scrape_and_save(url, username, password, save_path, urllogin):
    logging.basicConfig(filename='scrape_log.txt', level=logging.ERROR)  # Menyimpan log ke file

    try:
        # Lakukan proses login jika username dan password tidak kosong
        if username and password:
            login_payload = {'username': username, 'password': password}
            login_url = urllogin  # Ganti dengan URL login yang sesuai

            # Lakukan login menggunakan session
            with requests.Session() as session:
                login_response = session.post(login_url, data=login_payload, verify=False)

                # Periksa apakah login berhasil
                if login_response.status_code != 200:
                    print(f'Gagal login. Kode status: {login_response.status_code}')
                    return

                # Setelah login berhasil, lanjutkan dengan scraping menggunakan session yang sudah di-login
                response = session.get(url)
        else:
            # Jika tidak ada login yang diperlukan, lanjutkan dengan scraping tanpa login
            response = requests.get(url)

        # Mengecek apakah permintaan berhasil
        if response.status_code == 200:
            # Menggunakan BeautifulSoup untuk parsing halaman
            soup = BeautifulSoup(response.text, 'html.parser')

            # Sisanya sama seperti yang sebelumnya...
            links = soup.find_all('a')
            images = soup.find_all('img')

            # Menyimpan tautan ke dalam list
            link_list = [link.get('href') for link in links]

            # Membuat DataFrame untuk tautan
            df_links = pd.DataFrame({'Links': link_list})

            # Menyimpan DataFrame tautan ke dalam file Excel
            df_links.to_excel(os.path.join(save_path, 'links_output.xlsx'), index=False)
            print('Data tautan berhasil disimpan ke dalam file Excel.')

            # Menyimpan gambar ke dalam folder lokal
            for img_index, img in enumerate(images):
                img_url = img.get('src')

                if img_url.startswith('data:image'):
                    logging.info(f'URL gambar ke-{img_index}: {img_url}')
                    # Mendapatkan tipe gambar dan data base64 dari URL
                    img_type, img_data = img_url.split(';base64,')
                    img_type = img_type.split(':')[-1]

                    # Mendekode data base64
                    img_data_decoded = base64.b64decode(img_data)

                    # Membuat nama file gambar
                    img_name = f'image_{img_index}'

                    img_content_type = img_response.headers.get('Content-Type')
                    img_ext = img_content_type.split('/')[-1] if img_content_type else 'jpg'

                    img_ext = ''.join(char for char in img_ext if char.isalnum() or char in ['.', '-'])

                    if img_ext.lower() == 'plain':
                        # Jika ekstensi adalah plain, simpan sebagai file SVG
                        svg_content = img_data_decoded.decode('utf-8')

                        output_path = os.path.join(save_path, f'{img_name}.png')
                        try:
                            cairosvg.svg2png(bytestring=svg_content, write_to=output_path)
                            print(f'Gambar {img_name} berhasil diunduh sebagai file PNG.')
                        except Exception as svg_conversion_error:
                            print(f'Gagal mengonversi SVG ke PNG: {str(svg_conversion_error)}')
                            # Logging kesalahan konversi SVG ke PNG
                            logging.error(f'Gagal mengonversi SVG ke PNG: {str(svg_conversion_error)}')
                    elif img_ext.lower() == 'svg':
                        svg_content = img_data_decoded.decode('utf-8')
                        output_path = os.path.join(save_path, f'{img_name}.png')
                        try:
                            cairosvg.svg2png(bytestring=svg_content, write_to=output_path)
                            print(f'Gambar {img_name} berhasil diunduh dan dikonversi ke PNG.')
                        except Exception as svg_conversion_error:
                            print(f'Gagal mengonversi SVG ke PNG: {str(svg_conversion_error)}')
                            # Logging kesalahan konversi SVG ke PNG
                            logging.error(f'Gagal mengonversi SVG ke PNG: {str(svg_conversion_error)}')
                    else:
                        # Jika bukan SVG atau plain, simpan seperti biasa
                        with open(os.path.join(save_path, f'{img_name}.{img_ext}'), 'wb') as img_file:
                            img_file.write(img_data_decoded)
                        print(f'Gambar {img_name} berhasil diunduh.')

                else:
                    # Jika bukan data URI, lakukan seperti yang telah Anda lakukan sebelumnya
                    img_response = requests.get(img_url, stream=True)

                    if img_response.status_code == 200:
                        # Mendapatkan nama file dari URL gambar
                        img_name = f'image_{img_index}.jpg'  # Ganti ekstensi sesuai dengan tipe gambar yang diharapkan

                        # Menyimpan gambar ke dalam folder lokal
                        with open(os.path.join(save_path, img_name), 'wb') as img_file:
                            for chunk in img_response.iter_content(chunk_size=128):
                                img_file.write(chunk)
                        print(f'Gambar {img_name} berhasil diunduh.')
                    else:
                        print(f'Gagal mengunduh gambar. Kode status: {img_response.status_code}')
    except Exception as e:
        # Logging kesalahan
        logging.error(f'Terjadi kesalahan: {str(e)}')

    else:
        print(response, response.status_code)

def main():
    sg.theme('LightBlue2')
    window = sg.Window('Web Scrapper', create_layout())

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == '-LOGIN-':
            window['-URLLOGIN-'].update(disabled=not values['-LOGIN-'])
            window['-USERNAME-'].update(disabled=not values['-LOGIN-'])
            window['-PASSWORD-'].update(disabled=not values['-LOGIN-'])

        if event == 'Submit':
            url = values['-URL-']
            login_enabled = values['-LOGIN-']
            urllogin = values['-URLLOGIN-'] if login_enabled else None
            username = values['-USERNAME-'] if login_enabled else None
            password = values['-PASSWORD-'] if login_enabled else None
            save_path = values['-SAVEPATH-']

            # Panggil fungsi scrape_and_save dengan parameter yang sesuai
            scrape_and_save(url, username, password, save_path, urllogin)

            sg.popup('Scraping completed!')

    window.close()

if __name__ == '__main__':
    main()
