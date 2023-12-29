import PySimpleGUI as sg

def create_layout():
    layout = [
        [sg.Text('URL', size=(15, 1)), sg.InputText(key='-URL-', size=(30, 1))],
        [sg.Checkbox('Login', key='-LOGIN-', change_submits=True)],
        [sg.Text('Username', size=(15, 1)), sg.InputText(key='-USERNAME-', size=(30, 1), disabled=True)],
        [sg.Text('Password', size=(15, 1)), sg.InputText(key='-PASSWORD-', password_char='*', size=(30, 1), disabled=True)],
        [sg.Text('Save Path', size=(15, 1)), sg.InputText(key='-SAVEPATH-', size=(30, 1)),
         sg.FolderBrowse('Browse', target='-SAVEPATH-')],
        [sg.Button('Submit'), sg.Button('Exit')]
    ]
    return layout

def main():
    sg.theme('LightBlue2')
    window = sg.Window('Web Scraping Form', create_layout())

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == '-LOGIN-':
            window['-USERNAME-'].update(disabled=not values['-LOGIN-'])
            window['-PASSWORD-'].update(disabled=not values['-LOGIN-'])

        if event == 'Submit':
            url = values['-URL-']
            login_enabled = values['-LOGIN-']
            username = values['-USERNAME-'] if login_enabled else None
            password = values['-PASSWORD-'] if login_enabled else None
            save_path = values['-SAVEPATH-']

            # Lakukan tindakan scraping web di sini
            # (Anda dapat menggunakan library seperti BeautifulSoup atau Selenium)

            sg.popup('Scraping completed!')

    window.close()

if __name__ == '__main__':
    main()
