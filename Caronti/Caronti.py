import shutil
import os
import xlrd
import xlsxwriter
import glob
from tkinter import *
from tkinter import messagebox


# Function to Get the current
# working directory

def aggiornaRetro(file_retro, dict):

    try:
        wb = xlrd.open_workbook(file_retro)
        sh = wb.sheet_by_index(0)
    except:
        return -1

    d = {}
    for i in range(1, sh.nrows):
        cell_value_class = sh.cell(i, 0).value
        cell_value_id = [sh.cell(i, 1).value, sh.cell(i, 2).value]
        d[cell_value_class] = cell_value_id

    for cartella in dict:
        lista = dict[cartella]['Retro']['Lista Retro']
        cartella = float(cartella)
        d.setdefault(cartella, [0, ''])
        for i in lista:
            if i not in d[cartella][1]:
                d[cartella][1] = d[cartella][1] + '  ' + str(i)
                d[cartella][0] = d[cartella][0] + 1

    sort_list = sorted(d.items(), key=lambda x: int(x[0]), reverse=False)

    sort_d = {}

    for x in sort_list:
        sort_d.setdefault(x[0], [x[1][0], x[1][1]])

    workbook = xlsxwriter.Workbook(file_retro)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, sh.cell(0, 0).value)
    worksheet.write(0, 1, sh.cell(0, 1).value)
    worksheet.write(0, 2, sh.cell(0, 2).value)

    r = 1
    for cartella in sort_d:
        worksheet.write(r, 0, int(cartella))
        worksheet.write(r, 1, sort_d[cartella][0])
        worksheet.write(r, 2, sort_d[cartella][1])
        r = r + 1

    try:
        workbook.close()
    except:
        return -2

    return 0


def cerca_corrispondenza(list, member):
    for i in range(len(list)):
        if list[i][0] == member:
            return [True, i]
    return [False, -1]


def smista(picture_path, listname, member, path, filename, dati_smistamento):

    cartella = nome_cartella(member)

    corrispondenza_trovata = cerca_corrispondenza(listname, member)
    if corrispondenza_trovata[0]:

        dati_cartella = dati_smistamento.setdefault(
            cartella, {'Totali': 0, 'Caronti': 0, 'Non Caronti': 0, 'Retro': {'Totali': 0, 'Lista Retro': []}})
        dati_smistamento[cartella]['Totali'] = dati_cartella['Totali'] + 1

        i = corrispondenza_trovata[1]
        sorce_path = os.path.join(picture_path, filename)
        if (listname[i][1].strip() == 'si' or listname[i][1].strip() == 'sì'):

            dati_smistamento[cartella]['Caronti'] = dati_cartella['Caronti'] + 1

            cartellaCaronti = "Caronti" + cartella
            path = os.path.join(path, cartellaCaronti)
            if not os.path.exists(path):
                os.mkdir(path)
            target_path = os.path.join(path, filename)
            shutil.move(sorce_path, target_path)
        elif (listname[i][1].strip() == 'no'):

            dati_smistamento[cartella]['Non Caronti'] = dati_cartella['Non Caronti'] + 1

            target_path = os.path.join(path, filename)
            shutil.move(sorce_path, target_path)

        else:
            return False

        if 'retro' in filename:
            dati_smistamento[cartella]['Retro']['Totali'] = dati_smistamento[cartella]['Retro']['Totali'] + 1
            dati_smistamento[cartella]['Retro']['Lista Retro'].append(
                member[4:].replace('retro', '').lstrip('0'))

    else:
        return False

    return True


def crea_lista_da_exel(loc):
    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    num_file = sheet.nrows
    nomi_file = []
    for n in range(1, num_file):
        filename = sheet.cell_value(n, 0).strip().split(".")[
            0].replace('_', '')
        nomi_file.append([filename, sheet.cell_value(n, 2).strip()])
    return nomi_file


def nome_cartella(filename):
    # le prima 4 lettere sono il numero del cassetto
    if len(filename) > 4:
        cassetto = filename[:4]
        # la cartella è il numero del cassetto senza 0 iniziali
        cartella = cassetto.lstrip("0")
        return cartella
    else:
        return False


def cerca_cartella(desktop_path, cartella):

    if not cartella:
        return False
    else:
        path_cartella = os.path.join(desktop_path, cartella)
        result = os.path.exists(path_cartella)
        if result:
            return path_cartella
        else:
            return False


def main():

    # hide main window
    root = Tk()
    root.withdraw()

    print('Smistamento in corso')

    scansioni = []
    file_non_smistati = []
    exel_file_mancanti = []
    cartelle_mancanti = []
    dati_smistamento = {}

    desktop_path = os.path.join(os.environ["HOMEPATH"], "Desktop")

    picture_path = os.path.join(os.environ["HOMEPATH"], "Pictures")

    for filename in os.listdir(picture_path):
        filename_path = os.path.join(picture_path, filename)

        if os.path.isfile(filename_path):
            scansioni.append(filename)

    scansioni.remove('desktop.ini')

    for filename in scansioni:
        scansione = filename.split(".")[0].replace('_', '')
        cartella = nome_cartella(scansione)
        target_path = cerca_cartella(desktop_path, cartella)
        if target_path:
            loc = target_path + '/' + '*.xlsx'
            exel_file_list = glob.glob(loc)
            if exel_file_list:
                exel_file = exel_file_list[0]
                lista_file = crea_lista_da_exel(exel_file)
                file_smistato = smista(
                    picture_path, lista_file, scansione, target_path, filename, dati_smistamento)
                if not file_smistato:
                    file_non_smistati.append(filename)

            else:
                file_non_smistati.append(filename)
                exel_file = 'Cassetto' + cartella + '.xlsx'
                if exel_file not in exel_file_mancanti:
                    error_message = 'File exel ' + exel_file + ' non trovato!'
                    messagebox.showerror("Error", error_message)
                    exel_file_mancanti.append(exel_file)
        else:
            if cartella not in cartelle_mancanti:
                if cartella:
                    error_message = 'Cartella ' + cartella + ' non presente sul desktop!'
                    messagebox.showerror("Error", error_message)
                    file_non_smistati.append(filename)
                    cartelle_mancanti.append(cartella)

    info_smistamento = 'Smistamento completato con successo!\n\n'

    for cartella in dati_smistamento:
        info_smistamento = info_smistamento + str(dati_smistamento[cartella]['Totali']) + ' file smistati nella cartella ' + str(cartella) + ':\n' + str(
            dati_smistamento[cartella]['Caronti']) + ' attribuiti a Caronti\n' + str(dati_smistamento[cartella]['Non Caronti']) + ' non attribuiti a Caronti\n' + str(dati_smistamento[cartella]['Retro']['Totali']) + ' retro\n\n'

    messagebox.showinfo("Information", info_smistamento)

    stringa_file_non_smistati = "I seguenti file non sono stati smistati :\n"
    if len(file_non_smistati) > 0:
        for filename in file_non_smistati:
            stringa_file_non_smistati = stringa_file_non_smistati + filename + "\n"

        messagebox.showwarning("Warning", stringa_file_non_smistati)

    file_retro = os.path.join(desktop_path, r'Elenco retro.xlsx')
    if (aggiornaRetro(file_retro, dati_smistamento) == 0):
        messagebox.showinfo(
            "Information", 'File retro aggiornato con successo!')
    elif (aggiornaRetro(file_retro, dati_smistamento) == -1):
        messagebox.showerror("Error", 'Errore lettura file retro!')
    elif (aggiornaRetro(file_retro, dati_smistamento) == -2):
        messagebox.showerror("Error", 'Errore scrittura file retro!')


if __name__ == '__main__':

    main()
