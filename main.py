from random import random
from math import exp, log

feature = [
	lambda i: i[0], # x1
  lambda i: i[1], # x2
  #lambda i: i[0]**2, # x1 ^ 2 
  #lambda i: i[1]**5, # x2 ^ 5
	#lambda i: sin(i[0]), # sin(x1)
]

# C: lista de coeficientes da hipótese (thetas)
# I: uma instância dos dados de entrada
def hipotese(C, X):
  f = sum( [ c*feature[i](X) for i, c in enumerate(C)] )
  return 1 / ( 1 + exp(-f))

# Retorna valores normalizados
def getData():

  def fn_para_teste(x1, x2):
    return 3*x1 - 2*x2;

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

coeficiente = [
  [ [ random(), random() ], [ random(), random()] ], # camada 1
  [ [ random(), random() ] ],                        # camada 2
]

neuronio = [ # valores iniciais quaisquer, serão atribuidos na propagação das entradas
  [ 0, 0 ], # camada 1
  [ 0 ],    # camada 2
]

X = data[1] # (teste) usando somente um instância dos dados

y = X[ len(X)-1 ]
print("X", X)

C = coeficiente[0][0];
neuronio[0][0] = hipotese(C, X)
print("camada 0 - neuronio 0", C)

C = coeficiente[0][1]
neuronio[0][1] = hipotese(C, X)
print("camada 0 - neuronio 1", C)

C = coeficiente[1][0];
neuronio[1][0] = hipotese(C, neuronio[0]);


f_x = neuronio[ len(neuronio)-1 ][0] # saída último neurônio
print("f_x", f_x)
print("erro", abs(f_x - y))

print(neuronio)
print(neuronio[ len(neuronio)-1 ][0])