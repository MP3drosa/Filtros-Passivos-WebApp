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
    plt.title('Banda de aloca????o filtro passa faixa')
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
    fs = 30      # Frequ??ncia de teste
    cutoff = 3  # Frequencia desejada a ser cortada, em Hz.
    
    # Resposta do filtro passa baixa
    b, a = filtropb1(cutoff, fs, order)
    
    # Plotagem da resposta da frequ??ncia
    w, h = freqz(b, a, worN=8000)
    plt.subplot(2, 1, 1)
    plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
    plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
    plt.axvline(cutoff, color='k')
    plt.xlim(0, 0.5*fs)
    plt.title("Banda de a????o filtro passa baixa")
    plt.xlabel('Frequ??ncia [Hz]')
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

samp_freq = 1000 # Frequ??ncia teste filtro rejeita faixa
notch_freq = 60  # Frequ??ncia a ser removida do filtro rejeita faixa
quality_factor = 10  # Fator de qualidade filtro rejeita faixa
f1 = 17  # gerador de sinal conturbado
f2 = 60  # gerador de sinal conturbado

def filtrorf1():
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
    freq, h = signal.freqz(b_notch, a_notch, fs = samp_freq)
    plt.figure('filter')
    plt.plot( freq, 20*np.log10(abs(h)))
    plt.title('Frequ??ncia a ser negada filtro rejeita faixa')
    plt.savefig('filtrorf1.png')
    plt.clf()    
filtrorf1()
filtrorf1 = 'filtrorf1.png'
filtrorejeitafaixa1 = base64.b64encode(open(filtrorf1,'rb').read()).decode('ascii')    
    
def filtrorf2():   # Criar sinal deformado introduzindo duas frequ??ncias
    t = np.linspace(0.0, 1, 1_000)
    y_pure = np.sin(f1 * 2.0*np.pi*t) + np.sin(f2 * 2.0*np.pi*t) 
    plt.figure('result')
    plt.subplot(211)
    plt.plot(t, y_pure, color = 'r')
    
    # Aplicar o filtro rejeita faixa no sinal deformado
    
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)           
    y_notched = signal.filtfilt(b_notch, a_notch, y_pure)
    
    # Sinal ap??s a filtragem
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
    plt.title('Banda de a????o filtro passa alta')
    plt.grid(True)
    plt.annotate('Mudan??a de banda', xy=(0.55,0), xytext=(0, 0.4),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
    plt.savefig('grafico_1.png')
    plt.clf()
grafico_1()

grafico1 = 'grafico_1.png'
filtropassaalta1 = base64.b64encode(open(grafico1,'rb').read()).decode('ascii')
    
def grafico_2():
    fs = 10000  # Valor para alterar dimens??o do gr??fico
    t = np.arange(1000) / fs
    sinala = np.sin(2*np.pi*200*t) # frequencia para gerar o sinal conturbado (padrao 200)
    
    sinalb = np.sin(2*np.pi*20*t) # frequencia para gerar o sinal conturbado(padrao 20)
    
    sinalc = sinala + sinalb
    plt.plot(t, sinalc, label='Sinal ')
    fc = 50  # Frequ??ncia de corte do filtro
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
    html.P('====================================================Disciplina: Exp. Circ. El??tricos II==================================================================='),
    html.P('ALUNOS:'),
    html.P('Jean C. Borges Matheus Pedrosa, Ana Notario'),
     html.P('===================================================================================================================================================='),
    html.H2('Introdu????o'),
    html.P('?? definida como filtro qualquer combina????o de elementos, passivou ou ativos, projetada especificamente para selecionar uma faixa de frequ??ncias. Isto quer dizer que, a partir da combina????o que origina o circuito, sinais com frequ??ncias espec??ficas podem ter sua passagem bloqueada ou permitida ao passar por esse arranjo. '),
    html.P('Os filtros possuem diversas aplica????es, como em sistemas de comunica????o, ac??stico, dentre outros. A sua fun????o principal ?? eliminar sinais de frequ??ncias indesej??veis, ou ru??dos, que s??o gerados e podem influenciar de maneira negativa na sa??da do sistema. '),
    html.P('Como j?? mencionado, os filtros podem ser divididos em passivos e ativos. No primeiro caso a combina????o envolve apenas resistores, capacitores e/ou indutores. Esses componentes podem ser associados em s??rie ou em paralelo. No segundo caso, al??m desses componentes, s??o usados tamb??m transistores e amplificadores operacionais. Por esse motivo, ?? comum que filtros passivos n??o precisem de fonte de alimenta????o para o funcionamento. '),
    html.P('O sistema de c??lculo aqui apresentado se limitar?? ao funcionamento de filtros passivos e, mais especificamente, a duas categorias desses filtros: passa-baixa (PB) e passa-alta (PA). '),
    html.P('Como o pr??prio nome sugere, os filtros com fun????o passa-baixa permitir?? que sinais com frequ??ncias abaixo daquela de corte passem, tenham ganho. Enquanto os filtros passa-alta permitir??o que sinais acima da frequ??ncia de corte passem. '),
    html.P('Os dois circuitos estudados s??o baseados na associa????o entre um resistor e um capacitor e s??o regidos pela mesma equa????o para se obter valores de componentes que determinem a frequ??ncia de corte: '),
    html.P('                                     fc=1/2??RC                                  '),
    html.P('Baseado na f??rmula apresentada vamos desconsiderar, momentaneamente, a disposi????o do circuito. Ressaltamos apenas que no filtro PB a sa??da de tens??o ?? a partir do capacitor e no filtro PA do resistor. Para construir um filtro, com base em um valor de frequ??ncia de corte previamente determinado, note que ainda assim ter??amos duas vari??veis a serem definidas. Sendo assim, adotaremos o valor fixo de 1??F para o valor de C na f??rmula e o objetivo ser?? calcular o valor da resist??ncia (R).'),
    html.P('===================================================================================================================================================='),
    html.P('Utilizamos o valor do Capacitor como sendo um valor universal:'),
    html.P('C = e^-6'),
    html.P('===================================================================================================================================================='),
    html.P('FA??A SUA CONTA, E RESOLVA SEU PROBLEMA:'),
    html.P('Insira o valor da Frequencia de Corte desejada:'),
	dcc.Input(id='input', value='Frequencia de Corte[Hz]', type='text'),
	html.Div(id = 'output'),
    html.P('===================================================================================================================================================='),
    html.H2('Entendendo os filtros, seus tipos e aplicabilidades'),
    html.P(''),
    html.P(''),
    html.P('Um gr??fico representativo da banda passagem de frequ??ncia em um filtro ?? dado, geralmente, em valores de tens??o normalizados em fun????o da frequ??ncia. Isso quer dizer que, a tens??o de sa??da ?? dividida pela tens??o de entrada, criando o ganho, grandeza adimensional. Esse tipo de gr??fico permite ao usu??rio uma vis??o geral da capacidade de atenua????o do filtro em quest??o. Esse tipo de gr??fico ser?? bastante abordado mais afrente, a fim de entender quais ser??o as frequ??ncias negadas de acordo com o filtro utilizado'),
    html.Img(src='data:image/png;base64,{}'.format(filtropassabaixa)),
    html.P('Acima, al??m da banda de passagem permitida, temos tamb??m a aplica????o de um filtro passa baixa. Entendendo quais as frequ??ncias o filtro afeta ?? o suficiente para compreendermos o seu funcionamento, por??m uma an??lise gr??fica do filtro em funcionamento ao filtrar um sinal ajuda significativamente na compreens??o de sua execu????o.'),
    html.P('Esse conceito ser?? aplicado a todos os filtros estudados, os quais s??o os mais requisitados e utilizados no ??mbito de trabalho. '),
    html.P(''),
    html.P(''),
    html.P('Agora observaremos a mesma ideia, mas agora aplicada em um filtro passa alta.'),
    html.Img(src='data:image/png;base64,{}'.format(filtropassaalta1)),
    html.Img(src='data:image/png;base64,{}'.format(filtropassaalta2)),
    html.P('No geral, o ganho (Av) ?? dado em decib??is e pode ser obtido utilizando as seguinte equa????es:'),
    html.P('Passa-baixa: Avdb =  -20log10(f/fc) para frequ??ncias muito menores que a frequ??ncia de corte.'),
    html.P('Passa-alta: Avdb =    20Log1(f/fc) para frequ??ncias muito maiores do que a frequ??ncia de corte.'),
    html.P(''),
    html.P('A seguir, temos o gr??fico da banda de atua????o e da funcionalidade de um filtro rejeita faixa:'),
    html.Img(src='data:image/png;base64,{}'.format(filtrorejeitafaixa1)),
    html.P(''),
    html.Img(src='data:image/png;base64,{}'.format(filtrorejeitafaixa2)),
    html.P('E por fim, tamb??m temos um gr??fico de banda de um filtro passa-faixa'),
    html.Img(src='data:image/png;base64,{}'.format(filtropfimagem)),
    html.P('===================================================================================================================================================='),
    html.H2('Filtros na pr??tica!'),
    html.P('Filtros, ou atenuadores, possuem diversas aplica????es e est??o inseridos no cotidianos das pessoas. S??o muito usados em equipamentos de ??udio, sistemas de antenas, r??dios AM e FM, equipamentos biom??dicos, dentre outros. '),
    html.P('Os filtros s??o necess??rios em projetos onde h?? a necessidade de delimita????o de um sinal a ser trabalhado, e ao mesmo tempo, servem para retirar ru??dos. '),
    html.P('Ru??dos s??o todo e qualquer sinal indesejado ao sistema, podendo influenciar diretamente no funcionamento do equipamento. Um exemplo pr??tico s??o equipamentos biom??dicos que trabalham com sinais de baixa frequ??ncia e precisam ter um sistema de filtragem de ru??dos provenientes da rede de alimenta????o (frequ??ncias de 60Hz). '),
    html.P('Um outro exemplo ?? a necessidade de eliminar ru??dos de alta frequ??ncia, provenientes do pr??prio ambiente, depositados em uma fita magn??tica durante uma grava????o de ??udio.'),
    html.P('________??$$$$`_____________________________,,,_'),
	html.P('_______??$$$$$$$`_________________________??$$$`'),
	html.P('________`$$$$$$$`______,,________,,_______??$$$$??'),
	html.P('_________`$$$$$$$`____??$$`_____??$$`____??$$$$$??'),
	html.P('__________`$$$$$$$`_??$$$$$`_??$$$$$`__??$$$$$$$??'),
	html.P('___________`$$$$$$$_$$$$$$$_$$$$$$$_??$$$$$$$??_'),
	html.P('____________`$$$$$$_$$$$$$$_$$$$$$$`??$$$$$$??_'),
	html.P('___,,,,,,______`$$$$$$_$$$$$$$_$$$$$$$_$$$$$$??_'),
	html.P('_??$$$$$`____`$$$$$$_$$$$$$$_$$$$$$$_$$$$$$??_'),
	html.P('??$$$$$$$$$`??$$$$$$$_$$$$$$$_$$$$$$$_$$$$$??_'),
	html.P('??$$$$$$$$$$$$$$$$$$_$$$$$$$_$$$$$$$_$$$$$??_'),
	html.P('___`$$$$$$$$$$$$$$$_$$$$$$$_$$$$$$_$$$$$$??_'),
	html.P('______`$$$$$$$$$$$$$_$$$$$__$$_$$$$$$_$$??_'),
	html.P('_______`$$$$$$$$$$$$,___,$$$$,_____,$$$$$??_'),
	html.P('_________`$$$$$$$$$$$$$$$$$$$$$$$$$$$$$??_'),
	html.P('__________`$$$$$$$$$$$$$$$$$$$$$$$$$$$??_'),
	html.P('____________`$$$$$$$$$$$$$$$$$$$$$$$$??_'),
	html.P('_______________`$$$$$$$$$$$$$$$$$$$$??_')
	])


@app.callback(
	Output(component_id='output', component_property='children'),
	[Input(component_id='input', component_property='value')])
def update_value(input_data):
	try:
		return 'O Valor da Resistencia do circuito ?? {} K??'.format(str(float(input_data)**(-1)*resultado*(10**(-3))))
	except: 
		return "Resistencia do Circuito"
    


if __name__ == '__main__': 
	app.run_server(debug=True)
