import PySimpleGUI as pg
print(pg)
#pg.theme("DarkAmber")
layout=[
    [pg.Text("Enter name")],
    [pg.InputText()],
    [pg.Button("Ok"), pg.Button("Cancel")]
]
window= pg.Window("Form", layout)
list_of_names=[]
#event loop
while True:
    event,values = window.read()
    if event == "Cancel":
        break
    print(values[0])
    list_of_names.append(values[0])
    
print(list_of_names)
window.close()