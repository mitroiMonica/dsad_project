import numpy as np
import pandas as pd
import grafice as gf
import functii as fu

# PROIECT REALIZAT DE MITROI DANIELA MONICA

# Obtinerea datelor despre infrastructura educatiei in Romania din fisiere csv:

sali_clasa_df = pd.read_csv("./DataIN/sali_de_clasa.csv", index_col=0)
# print(sali_clasa_df)

ateliere_df = pd.read_csv("./DataIN/ateliere.csv", index_col=0)
# print(ateliere_df)

laboratoare_df = pd.read_csv("./DataIN/laboratoare.csv", index_col=0)
# print(laboratoare_df)

pc_df = pd.read_csv("./DataIN/pc-uri.csv", index_col=0)
# print(pc_df)

sali_gimnastica_df = pd.read_csv("./DataIN/sali_de_gimnastica.csv", index_col=0)
# print(sali_gimnastica_df)

terenuri_sport_df = pd.read_csv("./DataIN/terenuri_de_sport.csv", index_col=0)
# print(terenuri_sport_df)

infrastructura_invatamant_df = sali_clasa_df.merge(right=ateliere_df, on="Judete") \
    .merge(right=laboratoare_df, right_index=True, left_index=True) \
    .merge(right=pc_df, left_on="Judete", right_on="Judete") \
    .merge(right=sali_gimnastica_df, on="Judete") \
    .merge(right=terenuri_sport_df, how="inner", on="Judete")
print(infrastructura_invatamant_df)

# Salvare tabel cu infrastructura invatamantului intr-un fisier csv:
infrastructura_invatamant_df.to_csv("./DataOUT/infrastructura.csv")

# Preluarea altor date relevante despre educatia in Romania:

personal_didactic_df = pd.read_csv("./DataIN/personal_didactic.csv", index_col="Judete")
# print(personal_didactic_df)

populatie_scolara_df = pd.read_csv("./DataIN/populatia_scolara.csv", index_col="Judete")
# print(populatie_scolara_df)

unitati_invatamant_df = pd.read_csv("./DataIN/unitati_de_invatamant.csv", index_col="Judete")
# print(unitati_invatamant_df)

alte_detalii_df = personal_didactic_df.merge(right=populatie_scolara_df, on="Judete") \
    .merge(right=unitati_invatamant_df, left_on="Judete", right_index=True)
print(alte_detalii_df)

# Salvare tabel cu detaliile suplimenatre intr-un fisier csv:
alte_detalii_df.to_csv("./DataOUT/detalii_supl.csv")

tabel_educatie_df = infrastructura_invatamant_df.merge(right=alte_detalii_df, on="Judete")
print(tabel_educatie_df)

# Salvare tabel cu toate elementele despre educatie intr-un fisier Excel:
tabel_educatie_df.to_excel("./DataOUT/date_educatie.xlsx", sheet_name="EducatieRO")

denumire_judete = tabel_educatie_df.index.values  # ndarray
numar_judete = denumire_judete.shape[0]
print("Judete: ", denumire_judete, "\nNumar de judete: ", numar_judete)

denumire_variabile = tabel_educatie_df.columns.values
numar_variabile = denumire_variabile.shape[0]
print("Variabile: ", denumire_variabile, "\nNumar de variabile: ", numar_variabile)

# Crearea unei serii pe baza unui dataFrame unidemensional

# print(unitati_invatamant_df.T.values[0])
unit_inv_serie = pd.Series(data=unitati_invatamant_df.T.values[0], index=denumire_judete, name="Unitati de invatamant")
# print(unit_inv_serie)

# Masurarea tendintei centrale:
# Media unitatilor de invatamant in Romania pe judete:
medie_unit_inv = unit_inv_serie.agg(func=np.mean)
print("MEDIE: ", medie_unit_inv)

# Verificare daca media este reprezentativa:
fu.coef_variatie(unit_inv_serie)

# Deoarece media nu este reprezentativa vom elimina din serie outliers
# Identificare outliers:
# 1. Box-plot:
gf.box_plot(unit_inv_serie)
# gf.afisare()

# 2. Regula lui Cebasev:
stdev_unit_inv = unit_inv_serie.agg(func=np.std)
lim_sup = medie_unit_inv + 3 * stdev_unit_inv
lim_inf = medie_unit_inv - 3 * stdev_unit_inv

dict_outliers = {}
for i in range(unit_inv_serie.shape[0]):
    if unit_inv_serie.values[i] <= lim_inf or unit_inv_serie.values[i] >= lim_sup:
        dict_outliers[unit_inv_serie.index[i]] = unit_inv_serie.values[i]
print("Outliers: ", dict_outliers)

# Eliminare outliers:
unit_inv_serie_nou = unit_inv_serie.drop(labels=dict_outliers.keys())
# print(unit_inv_serie_nou)

fu.coef_variatie(unit_inv_serie_nou)  # de aceasta data media este reprezentativa

medie_reprezentativa = unit_inv_serie_nou.agg(func=np.mean)
print("MEDIE (noua): ", medie_reprezentativa)

# Creare dictionar pe baza numarului de unitati de invatamant si a mediei reprezentative obtinute:
dict_unit_inv_med = {}
for i in range(unit_inv_serie_nou.shape[0]):
    if unit_inv_serie_nou.values[i] < medie_reprezentativa:
        dict_unit_inv_med[unit_inv_serie_nou.keys()[i]] = "mai mic"
    else:
        dict_unit_inv_med[unit_inv_serie_nou.keys()[i]] = "mai mare"
for key in dict_outliers.keys():
    dict_unit_inv_med[key] = "Outlier"

for (k, v) in dict_unit_inv_med.items():
    print(k, ': ', v)

# Calcul matrice de covarianta:
mat = tabel_educatie_df.values  # ndarray
mat_cov = np.cov(mat, rowvar=False)
print("Matrice de covarianta:\n", mat_cov)

# Calcul matrice de corelatii:
mat_cor = np.corrcoef(mat, rowvar=False)
print("Matrice de corelatie:\n", mat_cor)
val_min_trunc = np.floor(np.min(mat_cor) * 10) / 10

# Corelograma pe baza unui ndarray:
den_var_scurt = ["cls", "atl", "lbs", "PCs", "gmnst", "ter_spt", "pers_dict", "pop_scl", "unit_inv"]
gf.corelograma(mat_cor, titlu="Corelograma infrastructura educatie", val_min=val_min_trunc, den_var=den_var_scurt)
# gf.afisare()

# Corelograma pe baza unui dataFrame:
corr_df = pd.DataFrame(data=mat_cor, index=den_var_scurt, columns=den_var_scurt)
# print(corr_df)

gf.corelograma(corr_df, val_min=val_min_trunc, titlu="Corelograma educatie")
# gf.afisare()

# Colectare date absolventi universitate (2020):
abs_fem_df = pd.read_excel("./DataIN/absolventi_universitate.xlsx", sheet_name="fem", index_col="Judete")
# print(abs_fem_df.T.values[0])
serie_fem = pd.Series(data=abs_fem_df.T.values[0], index=abs_fem_df.index.values, name="Absolventi de sex feminin")
# print(serie_fem)

abs_masc_df = pd.read_excel("./DataIN/absolventi_universitate.xlsx", sheet_name="masc", index_col="Judete")
# print(abs_fem_df.T.values[0])
serie_masc = pd.Series(data=abs_masc_df.T.values[0], index=abs_fem_df.index.values, name="Absolventi de sex masculin")
# print(serie_masc)

gf.population_pyramid(serie_fem=serie_fem, serie_masc=serie_masc)
# gf.afisare()

# Se observa cum Bucuresti si Cluj sunt outliers, de aceea vedem cum arata si fara aceste orase:
serie_fem.drop(labels=["Municipiul Bucuresti", "Cluj"], inplace=True)
serie_masc.drop(labels=["Municipiul Bucuresti", "Cluj"], inplace=True)

gf.population_pyramid(serie_fem, serie_masc)
# gf.afisare()

# Observarea datelor la nivelul regiunilor si macroregiunilor:
regiuni_df = pd.read_excel("./DataIN/jud_reg_mreg.xlsx", sheet_name="Regiuni", index_col=0)
# print(regiuni_df)

macroregiuni_df = pd.read_excel("./DataIN/jud_reg_mreg.xlsx", sheet_name="Macroregiuni", index_col=0)
# print(macroregiuni_df)

# Date despre educatia in Romania la nivelul regiunilor:
reg_edu_df = tabel_educatie_df.merge(right=regiuni_df, left_index=True, right_index=True) \
    .groupby(by="Regiune").agg(func=np.sum)
# print(reg_edu_df)

# Gasirea regiunilor cu maximul fiecarei variabile:
lista_max_reg = fu.max_el(reg_edu_df)
print(lista_max_reg)  # lista de tupluri
dict_max_reg = {lista_max_reg[i][0]: lista_max_reg[i][2] for i in range(len(lista_max_reg))}
# print(dict_max_reg)
serie_max_reg = pd.Series(data=dict_max_reg)
print(serie_max_reg)

# Creare dataframe pe baza listei cu valori maxime pentru a salva intr-un fisier Excel:
df_max_reg = pd.DataFrame(data=serie_max_reg, columns=["Regiune"])
val_max_lista = [lista_max_reg[i][1] for i in range(len(lista_max_reg))]
df_max_reg["Valoare maxima"] = val_max_lista
# print(df_max_reg)

df_max_reg.to_excel("./DataOUT/val_max_reg.xlsx", sheet_name="Regiuni")

# Numarul mediu de profesori pe unitatea de invatamant la nivelul regiunilor:
nr_mediu_profs = reg_edu_df[["Personal didactic"]] / reg_edu_df[["Unitati de invatamant"]].values
# sau
# nr_mediu_profs = reg_edu_df[["Personal didactic"]].div(reg_edu_df[["Unitati de invatamant"]].values)
print(nr_mediu_profs)

gf.bar_plot(nr_mediu_profs, "Medie profesori pe fiecare unitate de invatamant la nivelul regiunilor")
# gf.afisare()

# Date despre educatia in Romania la nivelul macroregiunilor:
mcrreg_edu_df = reg_edu_df.merge(right=macroregiuni_df, left_index=True, right_index=True) \
    .groupby(by="Macroregiune").agg(func=np.sum)
# print(mcrreg_edu_df)

# Gasirea macroregiunilor cu maximul fiecarei variabile:
lista_max_mreg = fu.max_el(mcrreg_edu_df)
print(lista_max_mreg)  # lista de tupluri
dict_max_mreg = {lista_max_mreg[i][0]: lista_max_mreg[i][2] for i in range(len(lista_max_mreg))}
# print(dict_max_mreg)
serie_max_mreg = pd.Series(data=dict_max_mreg)
print(serie_max_mreg)

# Creare dataframe pe baza listei cu valori maxime pentru a salva intr-un fisier Excel
df_max_mreg = pd.DataFrame(data=serie_max_mreg, columns=["Macroregiune"])
val_max_lista2 = [lista_max_mreg[i][1] for i in range(len(lista_max_mreg))]
df_max_mreg["Valoare maxima"] = val_max_lista2
# print(df_max_mreg)

df_max_mreg.to_excel("./DataOUT/val_max_macroreg.xlsx", sheet_name="Macroregiuni")

# Observarea numarului de absolventi in functie de sex pe regiuni:
nr_fem_reg = abs_fem_df.merge(right=regiuni_df, right_on="Nume Judet", left_on="Judete").groupby(by="Regiune").sum()
nr_masc_reg = abs_masc_df.merge(right=regiuni_df, right_on="Nume Judet", left_on="Judete").groupby(by="Regiune").sum()
reg_fem_serie = pd.Series(data=nr_fem_reg.T.values[0], index=nr_fem_reg.T.columns)
reg_masc_serie = pd.Series(data=nr_masc_reg.T.values[0], index=nr_masc_reg.T.columns)

gf.population_pyramid(serie_fem=reg_fem_serie, serie_masc=reg_masc_serie)
# gf.afisare()

# Pentru o mai buna comparare a datelor acestea se pot standardiza:
X = tabel_educatie_df.values
Xstd = fu.standardizare(X)

mat_cor_std = np.corrcoef(Xstd, rowvar=False)
val_min_tr = np.floor(np.min(mat_cor_std) * 10) / 10
gf.corelograma(mat_cor_std, titlu="Corelograma educatie",val_min=val_min_tr, den_var=den_var_scurt)
gf.afisare()

# OBS: Matricea standardizata va ajuta in analiza componentelor principale
date_std_df = pd.DataFrame(data=Xstd, index=denumire_judete, columns=denumire_variabile)
date_std_df.to_csv("./DataOUT/date_standardizate.csv")
