import pandas as pd

#Теперь также легко и просто конвертируем наши json-файлы в csv, чтобы привести их к чистому виду без выбросов
with open('../Step 0/topor.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('topor.csv', encoding='utf-8', index=False)
#(Результат после прогонки каждого нашего json, можно увидеть в папке 'Step 1')