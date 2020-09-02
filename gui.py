import PySimpleGUI as sg

from dbfunctions import *
from guifunctions import formatdatatable, tables

sg.theme('defaultnomorenagging')


def generateguicontent():
    data = formatdatatable()
    headings = ["Organisasjonsnummer", "Organisasjonsnavn", "Organisasjonsform", "Karakter"]
    layout = createlayout(data, headings)
    createwindow(data, layout)


def createlayout(data, headings):
    layout = [[sg.Table(values=data[0:][:], headings=headings, max_col_width=25,
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='middle',
                        num_rows=20,
                        alternating_row_color='light gray',
                        key='-TABLE-',
                        row_height=35, )],
              [sg.Button('Gi karakter'), sg.Button("Søk"), sg.Button("Vis alt databaseinnhold"), sg.Button("Nullstill database"),
               sg.Button("Last inn organisasjoner")]]
    return layout


def createwindow(data, layout):
    window = sg.Window('Oppgave', layout)
    eventloop(window, data)


def eventloop(window, data):
    while True:
        event, values = window.read()
        # print(event, values)

        if event == sg.WIN_CLOSED:
            break

        elif event == 'Gi karakter':
            popupInput = sg.popup_get_text('Gi organisasjonen en karakter fra 1 til 5.', 'Gi karakter')
            try:
                popupInput = int(popupInput)
            except:
                sg.popup("Feilmelding", "Skriv et tall mellom 1-5.")
                continue
            if popupInput not in [1, 2, 3, 4, 5]:
                sg.popup("Feilmelding", "Skriv et tall mellom 1-5.")
                continue
            try:
                t = str(values["-TABLE-"])[1:-1]
                t = int(t)
            except Exception as E:
                print(E)
                sg.popup("Feilmelding", "Velg en rad.")
                continue

            orgnumber = (data[t][0])
            updategrade(orgnumber, popupInput)

            # print(data[1])
            if verifygrade(orgnumber, popupInput):
                data[t][3] = popupInput
                window.FindElement("-TABLE-").Update(data)
            else:
                continue

        elif event == "Nullstill database":
            yesno = sg.popup_yes_no("Er du sikker på at du vil nullstille databasen?")  # Shows Yes and No buttons
            if yesno == "Yes":
                reset()
                data = ""
                window.FindElement("-TABLE-").Update(data)
            else:
                continue

        elif event == "Last inn organisasjoner":
            filldatabase()
            data = formatdatatable()
            #print(data)
            window.FindElement("-TABLE-").Update(data)

        elif event == "Søk":
            valg = getcolumnnames()
            layout2 = [[sg.Combo(valg, key="IN1"),
                        sg.Input(do_not_clear=True,  key="IN2")],
                       [sg.Button('Show'), sg.Button('Exit')]
                       ]

            window2 = sg.Window('Søkemeny').Layout(layout2)

            event, values = window2.Read()
            if event == "Exit":
                window2.Close()
            elif event == "Show":
                # print(values)
                try:
                    input1 = values["IN1"]
                    input2 = values["IN2"]
                    rows = search(input1, input2)
                    data = tables(rows, num_rows=len(rows), num_cols=4)
                    # print(data)
                    window.FindElement("-TABLE-").Update(data)
                    window2.Close()
                except Exception as E:
                    print(E)
                    sg.popup("Feilmelding", "Fyll inn informasjonen.")
                    window2.Close()


        elif event == "Vis alt databaseinnhold":
            data = formatdatatable()
            window.FindElement("-TABLE-").Update(data)

    window.close()


if __name__ == '__main__':
    filldatabase()
    generateguicontent()
