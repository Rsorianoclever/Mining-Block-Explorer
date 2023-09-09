# -*- coding: utf-8 -*-
#%% ## Libreias necesarias    
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
#%% ## Ploteo 3D de puntos del modelo de bloques
# Carga el archivo CSV en un DataFrame de pandas
df = pd.read_csv('Bm_ls_2.csv')

# Obtiene las columnas de posición x, y, y z y domain como arreglos numpy
x = df['XC'].to_numpy()
y = df['YC'].to_numpy()
z = df['ZC'].to_numpy()
domain = df['DOMAIN'].to_numpy()

# Define una lista de colores para cada grupo
colors = {'a': 'red', 'b': 'green', 'c': 'blue'}

# Crea una figura 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plotea las coordenadas x, y, z para cada grupo con su respectivo color
for d in set(domain):
    ax.scatter(x[domain == d], y[domain == d], z[domain == d], s=0.1, c=colors[d], label=d)

# Ajusta el tamaño de los ejes
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Agrega una leyenda
ax.legend()

# Activa la interacción con el gráfico
ax.view_init(elev=20, azim=45)
#ax.mouse_init()

# Muestra el gráfico
plt.savefig('Orebody.png',dpi=300, bbox_inches='tight')
plt.show() 

#%% ## Cambiando los tipos de datos y creando un nuevo DF
#print(df.dtypes)
df['RESCAT'] = df['RESCAT'].astype(str)

# Crea una copia del DataFrame original sin las columnas que quieres borrar
columns_to_drop = [1]+ [i for i in range(5,14)] + [i for i in range(24,27)] 
df_2 = df.drop(df.columns[columns_to_drop], axis=1)
#print(df_2.dtypes)
#print(df.dtypes)
a=df_2.describe()
print(df_2.describe())
#%% ## Histogramas de leyes

# Seleccionar las columnas que contienen leyes y sus rangos
leyes1 = {'FE':(0,50),'PB':(0,2),'ZN':(0,35),'CU':(0,4.5),'AG_OPT':(0,7),'AG_GPT':(0,220),'ZNEQ':(0,34)}

# Crear histogramas para cada columna de leyes
for col, rango in leyes1.items():
    
    # Obtener los valores de la columna dentro del rango
    valores = df_2[col][(df_2[col] >= rango[0]) & (df_2[col] < rango[1])]

    # Ajustar una distribución gaussiana a los datos
    kde = gaussian_kde(valores)
    x = np.linspace(rango[0], rango[1], num=500)
    y = kde(x)
    
    # Calcular los bins y frecuencias
    frecuencias, bins = np.histogram(valores, bins=500, range=rango)

   # Graficar el histogram
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(valores, bins=500, range=rango, color='blue', alpha=0.5, density=True)
    #ax.plot(x, y, color='red', label='Distribución ajustada')
    ax.plot(x, y, color='red',linewidth=0.5)
    ax.set_title(f'Histograma de {col}')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Densidad')
    ax.legend()
    # Guardar la figura
    plt.savefig(f'{col}.png',dpi=300, bbox_inches='tight')
    plt.show()

#%% ## Curvas tonelaje Ley

ley2 = {'FE':(0,44.5),'PB':(0,1.7),'ZN':(0.88,31.4),'CU':(0,4.18),'AG_OPT':(0,6.56),'AG_GPT':(0,204.2),'ZNEQ':(0,32.33)}

for col, rango in ley2.items():
    ton = df_2['TON']
    ley3 = df_2[col]
    
    # Obtener los valores de la columna dentro del rango
    ton = df_2['TON']
    ley3 = df_2[col]
    cutoffs = np.linspace(rango[0],rango[1], num=1000)
    tons = []
    for cutoff in cutoffs:
        ton_c = ton[ley3 >= cutoff].sum()
        tons.append(ton_c)

    # Calcular ley media para cada valor de cut off grade
    leyes_medias = []
    for cutoff in cutoffs:
        leyes_c = ley3[ley3 >= cutoff]
        if len(leyes_c) > 0:
            ley_media = np.average(leyes_c, weights=ton[ley3 >= cutoff])
        else:
            ley_media = 0
        leyes_medias.append(ley_media)
    
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax2 = ax1.twinx()
    
    # Graficar curva de tonelaje vs. cut off grade en el eje Y izquierdo
    ax1.plot(cutoffs, tons, color='tab:blue')
    ax1.set_xlabel('Cut off grade')
    ax1.set_ylabel('Tonelaje', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_title(f'Curva de tonelaje y ley media vs. cut off grade {col}')
    
    # Graficar curva de ley media vs. cut off grade en el eje Y derecho
    ax2.plot(cutoffs, leyes_medias, color='tab:red')
    ax2.set_ylabel('Ley media', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    # Guardar la figura
    plt.savefig(f'{col}_ley.png',dpi=300, bbox_inches='tight')
    plt.show()
    
