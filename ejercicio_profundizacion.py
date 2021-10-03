"""
Ejercicio de Profundización - SQL
"""
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np


def fetch():
    conn = sqlite3.connect('heart.db')
    c = conn.cursor()

    c.execute('SELECT pulso FROM sensor')
    
    data = c.fetchall()
    
    conn.commit()
    conn.close()

    return data


def show(data):
    fig = plt.figure()
    fig.suptitle('Ritmo cardíaco', fontsize=16)
    ax = fig.add_subplot()

    ax.plot(data, c='red', label='pulso')
    ax.legend()
    ax.grid()
    plt.show()

def estadistica(data):
    data = np.asanyarray(data)
    min = np.min(data)
    max = np.max(data)
    mean = np.mean(data)
    std = np.std(data)

    stats = f"ESTADÍSTICAS:\nValor mínimo: {min}\nValor máximo: {max}\nValor medio: {mean}\nDesvío estandar: {std}\n"

    return stats
    
 
def regiones(data):
    data = np.asanyarray(data)
    mean = np.mean(data)
    std = np.std(data)
    x1 = []
    y1 = []
    for i in range(len(data)):
        if data[i] <= (mean-std):
            x1.append(i)
            y1.append(data[i])
    
    x2 = []
    y2 = []
    for i in range(len(data)):
        if data[i] >= (mean+std):
            x2.append(i)
            y2.append(data[i])
            
    x3 = []
    y3 = []
    for i in range(len(data)):
        if data[i] not in x1 and data[i] not in x2:
            x3.append(i)
            y3.append(data[i])
    
    fig = plt.figure()
    fig.suptitle('Regiones', fontsize=16)
    ax1 = fig.add_subplot(1, 2, 1)  
    ax2 = fig.add_subplot(1, 2, 2)  
    ax3 = fig.add_subplot(2, 2, 1)  
    
    ax1.scatter(x1, y1, c='darkgreen',label='Tranquila')
    ax1.legend()
    ax1.grid()

    ax2.scatter(x2, y2, c='darkred', label='Entusiasmada')
    ax2.legend()
    ax2.grid()
    
    ax3.scatter(x3, y3, c='darkblue',label='Aburrida')
    ax3.legend()
    ax3.grid()
    
    plt.show()
    
    fig = plt.figure()
    fig.suptitle('Regiones', fontsize=16)
    ax4 = fig.add_subplot()
    ax4.scatter(x1, y1, c='darkgreen',label='Tranquila')
    ax4.scatter(x2, y2, c='darkred', label='Entusiasmada')
    ax4.scatter(x3, y3, c='darkblue',label='Aburrida')
    ax4.legend()
    ax4.grid()
    plt.show()
    
    
    
     
    
def main():
    data = fetch()
    show(data)
    stats = estadistica(data)
    print(stats)
    regiones(data)
    
    
if __name__ == '__main__':

    main()




