from random import random
from math import exp, log

feature = [
	lambda x: x[0], # x1
  lambda x: x[1], # x2
  lambda x: x[2], # x3
]

# C: lista de coeficientes da hipótese (thetas)
# I: uma instância dos dados de entrada
def hipotese(C, X):
  f = sum( [ c*feature[i](X) for i, c in enumerate(C)] )
  return 1 / ( 1 + exp(-f))

# Retorna valores normalizados
def getData():

  def fn_para_teste(x1, x2):
    return x1 + x2;

  data = [ 
    [1.17, 2.17,  fn_para_teste(1.17, 2.17)],
    [2.97, 30.97, fn_para_teste(2.97, 30.97)],
    [3.26, 70.26, fn_para_teste(3.26, 70.26)],
    [4.69, 0.69,  fn_para_teste(4.69, 0.69)],
    [5.83, 10.83, fn_para_teste(5.83, 10.83)],
    [6.00, 50.00, fn_para_teste(6.00, 50.00)],
    [6.41, 9.41,  fn_para_teste(6.41, 9.41)],
  ]

  # Retorna valores da lista entre 0 e 1
  # list: integer | float
  def normaliza_entre_0_1(list):
    min_val = min(list)
    max_val = max(list)
    return [ (x-min_val)/(max_val-min_val) for x in list]

  # Normaliza valores enter [0,1] por colunas
  for i in range(0, len(data[0])): # cada coluna
    original_column = [ row[i] for row in data ]
    normalized_column = normaliza_entre_0_1(original_column)
    for j in range(0, len(data)): # cada linha
      data[j][i] = normalized_column[j]

  return data; 

data = getData()

# Média dos erros ao quadrado
# C: lista de coeficientes da hipótese (thetas)
def J(C):
  def fn(X):
    y = X[len(X)-1]
    return -y*(log( hipotese(C, X) )) - (1-y)*(log( 1-hipotese(C, X) ))
  return (1/(2*len(data))) * sum([ fn(X) for X in data ])

# Cálculo da derivada em relação a um dos coeficientes (aproximação numérica)
# C: lista de coeficientes da hipótese (thetas)
# i: índice do coefiente que derivará J
def derivada_raw(C, i):
  epsilon = 0.0000001
  C1 = list(C)
  C2 = list(C)
  C1[i] = C1[i] + epsilon
  C2[i] = C2[i] - epsilon
  return (J(C1) - J(C2)) / (2*epsilon)

# Cálculo da derivada em relação a um dos coeficientes (usando função de erro)
# C: lista de coeficientes da hipótese (thetas)
# i: índice do coefiente que derivará J
def derivada(C, i):
  return (1/len(data)) * sum([ (hipotese(C, X) - X[len(X)-1])*feature[i](X) for X in data ]) # onde X[len[X]-1] é o atributo alvo ou y

# coeficiente = [
#   [ [ random(), random() ], [ random(), random()] ], # camada 1
#   [ [ random(), random() ] ],                        # camada 2
# ]
coeficiente = [
  [ [ 1, 2 ], [ 3, 4 ], [ 1, 2 ] ], # camada 1
  [ [ 1, 2, 1 ], [ 3, 4, 1 ], [ 1, 2, 1 ] ], # camada 1
  [ [ 5, 6, 1 ] ], # camada 2
]

###

neuronio = [ # valores iniciais quaisquer, serão atribuidos na propagação das entradas
  [ 0, 0, 0 ], # camada 1
  [ 0, 0, 0 ], # camada 1
  [ 0 ], # camada 2
]

erro = [ # valores iniciais quaisquer, serão atribuidos na propagação das entradas
  [ 0, 0, 0 ], # camada 1 (oculta)
  [ 0, 0, 0 ], # camada 1 (oculta)
  [ 0 ],    # camada 2 (saída)
]

ultima_camada = len(neuronio)-1;
print("ultima_camada", ultima_camada)

for i,X in enumerate(data):
  print(i,'-',X)
  # X = data[1] # (teste) usando somente um instância dos dados

  # ---- Propagação de entradas

  y = X[ len(X)-1 ]

  for l in range(0, len(neuronio)): # camadas
    for i in range(0, len(neuronio[l])): # neurônios da camada
      if(l == 0):
        neuronio[l][i] = hipotese(coeficiente[l][i], X)             # 1º camada tem como entrada X
      else:
        neuronio[l][i] = hipotese(coeficiente[l][i], neuronio[l-1]) # demais camada têm como entrada a camada anterior

  print("Valores propagados:", neuronio)


  # ---- Cálculo erros

  # camada de saída (considera somente 1 saída (TODO: permitir mais de uma saida))
  erro[ultima_camada][0] = neuronio[ultima_camada][0] - y 

  # camadas ocultas
  for l in range(len(neuronio)-2, -1, -1): # camadas (da penultima para a primeira, última camada já foi tratada no passo anterior).
    for i in range(0, len(neuronio[l])): # neurônios da camada
      coluna_pesos = [row[i] for row in coeficiente[l+1]] # usa somente pesos do neurônio i (coeficiente[l+1] retorna os pesos de todos os coeficientes da camada da frente, pesos de um neuronio estão na coluna dessa matriz)
      erros_balanceados = sum([ c*erro[l+1][j] for j,c in enumerate(coluna_pesos) ])
      erro[l][i] = erros_balanceados * (neuronio[l][i] * (1 - neuronio[l][i]))  # somatorio dos erros dos neuronios das camadas seguintes

  print("Erros coletados:", erro)


  # ---- Cálculo gradientes / Ajuste coeficientes(pesos)

  print('---------------------')

  # TODO: reavaliar!!!
  # TODO: tentar unificar X e neuronio (trata X como camda zero e demais como camada 1) 

  alpha = 0.1

  print('l i j \told\tnew')
  for l in range(0, len(neuronio)):
    for i in range(0, len(neuronio[l])):
      for j in range(0, len(coeficiente[l][i])):
        if(l == 0):
          new = coeficiente[l][i][j] - alpha * ( X[j] * erro[l][i] )
          print(l, i, j, '\t', coeficiente[l][i][j], '\t', new, '\t', X[j], '\t', erro[l][i])
          coeficiente[l][i][j] = new
        else:
          new = coeficiente[l][i][j] - alpha * ( neuronio[l-1][j] * erro[l][i] )
          coeficiente[l][i][j] = new
          print(l, i, j, '\t', coeficiente[l][i][j], '\t', new, '\t', neuronio[l-1][j], '\t', erro[l][i])

  print('---------------------')

