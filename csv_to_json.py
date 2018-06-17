import pandas as pd

df = pd.read_csv('workouts.csv')
df = df.transpose()
json = df.to_json()

f = open('workouts.json', 'w')

f.write(json)
f.close()
