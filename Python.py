import serial
import time
import pandas as pd
import matplotlib.pyplot as plot
from openpyxl import load_workbook

planilha = 'temperatura.xlsx'
try:
    df = pd.read_excel(planilha)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Hora', 'Min', 'Atual', 'Max'])

COM = "COM7"
BandaSerial = 9600
print(f"Tentando conectar com o Arduino... (Porta {COM}, serial {BandaSerial})")

while True:
    try:
        arduino = serial.Serial(COM, BandaSerial)
        print('Arduino conectado com sucesso')
        break
    except:
        pass

while True:
    if arduino.in_waiting > 0:
        entradaSerial = str(arduino.readline())[2:-5].split(';')
        menorTemp = entradaSerial[0]
        temperatura = entradaSerial[1]
        maiorTemp = entradaSerial[2]
        print(f"A temperatura atual é de {temperatura}, com mínima de {menorTemp} e máxima de {maiorTemp}.")
        arduino.flush()
        temperaturaDF = {
        'Hora': pd.Timestamp.now(),
        'Min': int(menorTemp),
        'Atual': int(temperatura),
        'Max': int(maiorTemp)
        }
        linha = pd.DataFrame([temperaturaDF])
        if not linha.isnull().all().all():
            df = pd.concat([df, linha], ignore_index=True)
            df.to_excel(planilha, index=False)

            workbook = load_workbook(planilha)
            sheet = workbook.active
            for column in sheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                sheet.column_dimensions[column[0].column_letter].width = adjusted_width
            workbook.save(planilha)