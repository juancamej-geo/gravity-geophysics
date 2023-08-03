import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from tkinter import filedialog
import os, warnings
warnings.simplefilter('ignore',np.RankWarning)

def grafica(x2, title):
    df= x2
    x = df['x'].values
    y = df['y'].values
    z = df['z'].values

    xi = np.linspace(min(x), max(x), 50)
    yi = np.linspace(min(y), max(y), 50)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((x, y), z, (xi, yi), method='cubic')
                
    plt.contourf(xi, yi, zi, levels=20, cmap='RdYlBu'),plt.colorbar().set_label('mGal'),plt.xlabel('X'), plt.ylabel('Y')
    plt.title(title), plt.show()

def mainmenu():
    global ruta
    ch=input('-'*10+ 'Menú principal'+ '-'*10+ '\nSeleccione una opción:\n1-Leer Archivo\n2-Información del software\n')
    match ch:
        case '1':
            ruta= filedialog.askopenfile(title='Ingrese el archivo', initialdir='C:/Users/PC/Documents',filetypes=[('Archivos Excel','.xlsx')]).name
            leer(ruta)
        case '2':
            input('-'*50+'\nDesarrollado por: Juan C. Mejía\nSoftware de uso académico\nPara más información consulte al correo juan.601823945@ucaldas.edu.co\n'+'-'*50+'\n')
            os.system('cls')
            mainmenu()
        case _:
            os.system('cls')
            input('Ingrese 1 o 2\n')
            os.system('cls')
            mainmenu()


def leer(inb):
    global xi,yi,zi
    if type(inb)== type('esto es un string'):
        df = pd.read_excel(inb)
        print('ok')
    else:
        df=inb
    
    x = df['x'].values
    y = df['y'].values
    z = df['z'].values

    xi = np.linspace(min(x), max(x), 50)
    yi = np.linspace(min(y), max(y), 50)
    xi, yi = np.meshgrid(xi, yi)

    zi = griddata((x, y), z, (xi, yi), method='cubic')
    while True:
        match input('Desea mostrar los puntos cargados?[s/n]\n'):
            case 's':
                plt.scatter(x, y, c='Black')
                plt.show()
                break
            case 'n':
                os.system('cls')
                break
            case _:
                input('Opción no válida.')
                os.system('cls')
                

    plt.contourf(xi, yi, zi, levels=20, cmap='RdYlBu'),plt.colorbar().set_label('mGal'),plt.xlabel('X'), plt.ylabel('Y')
    plt.title('Mapa de anomalía de Bouguer Corregida'), plt.show()

#generar residual:

def GeneraResidual():
    dfres=pd.DataFrame()
    dfreg=pd.DataFrame()
    df_interpolated = pd.DataFrame({'x': xi.flatten(), 'y': yi.flatten(), 'z': zi.flatten()}) #se aplanan las matrices en un df
    df_interpolated.dropna(inplace=True)
    df2= df_interpolated['x'].value_counts().to_frame('counts').reset_index() #Obtiene los valores de x que se repiten
    df2.columns=['x','count'] #renombra columnas
    df3= df_interpolated['y'].value_counts().to_frame('counts').reset_index() #obtiene valores de y que se repiten
    df3.columns=['y','count']# renombra

    while True:
        preg=input('Desea perfiles horizontales o verticales?[h/v]\n')
        match preg:
            case 'h':
                gi='x'
                df4=df2[gi]
                break
            case 'v':
                gi='y'
                df4=df3[gi]
                break
            case _:
                input('Ingrese una opción válida de perfiles\n')
                os.system('cls')
    for i in df4:
        x1= np.array(df_interpolated[df_interpolated[gi]==i]['x'])
        y1=np.array(df_interpolated[df_interpolated[gi]==i]['y'])
        z1=np.array(df_interpolated[df_interpolated[gi]==i]['z'])

        x0= np.linspace(x1[0],x1[-1])
        y0= np.linspace(y1[0],y1[-1])  #y constante OJO
        z0=np.linspace(z1[0],z1[-1])
        match preg:
            case 'h':
                perf1=y1
                perf0=y0
            case 'v':
                perf1=x1
                perf0=x0
        
        for order in range(1,30):
            model=np.polyfit(perf1,z1,order)
            evalua=np.polyval(model,perf1) #Bouger
            reg= np.polyfit(perf0,z0,1) 
            evareg= np.polyval(reg,perf1) #regional 

            if np.corrcoef(z1,evalua)[0,1]>=0.80: #coeficiente de correlacion R^2

                dfres=dfres.append(pd.DataFrame({'x':x1,'y':y1, 'z':evalua-evareg}),ignore_index=True)
                dfreg=dfreg.append(pd.DataFrame({'x':x1,'y':y1, 'z':evareg}),ignore_index=True)

                
            else:
                continue
    grafica(dfreg, 'Mapa de anomalía Regional')
    grafica(dfres, 'Mapa de anomalía Residual')
    os.system('cls')
    while True:
        qest= input('Desea guardar los datos de residual y regional en un excel?[s/n]\n')
        match qest:
            case 's':
                dfreg.to_excel(ruta[:-5]+'-Regional.xlsx',index=False)
                dfres.to_excel(ruta[:-5]+'-Residual.xlsx',index=False)
                break
            case 'n':
                print('Finalizó el programa')
                break
            case _:
                os.system('cls')
                input('Ingrese una opción válida')

#########
if __name__ =='__main__':
    while True:
        mainmenu()
        GeneraResidual()