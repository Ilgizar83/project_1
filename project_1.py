import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# %matplotlib inline

"""# Визуальный анализ рейтингов шоу Netflix
<img src="https://pp.userapi.com/c854528/v854528797/c62ce/FiPEibYUxJc.jpg" width="40%">

Netflix за последние 5-10 лет обзавелись большим количеством зрителей. С увеличением числа зрителей увеличилось и разнообразие шоу. Соответственно, перед аналитиками из киноиндустрии встала задача исследования данных с рейтингами различных сериалов.  
В данном задании вам предстоит провести визуальный анализ датасета **1000 Netflix Shows** (по состоянию на 11.06.2017) и сделать выводы.

### Описание признаков:
* `title` - название шоу.
* `rating` - рейтинг шоу. Например: G, PG, TV-14, TV-MA.
* `ratingLevel` - описание рейтинговой группы и особенностей шоу.
* `ratingDescription` - рейтинг шоу, закодированный в числом.
* `release year` - год выпуска шоу.
* `user rating score` - оценка пользователей.
* `user_rating_size` - общий рейтинг пользователей.

## Решение
"""

# from google.colab import files
# uploaded = files.upload()

data = pd.read_csv("data_set/NetflixShows.csv", encoding='cp437')
del data['ratingDescription'], data['user rating size']
print(data)

"""
### Удалите из данных дубликаты.
- Почему они возникли?
- Много ли их? В каких группах их больше всего?
"""

# дубликаты изначально в данных. По идеи должны были быть 1000 уникальных значение если не удалять два столбца
# 500 (В каких группах их больше всего? - если это дубликаты строк, как их может больше в какой либо группе?)

data.duplicated().sum()

# дубликаты по значениям в столбцах до удаления
data.duplicated(['title']).sum(),data.duplicated(['rating']).sum(),data.duplicated(['ratingLevel']).sum(),data.duplicated(['release year']).sum(),data.duplicated(['user rating score']).sum()

# удаляем дубликаты (по всем значениям)
df=data.drop_duplicates().reset_index(drop=True)
print(df)

# дубликаты по значениям в столбцах после удаления
df.duplicated(['title']).sum(),df.duplicated(['rating']).sum(),df.duplicated(['ratingLevel']).sum(),df.duplicated(['release year']).sum(),df.duplicated(['user rating score']).sum()

"""### Сколько рейтинговых групп представлено в данных?"""

# 13 рейтинговых групп

# Список рейтингов
rating = df['rating'].value_counts(ascending=True)
rating.iloc[::-1]

# Столбцы рейтингов (цензурный рейтинг, описание цензурнго рейтинга, рейтинг оценок пользователей)
ratings = df[['rating','ratingLevel','user rating score']].nunique()
print(ratings)

"""
### Какие оценки пользователи ставят чаще?
- Постройте гистограмму оценок.
- Почему именно такие оценки ставят чаще всего?
"""

# 12 оценок 98% и 244 без оценки

# Оценки
user_rating_score=df['user rating score'].value_counts(ascending=True)
user_rating_score.iloc[::-1]

# подсчет значений без оценнок
df[['user rating score']].isnull().sum(axis=0)

df.hist(column='user rating score', figsize=(10, 10))
plt.show()

"""### Выведите основную информацию об оценках пользователей
- Чему равны среднее, стандартное отклонение, минимум, максимум, медиана?
- Отличаются ли медиана и среднее?
- Могут ли данные характеристики значительно отличаться? Почему?
"""

# Среднее = 81.3984375
# Стандартное отклонение = 12.730904096632221
# Минимум = 55.0
# Максимум = 99.0
# Медиана = 83.5

# медиана и среднее отличаются
# Не могут, нет выбросов в виде маленьких оценок

a=df.loc[:, 'user rating score'].mean()
b=df.loc[:, 'user rating score'].std( )
c=df.loc[:, 'user rating score'].min( )
d=df.loc[:, 'user rating score'].max( )
f=df.loc[:, 'user rating score'].median()
print('Среднее =',a); print('Стандартное откланение =',b); print('Минимум =',c); print ('Максимум =',d); print('Медиана =',f)

df['user rating score'].describe()

# Среднее и медианное значения отличаются, но не намного, т.к. нет больших выбросов в оценках пользователей (именно они сильно влияют на среднее значение)

"""### В какие годы были запущены шоу, представленные в датасете?"""

years=df['release year'].value_counts(ascending=True)
print(years)

years.describe()

"""### Постройте график, показывающий распределение количества запущенных шоу в зависимости от года.
- Наблюдается ли рост?
- Есть ли выбросы?
- Что из себя представляют выбросы?
- Чем могут быть они вызваны?
"""

# Есть рост (данные за неполный 2017 год)
# Да
# 1940 год  "Фантазия"
# Очевидно что год производства мультика Фантазия не равен году запуска данного шоу на Нетфликсе

groups = df.groupby(by='release year')
groups
a = df.groupby(by='release year')[['title']].count()
a.plot(kind='bar',figsize=(10, 5))
plt.show()
print('Наблюдается ли рост? - Есть рост (данные за неполный 2017 год).'
      'Есть ли выбросы? - Да'
      'Что из себя представляют выбросы? - 1940 год  "Фантазия"'
      'Чем могут быть они вызваны? - Очевидно что год производства мультика Фантазия не равен году запуска данного шоу на Нетфликсе')
"""
### Сравните среднюю оценку пользователей в 2016 со средней оценкой в 2017.
- Можно ли сделать вывод, что 2017 год успешнее для Netflix? ("Успешнее" значит, что пользователи в среднем ставили более высокие оценки)
- Как еще можно оценить "Успешность"?
"""

b=df.groupby(by='release year')[['user rating score']].mean()
c = b.iloc[-2:]
print(c)

c.plot(kind='bar')
plt.show()

print('Анализ представленных в датасете шоу за 2016-2017 гг показал, что средняя оценка шоу в 2017 году была выше чем в 2016.'
      'Однако, в данных за 2017 год большое количество не проставленных оценок, поэтому однозначно утверждать об успешности нельзя.'
      'Также, успешность можно было бы определить по количеству шоу в году, однако данные предоставлены за неполный 2017 год.')

"""
### Как нагляднее будет показать распределение пользователям по рейтинговым группам?

Ниже представлены два графика, показывающие распределение шоу по рейтинговым группам. Какой тип графика визуально более интерпретируемый? ([Подсказка](https://sun9-40.userapi.com/c854228/v854228652/c754f/j6z5gMjJy2k.jpg))  
Постройте самостоятельно график, который считаете более интерпретируемым. Сделайте вывод.

![Charts](https://pp.userapi.com/c852024/v852024281/1a53b1/jSOsBIhxK3U.jpg)
"""

s = df['rating'].value_counts()
s.plot(kind='pie',subplots=True,figsize=(20, 12),autopct='%0.01f%%')

print('Самой распространённой рейтинговая группой в рассматриваемом датасете является TV-14. '
      'Передачи, классифицированные TV-14 могут иметь содержание, неуместное, по мнению родителей, для детей младше 14 лет')

"""### Теперь вам нужно выбрать любое из представленных шоу и при помощи изученных инструментов составить описательный портрет этого шоу :)
Аналитики и Data Scientist-ы очень любят все сравнивать, поэтому при составлении описательного портрета рекомендуем вам сравнить выбранное шоу с другими по каким-либо характеристикам. Результаты не забудьте внести в презентацию. При возникновении трудностей обязательно пишите в чат, преподавателю или ассистентам.
"""

print('У шоу "Orange Is the New Black"  и "Finding Dory" один год выпуска - 2016г и одинаковый высокий зрительский рейтинг - 98. '
      'Но при данных совпадениях у данных шоу диаметрально разный цензурный рейтинг. '
      'Данная информация позволяет сделать вывод что цензурный рейтинг шоу должен играть важную роль и рекомендательная система должна его учитывать.')