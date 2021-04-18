#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 20:40:37 2021

@author: jeanborges
"""
'''
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
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html 

myheading = 'Filtros Ressonantes'
apptitle = "Calculo da Resistencia do Circuito"
resultado = 1/((10**(-6))*(2)*(math.pi))

app = dash.Dash()

app.layout = html.Div(children=[
	html.H1(myheading),
    html.P('Disciplina: Exp. Circ. Elétricos II'),
    html.P('Jean C. Borges, Matheus Pedrosa, Ana Notario'),
    html.P('C = e^-6, valor universal'),
    html.P('Insira o valor da Frequencia de Corte desejada:'),
	dcc.Input(id='input', value='Frequencia de Corte[Hz]', type='text'),
	html.Div(id= 'output')
	])

@app.callback(
	Output(component_id='output', component_property='children'),
	[Input(component_id='input', component_property='value')])
def update_value(input_data):
	try:
		return 'O Valor da Resistencia do circuito é {} KΩ'.format(str(float(input_data)**(-1)*resultado*(10**(-3))))
	except: 
		return "Retorna o valor da Resistencia do Circuito"

if __name__ == '__main__':
	app.run_server(debug=True)