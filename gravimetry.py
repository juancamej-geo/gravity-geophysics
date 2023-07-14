import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from tkinter import filedialog
import os
def mainmenu():
    global ruta
    ch=input('-'*10+ 'Menú principal'+ '-'*10+ '\nSeleccione una opción:\n1-Leer Archivo\n2-Información del software\n')
    match ch:
        case '1':
            ruta= filedialog.askopenfile(title='Ingrese el archivo', initialdir='C:/Users/PC/Documents',filetypes=[('Archivos Excel','.xlsx')]).name
            leer(ruta)
        case '2':
            input('-'*50+'\nDesarrollado por: Juan C. Mejía\nSoftware de uso académico\nPara más información consulte al correo juan.601823945@ucaldas.edu.co\n'+'-'*50)



def leer(inb):
    global df_interpolated,df2,df3
    df = pd.read_excel(inb)

    x = df['x'].values
    y = df['y'].values
    z = df['z'].values

    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    xi, yi = np.meshgrid(xi, yi)

    zi = griddata((x, y), z, (xi, yi), method='cubic')
    while True:
        match input('Desea mostrar los puntos cargados?[s/n]'):
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

    df_interpolated = pd.DataFrame({'x': xi.flatten(), 'y': yi.flatten(), 'z': zi.flatten()})
    df_interpolated.dropna(inplace=True)
    df2= df_interpolated['x'].value_counts().to_frame('counts').reset_index() #Obtiene los valores de x que se repiten
    df2.columns=['x','count'] #renombra columnas
    df3= df_interpolated['y'].value_counts().to_frame('counts').reset_index() #obtiene valores de x que se repiten
    df3.columns=['y','count']# renombra


#generar residual:

def GeneraResidual():
    res=pd.read_csv(ruta, sep=' ')
    
    for i in df3['y']:
        x1= np.array(df_interpolated[df_interpolated['y']==i]['x'])
        y1=np.array(df_interpolated[df_interpolated['y']==i]['y'])
        z1=np.array(df_interpolated[df_interpolated['y']==i]['z'])

        x0= np.linspace(x1[0],x1[-1])
        y0= np.linspace(y1[0],y1[-1])  #y constante
        z0=np.linspace(z1[0],z1[-1])
        for order in range(0,50):
            model=np.polyfit(x1,z1,order)
            evalua=np.polyval(model,x1)
            reg= np.polyfit(x0,z0,1) #regional 
            evareg= np.polyval(reg,x1) #regional 

            if np.corrcoef(z1,evalua)[0,1]>=0.99: #coeficiente de correlacion R^2
                dffinal=pd.DataFrame({'x':x1,'y':y1, 'z':evalua-evareg})  
                       
            else:
                continue
            res=res.append(dffinal, ignore_index=True )
    return res.to_excel(ruta+'000.xlsx',index=False)


#esto es un test
if __name__ =='__main__':
    while True:
        mainmenu()