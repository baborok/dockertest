import numpy as np
from keras.models import load_model
from numpy import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import math
from matplotlib import use as use_agg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import PySimpleGUI as sg


model = load_model('model.h5')

def transformer(Водород,Кислород,Азот,Метан,CO,CO2,Этилен,Этан,Ацетилен,Дибензилсульфид,Напряжение,Поверхностное_Н,Диэлектрическая_жесткость,Содержание_Воды,Срок_службы):
    data = np.array([[Водород,Кислород,Азот,Метан,CO,CO2,Этилен,Этан,Ацетилен,Дибензилсульфид,Напряжение,Поверхностное_Н,Диэлектрическая_жесткость,Содержание_Воды,Срок_службы]])
    prediction = model.predict(data)
    x = int(prediction[0])
    if x >= 56:
        transformer_index = 1
    elif 29<=x<=55:
        transformer_index = 2
    elif 17<=x<=28:
        transformer_index = 3
    elif 6<=x<=16:
        transformer_index = 4   
    elif x<=5:
        transformer_index = 5

    return transformer_index

myArray=0


def cock():
    global myArray
    a = random.randint(7000,10000)
    b = random.randint(7000,10000)
    c = random.randint(7000,10000)
    d = random.randint(7000,10000)
    e = random.randint(7000,10000)
    f = random.randint(7000,10000)
    g = 1000
    h = 1000
    j = 1000
    k = 1000
    l = 70
    z = 40
    m = 50
    v = 20
        
    myArray = transformer(a,b,c,d,d,e,f,g,h,j,k,l,z,m,v)
        
    return(myArray)





def animate(i, xs, ys):

    # Состояние трансформатора с текущего ридинга
    temp_c = myArray

    # Добавляем значения на лист
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)
    

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Показатель Индекса трансформатора')
    plt.ylabel('Индекс состояния трансформатора')
    fig.canvas.draw()


def pack_figure(graph, figure):
    canvas = FigureCanvasTkAgg(figure, graph.Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack(side='top', fill='both', expand=1)
    return plot_widget

use_agg('TkAgg')

def LEDIndicator(key=None, radius=100):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 48, fill_color=color, line_color=color)

layout = [[sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1'), [sg.Text('Индикатор состояния трансформатора', size=(30,1))],[sg.Text('Индекс состояния'), LEDIndicator('_cpu_'),[sg.Text(font=('Helvetica', 15), key='-TEXT1-', text_color='black')]]],[sg.Button('Пауза'), sg.Button('Выход')]]
window = sg.Window('Индекс состояния трансформатора', layout, finalize=True)


graph1 = window['Graph1']
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
pack_figure(graph1, fig)
animate(100,xs,ys)


def cvet(): 
    color=None
    if myArray == 1:
        color = 'green'
    elif myArray == 2:
        color ='blue'
    elif myArray == 3:
        color = 'yellow'
    elif myArray ==4:
        color = 'orange'
    elif myArray==5:
        color = 'red'

    return color

def index():
   
    if myArray == 1:
        transformer_index = f'Индекс состояния трансформатора 1'
    elif myArray == 2:
        transformer_index = f'Индекс состояния трансформатора 2'
    elif myArray == 3:
        transformer_index = f'Индекс состояния трансформатора 3'
    elif myArray ==4:
        transformer_index = f'Индекс состояния трансформатора 4'
    elif myArray==5:
        transformer_index = f'Индекс состояния трансформатора 5'
    return transformer_index

#def logs():
    f = open("log.txt", "a")
    f.write('\n')
    f.write(str(index()))
    f.write('  ')
    f.write(str(dt.datetime.now()))
    f.close()

data = np.array([0])
x=np.array([0])
y=np.array([0])


def sohr():
    global myArray
    global data
    global xs
    global ys
    global y
    global x
    y=np.append(y, ys)
    x=np.append(x, xs)
    df = pd.DataFrame({"date" : x, "index" : y})
    df.to_csv("sub1.csv", index=False)
    data = np.append(data, myArray)
    print (x,y)
    return data
    


while True:
    
    cock()  
    event, values = window.read(timeout=10)
    print(event, values)

    if event in (None, 'Выход'):
            break
    elif event == sg.TIMEOUT_EVENT:
        sohr()
        #logs()
        cock()
        animate(100,xs,ys)
    SetLED(window, '_cpu_', cvet())
    window['-TEXT1-'].update(f"Индекс состояния {myArray}")
     

window.close()