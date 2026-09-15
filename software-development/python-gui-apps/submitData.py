import eldergui
import caregivergui
import PySimpleGUI as pg
import sqlite3

def Submitpage():
        layout=[
            [pg.Text('Submiting into the databases')],
            
            [pg.Button("Submit Elder")],
            [pg.Button("Submit Caregiver")]
            
            ]
        window= pg.Window("Sumbit data", layout,resizable=True,font=('Any 50'))
        #event loop
        while True:
            event,values = window.read()
            if event == "Submit Elder":
                eldergui.ElderSubmit() 
            elif event ==pg.WIN_CLOSED:
                break
            elif event == "Submit Caregiver":
                caregivergui.CaregiverSubmit()
                
            #elif values['-NOFOOD-']:
            #    print("they need food")
                
            #print(values[0])
            #list_of_names.append(values[0])
            
    # print(list_of_names)
        window.close()
        
        
#Submitpage() 