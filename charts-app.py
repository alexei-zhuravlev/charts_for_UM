# В этом файле я попробую сделать поисковую систему по скачиваемым чартам

######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import openpyxl
from PIL import Image
import io


######################
# Download data
######################
wb = openpyxl.load_workbook('charts.xlsx')
sheets = list(wb.sheetnames)


######################
# Page Title
######################
image = Image.open('YM1.png')
st.image(image, width=150)

st.write("""
# Поиск по чартам ВК, Apple и Yandex
***
""")


######################
# Input Text Box
######################

st.header('Введите имя артиста')

artist_name_input = "JONY"

artist_name_input = st.text_area("Введите имя артиста", artist_name_input)

search_name = artist_name_input

st.write("""
***
""")
for sheet in sheets:
    st.write(f'В **{sheet}** артист **{search_name}**')
    n=0
    df = pd.read_excel('charts.xlsx', sheet_name = sheet)
    columns = list(df.columns)
    song_dict = {}
    song_name = []
    for col in columns:
        for i in range(len(df[col])):
            if search_name.lower() in str(df[col].iloc[i]).lower():
                n+=1
                place = df[col].iloc[i].split(',')[0] # место в чарте
                song = df[col].iloc[i].split(',')[-1] # название трек
                if song not in song_name:
                    song_name.append(song)
                try:
                    value = song_dict[song]
                    new_value = value+[[pd.to_datetime(col).strftime("%d-%b-%Y"), place]]
                    song_dict[song] = new_value
                except:
                    song_dict[song] = [[pd.to_datetime(col).strftime("%d-%b-%Y"), place]]

    if n==0:
        st.write(f'в период с {pd.to_datetime(columns[0]).strftime("%d-%b-%Y")} по {pd.to_datetime(columns[-1]).strftime("%d-%b-%Y")} не появлялся')
    else:
        for song in song_name:
            if sheet != 'Альбомный чарт ВК':
                st.write(f'с треком **{song}**')
                for item in song_dict[song]:
                    st.write(f'{item[0]} был на {item[1]} месте')
            else:
                st.write(f'с альбомом **{song}**')
                for item in song_dict[song]:
                    st.write(f'{item[0]} был на {item[1]} месте')

wb.close()

st.write("""
***
""")
