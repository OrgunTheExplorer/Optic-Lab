import pandas as pd

L = 32.5
wavelenght_red = 6040*(10**(-8))
wavelenght_green = 5592*(10**(-8))


red_max = pd.Series([2, 2.1, 2.1, 2.1, 2, 2, 2])
red_min = pd.Series([1.6, 1.7, 1.8, 2.1, 2, 1.8, 1.8])
green_max = pd.Series([2.1, 2, 2.1, 2, 2, 2, 2])
green_min = pd.Series([1.4, 1.5, 1.5, 1.4, 1.4, 1.4, 1.5])


delta_red = red_max.mean()-red_min.mean()
delta_red_std = ((red_max.std()**2)+(red_min.std()**2))**1/2


delta_green = green_max.mean()-green_min.mean()
delta_green_std = ((green_max.std()**2)+(green_min.std()**2))**1/2


print("Distance d of red light equals to:",L*wavelenght_red*10000/delta_red,"µm")
print("STD of distance d of red light equals to:",L*wavelenght_red*delta_red_std*10000/delta_red/delta_red,"µm")

print("Distance d of green light equals to:",L*wavelenght_green*10000/delta_green,"µm")
print("STD of distance d of green light equals to:",L*wavelenght_green*delta_green_std*10000/delta_green/delta_green,"µm")
