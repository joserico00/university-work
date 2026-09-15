import PySimpleGUI as sg

sg.change_look_and_feel('GreenTan')

layout = [ [sg.Text('Enter distance in Kilometers'), sg.Input(key='-KILO-', do_not_clear=False, size=(5,1))],
           [sg.Text(size=(5,1), justification='right', key='-OUT-KM-'),
            sg.Text('km = '),
            sg.Text(size=(5,1), key='-OUT-MI-'),
            sg.Text('miles')],
           [sg.Button('Convert', bind_return_key=True), sg.Button('Quit')]  ]

window = sg.Window('Kilometer conversion', layout)
# Loop, reading events (button clicks) and getting input field
while True:             # Event Loop
    event, values = window.read()
    if event in (None, 'Quit'):
        break
    window['-OUT-KM-'].Update(values['-KILO-'])
    window['-OUT-MI-'].Update(float(values['-KILO-'])*0.6214)
window.close()