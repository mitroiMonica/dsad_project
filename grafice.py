import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def box_plot(data):
    if isinstance(data, pd.Series):
        sns.set(style="darkgrid")
        sns.boxplot(data)


# mat - matricea de corelatie
# den_var - lista a denumirilor variabilelor
# titlu - titlul ferestrei si al graficuliui
# zec - numar de zecimale
# val_min - valoarea minima care sa fie reprezentata pe corelograma
# val_max - valoarea maxima care sa fie reprezentata pe corelograma
def corelograma(mat, titlu="Corelograma", zec=2, val_min=-1, val_max=1, den_var=None):
    if isinstance(mat, np.ndarray):
        plt.figure(num=titlu, figsize=(10, 10))
        plt.title(label=titlu,
                  fontdict={'fontsize': 17, 'fontweight': 'bold', 'verticalalignment': 'baseline',
                            'horizontalalignment': 'center', 'color': 'purple'})
        if den_var == None:
            den_var = ['V' + str(i) for i in range(mat.shape[1])]
        sns.heatmap(data=np.round(mat, zec), annot=True, cmap='bwr',
                    vmin=val_min, vmax=val_max, linewidths=0.5,
                    xticklabels=den_var, yticklabels=den_var)  # etichete axa x respectiv axa y

    elif isinstance(mat, pd.DataFrame):
        plt.figure(num=titlu, figsize=(10, 10))
        plt.title(label=titlu,
                  fontdict={'fontsize': 15, 'fontweight': 'bold', 'verticalalignment': 'baseline',
                            'horizontalalignment': 'center', 'color': 'purple'})
        sns.heatmap(data=np.round(mat, zec), annot=True, cmap='bwr',
                    vmin=val_min, vmax=val_max, linewidths=0.5)


# sursa bibliografica: https://www.statology.org/population-pyramid-python/
def population_pyramid(serie_masc, serie_fem):
    if isinstance(serie_masc, pd.Series) and isinstance(serie_fem, pd.Series):
        x_masc = serie_masc.values
        x_fem = serie_fem.values
        obs = range(0, serie_masc.shape[0])
        # print(x_masc, x_fem)
        fig, axes = plt.subplots(ncols=2,
                                 sharey=True)  # sharey este pentru a utiliza aceleasi axe pentru ambele grafice
        axes[0].barh(obs, x_masc, align='center', color='royalblue')
        axes[0].set(title='Barbati')
        axes[1].barh(obs, x_fem, align='center', color='lightpink')
        axes[1].set(title='Femei')

        axes[1].grid()
        axes[0].set(yticks=obs, yticklabels=serie_masc.index)
        axes[0].invert_xaxis()
        axes[0].grid()


def bar_plot(data, titlu="Grafic bare"):
    if isinstance(data, pd.Series):
        inaltime = data.values
        bars = data.index
        x_poz = np.arange(len(bars))  # coordonatele barelor
        plt.bar(x_poz, height=inaltime)  # creare bare
        plt.xticks(x_poz, bars)  # creare etichete
        plt.title(label=titlu,
                  fontdict={'verticalalignment': 'baseline'})
    elif isinstance(data, pd.DataFrame):
        serie = pd.Series(data=data.iloc[:, 0])  # desenare doar prima variabila
        bar_plot(serie, titlu)


def afisare():
    plt.show()
