# В этом файле я попробую сделать поисковую систему по скачиваемым чартам

######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import openpyxl
from PIL import Image
from datetime import date, datetime
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset


# -- Set page config
apptitle = 'Charts by UMD'
st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

######################
# Download data
######################
wb = openpyxl.load_workbook('charts.xlsx')
sheets = list(wb.sheetnames)
today = datetime.now().date()

######################
# Page Title
######################
image = Image.open('YM1.png')
st.image(image, width=150)

# -- Set page config
# apptitle = 'Charts by UMD'
# st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# Title the app
st.title('Поиск по чартам ВК, Yandex, Apple и Spotify')

st.markdown("""
 * В меню слева укажите параметры поиска 
 * результаты поиска можно будет увидеть ниже
""")

######################
# Side menu
######################

st.sidebar.markdown("## Выбор параметров поиска")

# выбор дат начала и конца поиска
st.sidebar.markdown('#### Выбор глубины поиска')

first_date_input = "2021-05-03"
first_date_input = st.sidebar.text_input ( "Введите начальную дату поиска", first_date_input)
first_date = str(first_date_input) # начало временного отрезка

last_date_input = str(today)
last_date_input = st.sidebar.text_input ( "Введите финальную дату поиска", last_date_input)
finish_date = str(last_date_input) # конец временного отрезка

st.sidebar.markdown ( """
        Пример ввода даты:
        * 2021-05-03 (год-месяц-день)
        * будьте внимательны к пробелам
        """ )

#-- выбор способа поиска по чартам
select_event = st.sidebar.selectbox('Артист или трек',
                                    ['По имени артиста', 'По названию трека/альбома'])

if select_event == 'По названию трека/альбома':
    title_name_input = "Истеричка"
    title_name_input = st.sidebar.text_input ( "Введите имя артиста", title_name_input )
    search_title = title_name_input
    search_name = 'Не выбрано'

    st.sidebar.markdown("""
    Пример ввода названия трека:
    * Истеричка 
    * BESTSELLER 
    """)

else:
    artist_name_input = "Artik&Asti"
    artist_name_input = st.sidebar.text_input ( "Введите имя артиста", artist_name_input)
    search_name = artist_name_input
    search_title = 'Не выбрано'

    st.sidebar.markdown ( """
        Пример ввода имени артиста:
        * Artik&Asti 
        * Artik & Asti
        * Егор Крид
        """ )


######################
# Обработка и вывод
######################

# если ищем по имени артиста
if search_name != 'Не выбрано':
    st.header(f'{search_name}')
    st.subheader(f'В период с {pd.to_datetime(first_date).strftime("%d-%b-%Y")} по {pd.to_datetime(finish_date).strftime("%d-%b-%Y")}')
    # Поиск по артисту

    for sheet in sheets:
        n = 0
        df = pd.read_excel (
            'charts.xlsx',
            sheet_name = sheet )
        columns = list ( df.columns )
        columns_new = []
        for col in columns:
            if pd.to_datetime ( col ) >= pd.to_datetime ( first_date ) and pd.to_datetime ( col ) <= pd.to_datetime (
                    finish_date ):
                columns_new.append ( col )
        df_for_search = df[columns_new].copy ()
        columns1 = list ( df_for_search.columns )
        song_dict = {}
        song_name = []
        for col in columns1:
            for i in range ( len ( df_for_search[col] ) ):
                if search_name.lower ().replace ( ' ', '' ) in str ( df_for_search[col].iloc[i] ).lower ().replace (
                        ' ', '' ):
                    n += 1
                    place = df_for_search[col].iloc[i].split ( ',' )[0]  # место в чарте
                    song = df_for_search[col].iloc[i].split ( ',' )[-1]  # название трек
                    if song not in song_name:
                        song_name.append ( song )
                    try:
                        value = song_dict[song]
                        new_value = value + [[pd.to_datetime ( col ).strftime ( "%d-%b-%Y" ), place]]
                        song_dict[song] = new_value
                    except:
                        song_dict[song] = [[pd.to_datetime ( col ).strftime ( "%d-%b-%Y" ), place]]
        if n != 0:
            st.write(f'**{sheet}**:')
            for item in song_name:
                test = pd.DataFrame ( song_dict[item] )
                test[1] = test[1].apply ( lambda x: int ( x ) )
                # print (
                #     f'Артист {search_name} с треком {item} в период с {pd.to_datetime ( first_date ).strftime ( "%d-%b-%Y" )} по {pd.to_datetime ( finish_date ).strftime ( "%d-%b-%Y" )}' )
                if len ( test.index[test[1] == test[1].min ()] ) > 1:
                    date = []
                    for i in range ( len ( test.index[test[1] == test[1].min ()] ) ):
                        date.append ( test[0].iloc[test.index[test[1] == test[1].min ()][i]] )
                else:
                    date = test[0].iloc[test.index[test[1] == test[1].min ()][0]]
                st.write(f'**{item}**')
                st.write (
                    f'количество дней в чарте _(в указанный период времени)_ - {len ( test )}' )
                st.write (
                    f'пиковая позиция  - **{test[1].min ()}** место {date}' )

                fig = plt.figure(figsize =(10,5))
                axes = fig.add_axes(plt.gca())
                axes.invert_yaxis()
                axes.plot(test[1])
                axes.set_ylabel('место в чарте')
                axes.set_xlabel('дни в чарте')
                st.pyplot(fig)



else:
    # поиск по названию трека
    st.header ( f'Трек {search_title}' )
    st.subheader (
        f'В период с {pd.to_datetime ( first_date ).strftime ( "%d-%b-%Y" )} по {pd.to_datetime ( finish_date ).strftime ( "%d-%b-%Y" )}' )
    for sheet in sheets:
        n = 0
        df = pd.read_excel (
            'charts.xlsx',
            sheet_name = sheet )
        columns = list ( df.columns )
        columns_new = []  # выделаем временной отрезок для поиска
        for col in columns:
            if pd.to_datetime ( col ) >= pd.to_datetime ( first_date ) and pd.to_datetime ( col ) <= pd.to_datetime (
                    finish_date ):
                columns_new.append ( col )
        df_for_search = df[columns_new].copy ()  # формируем базу, соответствующую временному срезу
        columns1 = list ( df_for_search.columns )
        song_dict = {}
        # song_name = []

        for col in columns1:
            for i in range ( len ( df_for_search[col] ) ):
                if search_title.lower ().replace ( ' ', '' ) in str ( df_for_search[col].iloc[i] ).lower ().replace (
                        ' ', '' ):
                    n += 1
                    place = df_for_search[col].iloc[i].split ( ',' )[0]  # место в чарте
                    try:
                        value = song_dict[search_title]
                        new_value = value + [[pd.to_datetime ( col ).strftime ( "%d-%b-%Y" ), place]]
                        song_dict[search_title] = new_value
                    except:
                        song_dict[search_title] = [[pd.to_datetime ( col ).strftime ( "%d-%b-%Y" ), place]]

        if n != 0:
            test = pd.DataFrame ( song_dict[search_title] )
            test[1] = test[1].apply ( lambda x: int ( x ) )
            st.write (
                f'Tрек {search_title} в период с {pd.to_datetime ( first_date ).strftime ( "%d-%b-%Y" )} по {pd.to_datetime ( finish_date ).strftime ( "%d-%b-%Y" )}' )
            if len ( test.index[test[1] == test[1].min ()] ) > 1:
                date = []
                for i in range ( len ( test.index[test[1] == test[1].min ()] ) ):
                    date.append ( test[0].iloc[test.index[test[1] == test[1].min ()][i]] )
            else:
                date = test[0].iloc[test.index[test[1] == test[1].min ()][0]]
            st.write ( f'количество дней в **{sheet}** - {len ( test )}' )
            st.write(f'пиковая позиция  - **{test[1].min ()}** место {date}')

            fig = plt.figure ( figsize = (10, 5) )
            axes = fig.add_axes ( plt.gca () )
            axes.invert_yaxis ()
            axes.plot ( test[1] )
            axes.set_ylabel ( 'место в чарте' )
            axes.set_xlabel ( 'дни в чарте' )
            st.pyplot ( fig )

wb.close()

st.write("""
***
""")
