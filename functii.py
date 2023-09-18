import numpy as np
import pandas as pd


def coef_variatie(data):
    if isinstance(data, pd.Series):
        medie_unit_inv = data.agg(func=np.mean)
        stdev_unit_inv = data.agg(func=np.std)
        coef_var = (stdev_unit_inv / medie_unit_inv) * 100
        print("Coeficientul de variatie este: " + str(coef_var) + " %")
        if coef_var <= 35:
            print("Seria este omogena, deci media este reprezentativa")
        else:
            print("Seria NU este omogena, deci media NU este reprezentativa")


def max_el(data):
    if isinstance(data, pd.DataFrame):
        lista_max = []
        for i in range(data.columns.shape[0]):
            serie = data.iloc[:, i]
            # print(serie.values)
            nume_var = serie.name
            max_val = np.max(data.iloc[:, i])
            max_index = np.where(serie.values == max_val)  # tuplu
            loc = serie.index[max_index[0][0]]
            # print(nume_var, ": ", max_val, " - ", serie.index[max_index[0][0]])
            tuplu_date = (nume_var, max_val, loc)
            # print(tuplu_date)
            lista_max.append(tuplu_date)
        return lista_max


def standardizare(data):
    if isinstance(data, np.ndarray):
        medii = np.mean(a=data, axis=0)  # medii pe coloane
        abateriSt = np.std(a=data, axis=0)  # abateri standard pe coloane
        data_std = (data - medii) / abateriSt
        return data_std

