import math

print('>>>>>>>>>>>>>>>>>>>')
print('Filtros Ressonantes')
print('<<<<<<<<<<<<<<<<<<<\n\n')
print('===================')
print('Frequencia De Corte')
print('===================')
F1 = int(input('Digite o valor da Frequencia : \n'))
C1 = 10**(-6)
R1 = 1/(F1*C1*2*math.pi)
print('---------')
print(R1/1000,'kohms')
print('---------')
print('===================')
print('Frequencia Alta')
print('===================')
F2 = int(input('Digite o valor da Alta Frequencia : \n'))
C2 = 10**(-6)
R2 = 1/(F2*C2*2*math.pi)
print('---------')
print(R2/1000,'kohms')
print('---------')
'''
import math
import dash 
from plotly.tools import mpl_to_plotly
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html 
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import base64
from scipy.signal import butter, lfilter, freqz


myheading = 'Calculadora de Filtros Passivos'
apptitle = "Calculo da Resistencia do Circuito, dado o valor da Frequencia de Corte"
resultado = 1/((10**(-6))*(2)*(math.pi))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title=apptitle
server = app.server

#FILTRO PASSA FAIXA

def filtropf1(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def filtropf2(data, lowcut, highcut, fs, order=5):
    b, a = filtropf1(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def filtropf():
    fs = 5000.0
    lowcut = 500.0
    highcut = 2000.0

    # Plot the frequency response for a few different orders.
    plt.figure(1)
    plt.clf()
    for order in [3]:
        b, a = filtropf1(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h))

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Ganho')
    plt.grid(True)
    plt.legend(loc='best')
    plt.title('Banda de alocação filtro passa faixa')
    plt.savefig('filtropf.png')
    plt.clf()
filtropf()
filtropfplot = 'filtropf.png'
filtropfimagem = base64.b64encode(open(filtropfplot,'rb').read()).decode('ascii')

# FILTRO PASSA BAIXA

def filtropb1(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def filtropb2(data, cutoff, fs, order=5):
    b, a = filtropb1(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def filtropassabaixa():
    order = 6
    fs = 30      # Frequência de teste
    cutoff = 3  # Frequencia desejada a ser cortada, em Hz.
    
    # Resposta do filtro passa baixa
    b, a = filtropb1(cutoff, fs, order)
    
    # Plotagem da resposta da frequência
    w, h = freqz(b, a, worN=8000)
    plt.subplot(2, 1, 1)
    plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
    plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
    plt.axvline(cutoff, color='k')
    plt.xlim(0, 0.5*fs)
    plt.title("Banda de ação filtro passa baixa")
    plt.xlabel('Frequência [Hz]')
    plt.grid()
    
    
    # Uso do filtro
    # Gerador de sinal conturbado a fim de analisar o uso do filtro no mesmo
    T = 7.0         # seconds
    n = int(T * fs) # numero de amostras
    t = np.linspace(0, T, n, endpoint=False)
    # Sinal conturbado
    data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)
    
    # Plotagem do sinal filtrado e o sintal conturbado
    y = filtropb2(data, cutoff, fs, order)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, data, 'b-', label='Sinal')
    plt.plot(t, y, 'g-', linewidth=2, label='Sinal filtrado')
    plt.xlabel('Tempo')
    plt.grid()
    plt.legend()
    
    plt.subplots_adjust(hspace=0.35)
    plt.savefig('filtropb1.png')
    plt.clf()
filtropassabaixa() 
filtropassabaixaplot = 'filtropb1.png'
filtropassabaixa = base64.b64encode(open(filtropassabaixaplot,'rb').read()).decode('ascii')  

# FILTRO REJEITA FAIXA

samp_freq = 1000 # Frequência teste filtro rejeita faixa
notch_freq = 60  # Frequência a ser removida do filtro rejeita faixa
quality_factor = 10  # Fator de qualidade filtro rejeita faixa
f1 = 17  # gerador de sinal conturbado
f2 = 60  # gerador de sinal conturbado

def filtrorf1():
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
    freq, h = signal.freqz(b_notch, a_notch, fs = samp_freq)
    plt.figure('filter')
    plt.plot( freq, 20*np.log10(abs(h)))
    plt.title('Frequência a ser negada filtro rejeita faixa')
    plt.savefig('filtrorf1.png')
    plt.clf()    
filtrorf1()
filtrorf1 = 'filtrorf1.png'
filtrorejeitafaixa1 = base64.b64encode(open(filtrorf1,'rb').read()).decode('ascii')    
    
def filtrorf2():   # Criar sinal deformado introduzindo duas frequências
    t = np.linspace(0.0, 1, 1_000)
    y_pure = np.sin(f1 * 2.0*np.pi*t) + np.sin(f2 * 2.0*np.pi*t) 
    plt.figure('result')
    plt.subplot(211)
    plt.plot(t, y_pure, color = 'r')
    
    # Aplicar o filtro rejeita faixa no sinal deformado
    
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)           
    y_notched = signal.filtfilt(b_notch, a_notch, y_pure)
    
    # Sinal após a filtragem
    plt.subplot(212)
    plt.plot(t, y_notched, color = 'r')
    plt.title('Filtro Rejeita Faixa')
    plt.savefig('filtrorf2.png')
    plt.clf()
filtrorf2()
filtrorf2 = 'filtrorf2.png'
filtrorejeitafaixa2 = base64.b64encode(open(filtrorf2,'rb').read()).decode('ascii')    
    
# FILTRO PASSA ALTA

def grafico_1():
    x = np.linspace(0, 1, 100)
    y = np.exp(x)

    plt.subplot(223)
    plt.plot(x, y - y.mean())
    plt.yscale('symlog', linthresh=0.01)
    plt.title('Banda de ação filtro passa alta')
    plt.grid(True)
    plt.annotate('Mudança de banda', xy=(0.55,0), xytext=(0, 0.4),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
    plt.savefig('grafico_1.png')
    plt.clf()
grafico_1()

grafico1 = 'grafico_1.png'
filtropassaalta1 = base64.b64encode(open(grafico1,'rb').read()).decode('ascii')
    
def grafico_2():
    fs = 10000  # Valor para alterar dimensão do gráfico
    t = np.arange(1000) / fs
    sinala = np.sin(2*np.pi*200*t) # frequencia para gerar o sinal conturbado (padrao 200)
    
    sinalb = np.sin(2*np.pi*20*t) # frequencia para gerar o sinal conturbado(padrao 20)
    
    sinalc = sinala + sinalb
    plt.plot(t, sinalc, label='Sinal ')
    fc = 50  # Frequência de corte do filtro
    w = fc / (fs / 2) # Normalizando a frequencia
    b, a = signal.butter(5, w, 'High')
    output = signal.filtfilt(b, a, sinalc)
    plt.plot(t, output, label='Sinal Filtrado')
    plt.title("FILTRO PASSA ALTA")
    plt.xlabel("tempo")
    plt.ylabel("grandeza")
    plt.legend()
    plt.savefig('grafico_2.png')
    return 0
grafico_2()

grafico2 = 'grafico_2.png'
filtropassaalta2 = base64.b64encode(open(grafico2,'rb').read()).decode('ascii')


app.layout = html.Div(children=[
	html.H1(myheading),
    html.P('====================================================Disciplina: Exp. Circ. Elétricos II==================================================================='),
    html.P('ALUNOS:'),
    html.P('Jean C. Borges Matheus Pedrosa, Ana Notario'),
     html.P('===================================================================================================================================================='),
    html.H2('Introdução'),
    html.P('É definida como filtro qualquer combinação de elementos, passivou ou ativos, projetada especificamente para selecionar uma faixa de frequências. Isto quer dizer que, a partir da combinação que origina o circuito, sinais com frequências específicas podem ter sua passagem bloqueada ou permitida ao passar por esse arranjo. '),
    html.P('Os filtros possuem diversas aplicações, como em sistemas de comunicação, acústico, dentre outros. A sua função principal é eliminar sinais de frequências indesejáveis, ou ruídos, que são gerados e podem influenciar de maneira negativa na saída do sistema. '),
    html.P('Como já mencionado, os filtros podem ser divididos em passivos e ativos. No primeiro caso a combinação envolve apenas resistores, capacitores e/ou indutores. Esses componentes podem ser associados em série ou em paralelo. No segundo caso, além desses componentes, são usados também transistores e amplificadores operacionais. Por esse motivo, é comum que filtros passivos não precisem de fonte de alimentação para o funcionamento. '),
    html.P('O sistema de cálculo aqui apresentado se limitará ao funcionamento de filtros passivos e, mais especificamente, a duas categorias desses filtros: passa-baixa (PB) e passa-alta (PA). '),
    html.P('Como o próprio nome sugere, os filtros com função passa-baixa permitirá que sinais com frequências abaixo daquela de corte passem, tenham ganho. Enquanto os filtros passa-alta permitirão que sinais acima da frequência de corte passem. '),
    html.P('Os dois circuitos estudados são baseados na associação entre um resistor e um capacitor e são regidos pela mesma equação para se obter valores de componentes que determinem a frequência de corte: '),
    html.P('                                     fc=1/2πRC                                  '),
    html.P('Baseado na fórmula apresentada vamos desconsiderar, momentaneamente, a disposição do circuito. Ressaltamos apenas que no filtro PB a saída de tensão é a partir do capacitor e no filtro PA do resistor. Para construir um filtro, com base em um valor de frequência de corte previamente determinado, note que ainda assim teríamos duas variáveis a serem definidas. Sendo assim, adotaremos o valor fixo de 1µF para o valor de C na fórmula e o objetivo será calcular o valor da resistência (R).'),
    html.P('===================================================================================================================================================='),
    html.P('Utilizamos o valor do Capacitor como sendo um valor universal:'),
    html.P('C = e^-6'),
    html.P('===================================================================================================================================================='),
    html.P('FAÇA SUA CONTA, E RESOLVA SEU PROBLEMA:'),
    html.P('Insira o valor da Frequencia de Corte desejada:'),
	dcc.Input(id='input', value='Frequencia de Corte[Hz]', type='text'),
	html.Div(id = 'output'),
    html.P('===================================================================================================================================================='),
    html.H2('Entendendo os filtros, seus tipos e aplicabilidades'),
    html.P(''),
    html.P(''),
    html.P('Um gráfico representativo da banda passagem de frequência em um filtro é dado, geralmente, em valores de tensão normalizados em função da frequência. Isso quer dizer que, a tensão de saída é dividida pela tensão de entrada, criando o ganho, grandeza adimensional. Esse tipo de gráfico permite ao usuário uma visão geral da capacidade de atenuação do filtro em questão. Esse tipo de gráfico será bastante abordado mais afrente, a fim de entender quais serão as frequências negadas de acordo com o filtro utilizado'),
    html.Img(src='data:image/png;base64,{}'.format(filtropassabaixa)),
    html.P('Acima, além da banda de passagem permitida, temos também a aplicação de um filtro passa baixa. Entendendo quais as frequências o filtro afeta é o suficiente para compreendermos o seu funcionamento, porém uma análise gráfica do filtro em funcionamento ao filtrar um sinal ajuda significativamente na compreensão de sua execução.'),
    html.P('Esse conceito será aplicado a todos os filtros estudados, os quais são os mais requisitados e utilizados no âmbito de trabalho. '),
    html.P(''),
    html.P(''),
    html.P('Agora observaremos a mesma ideia, mas agora aplicada em um filtro passa alta.'),
    html.Img(src='data:image/png;base64,{}'.format(filtropassaalta1)),
    html.Img(src='data:image/png;base64,{}'.format(filtropassaalta2)),
    html.P('No geral, o ganho (Av) é dado em decibéis e pode ser obtido utilizando as seguinte equações:'),
    html.P('Passa-baixa: Avdb =  -20log10(f/fc) para frequências muito menores que a frequência de corte.'),
    html.P('Passa-alta: Avdb =    20Log1(f/fc) para frequências muito maiores do que a frequência de corte.'),
    html.P(''),
    html.P('A seguir, temos o gráfico da banda de atuação e da funcionalidade de um filtro rejeita faixa:'),
    html.Img(src='data:image/png;base64,{}'.format(filtrorejeitafaixa1)),
    html.P(''),
    html.Img(src='data:image/png;base64,{}'.format(filtrorejeitafaixa2)),
    html.P('E por fim, também temos um gráfico de banda de um filtro passa-faixa'),
    html.Img(src='data:image/png;base64,{}'.format(filtropfimagem)),
    html.P('===================================================================================================================================================='),
    html.H2('Filtros na prática!'),
    html.P('Filtros, ou atenuadores, possuem diversas aplicações e estão inseridos no cotidianos das pessoas. São muito usados em equipamentos de áudio, sistemas de antenas, rádios AM e FM, equipamentos biomédicos, dentre outros. '),
    html.P('Os filtros são necessários em projetos onde há a necessidade de delimitação de um sinal a ser trabalhado, e ao mesmo tempo, servem para retirar ruídos. '),
    html.P('Ruídos são todo e qualquer sinal indesejado ao sistema, podendo influenciar diretamente no funcionamento do equipamento. Um exemplo prático são equipamentos biomédicos que trabalham com sinais de baixa frequência e precisam ter um sistema de filtragem de ruídos provenientes da rede de alimentação (frequências de 60Hz). '),
    html.P('Um outro exemplo é a necessidade de eliminar ruídos de alta frequência, provenientes do próprio ambiente, depositados em uma fita magnética durante uma gravação de áudio.'),
    html.P('________´$$$$`_____________________________,,,_'),
	html.P('_______´$$$$$$$`_________________________´$$$`'),
	html.P('________`$$$$$$$`______,,________,,_______´$$$$´'),
	html.P('_________`$$$$$$$`____´$$`_____´$$`____´$$$$$´'),
	html.P('__________`$$$$$$$`_´$$$$$`_´$$$$$`__´$$$$$$$´'),
	html.P('___________`$$$$$$$_$$$$$$$_$$$$$$$_´$$$$$$$´_'),
	html.P('____________`$$$$$$_$$$$$$$_$$$$$$$`´$$$$$$´_'),
	html.P('___,,,,,,______`$$$$$$_$$$$$$$_$$$$$$$_$$$$$$´_'),
	html.P('_´$$$$$`____`$$$$$$_$$$$$$$_$$$$$$$_$$$$$$´_'),
	html.P('´$$$$$$$$$`´$$$$$$$_$$$$$$$_$$$$$$$_$$$$$´_'),
	html.P('´$$$$$$$$$$$$$$$$$$_$$$$$$$_$$$$$$$_$$$$$´_'),
	html.P('___`$$$$$$$$$$$$$$$_$$$$$$$_$$$$$$_$$$$$$´_'),
	html.P('______`$$$$$$$$$$$$$_$$$$$__$$_$$$$$$_$$´_'),
	html.P('_______`$$$$$$$$$$$$,___,$$$$,_____,$$$$$´_'),
	html.P('_________`$$$$$$$$$$$$$$$$$$$$$$$$$$$$$´_'),
	html.P('__________`$$$$$$$$$$$$$$$$$$$$$$$$$$$´_'),
	html.P('____________`$$$$$$$$$$$$$$$$$$$$$$$$´_'),
	html.P('_______________`$$$$$$$$$$$$$$$$$$$$´_')
	])


@app.callback(
	Output(component_id='output', component_property='children'),
	[Input(component_id='input', component_property='value')])
def update_value(input_data):
	try:
		return 'O Valor da Resistencia do circuito é {} KΩ'.format(str(float(input_data)**(-1)*resultado*(10**(-3))))
	except: 
		return "Resistencia do Circuito"
    


if __name__ == '__main__': 
	app.run_server(debug=True)
