import random

feature = [
	lambda x: 1,
	lambda x: x,
]

coeficiente = [
	random.random(),
	random.random(),
]

def hipotese(X):
  return sum( [ (coeficiente[i]*feature[i](x)) for i, x in enumerate(X)] )

print(hipotese([2,2]))
