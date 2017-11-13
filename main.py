from random import random
from math import exp, log

feature = [
	lambda i: 1,
  lambda i: i[0], #x1
  lambda i: i[0]**2, #x1
  lambda i: i[0]**5, #x1
	lambda i: sin(i[0]), #x1
]

# C: lista de coeficientes da hipótese (thetas)
# I: uma instância dos dados de entrada
def hipotese(C, X):
  f = sum( [ c*feature[i](X) for i, c in enumerate(C)] )
  return 1 / ( 1 + exp(-f))

# Retorna valores normalizados
def getData():
  data = [
    [1.17, 78.93],
    [2.97, 58.20],
    [3.26, 67.47],
    [4.69, 37.47],
    [5.83, 45.65],
    [6.00, 32.92],
    [6.41, 29.97],
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
  random(),
  random(),
]

alpha = 0.1;

erro_atual = 0;
while(abs(J(coeficiente) - erro_atual) > 0.00001):
  
  erro_atual = J(coeficiente);

  print("Erro :", J(coeficiente), "\t\tC: ", coeficiente)
  
  # Atualização de coeficientes
  coeficiente = [ c - alpha*derivada(coeficiente, i) for i,c in enumerate(coeficiente) ]


print(hipotese(coeficiente, [0.1]))
print(hipotese(coeficiente, [0.2]))
print(hipotese(coeficiente, [0.3]))
print(hipotese(coeficiente, [0.4]))
print(hipotese(coeficiente, [0.5]))
print(hipotese(coeficiente, [0.5]))
print(hipotese(coeficiente, [0.6]))
print(hipotese(coeficiente, [0.7]))
print(hipotese(coeficiente, [0.8]))
print(hipotese(coeficiente, [0.9]))
print(hipotese(coeficiente, [0.10]))