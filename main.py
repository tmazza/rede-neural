import random

feature = [
	lambda i: 1,
	lambda i: i[0], #x1
]

# C: lista de coeficientes da hipotese (thetas)
# I: uma instância dos dados de entrada
def hipotese(C, X):
  return sum( [ c*feature[i](X) for i, c in enumerate(C)] )

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
  return data; #TODO: normalizar

data = getData()

# Média dos erros ao quadrado
# C: lista de coeficientes da hipotese (thetas)
def J(C):
  return (1/2*len(data)) * sum([ (hipotese(C, X) - X[len(X)-1])**2 for X in data ])

coeficiente = [
  83.089,
  -7.812,
]

alpha = 0.1;

print(hipotese(coeficiente, [5.83, 78.93]))

# erro_atual = 0;

# a = 0
# while(a < 10):

#   # erro_atual = J(data)
#   # print(erro_atual)
#   gradiente = [ derivada(data, i) for i, f in enumerate(feature) ];
#   print(gradiente)
#   coeficiente = [ c - alpha*gradiente[i] for i, c in enumerate(coeficiente) ]
#   # print(coeficiente)

#   a+=1




