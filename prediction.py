import pandas as pd
import numpy as np      # Importações
import scipy.stats



def ciCalculator(data, confidence, day):

    confidenceAdjusted = 100 - (100 - confidence) / 2

    mean = np.mean(data)
    z = scipy.stats.norm.ppf(confidenceAdjusted / 100)

    std = np.std(data, ddof=1)



    ciMinus = mean - (z * (std / np.sqrt(len(data)))) 
    ciPlus = mean + (z * (std / np.sqrt(len(data)))) 

    print(f'Pode-se dizer com {confidence}% de confiança que o valor para o dia {day} estará entre {round(ciMinus, 3)} e {round(ciPlus, 3)}.')




monday = []
tuesday = []
wednesday = []     # Será usado para estimar os valores os dados de vendas de cada dia da semana
thursday = []
friday = []
saturday = []
sunday = []




data = pd.read_excel(r'Dados.xlsx')


sales = data['Vendas'].tolist() # Lista com todos os valores de vendas dos dias 06/12/2022 até 20/01/2023


stdValues = np.std(sales, ddof=1) # Desvio padrão de amostra


mean = np.mean(sales) # Media dos valores


for x in range(len(sales)):                # Funcao que identifica os outliers (principalmente em feriados) para nao afetar as previsoes para os dias 21-25
    zScore = (sales[x] - mean) / stdValues
    if zScore > 3 or zScore < -1.5:
        sales[x] = -1 #Flag

tempWeekDay = 3 # Primeiro valor da tabela é uma terça-feira



for x in range(len(sales)):

    if sales[x] == -1: 
        tempWeekDay += 1
        if tempWeekDay == 8:
            tempWeekDay = 1
        continue # Exclui outliers da conta

    match tempWeekDay:
        case 1:
            sunday.append(sales[x])
        case 2:
            monday.append(sales[x])
        case 3:
            tuesday.append(sales[x])
        case 4:
            wednesday.append(sales[x])
        case 5:
            thursday.append(sales[x])
        case 6:
            friday.append(sales[x])
        case 7:
            saturday.append(sales[x])
    tempWeekDay += 1
    if tempWeekDay == 8:
        tempWeekDay = 1

confidence = 95 # Para alterar intervalo de confiança, mudar este número

for day in range(21, 26): # Para os dias 21 ate 26, faz a previsao baseado na porcentagem desejada

    match tempWeekDay:
        case 1:
            ciCalculator(sunday, confidence, day)
        case 2:
            ciCalculator(monday, confidence, day)
        case 3:
            ciCalculator(tuesday, confidence, day)
        case 4:
            ciCalculator(wednesday, confidence, day)
        case 5:
            ciCalculator(thursday, confidence, day)
        case 6:
            ciCalculator(friday, confidence, day)
        case 7:
            ciCalculator(saturday, confidence, day)
    tempWeekDay += 1
    if tempWeekDay == 8:
        tempWeekDay = 1




    




