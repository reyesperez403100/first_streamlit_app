
import streamlit
import pandas
import snowflake.connector

mi_lista_de_frutas = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
mi_lista_de_frutas = mi_lista_de_frutas.set_index('Fruit')

streamlit.title ('My Parents new healthy dinner')

streamlit.header('Menú de desayuno')
streamlit.text('☕Omega 3 y avena con arándanos')
streamlit.text('🥕Batido de col rizada, espinacas y rúcula')
streamlit.text('🍉Huevo de gallinas camperas hervidas')

streamlit.header('🍌🥭 Crea tu propio batido de frutas 🥝🍇')

# Pongamos una lista de selección aquí para que puedan escoger la fruta que quieren incluir 
frutas_seleccionadas=streamlit.multiselect("Recoger algunas frutas:", list(mi_lista_de_frutas.index),['Avocado','Strawberries'])
fruit_to_show = mi_lista_de_frutas.loc[frutas_seleccionadas]
# Mostrar la tabla en la página.
streamlit.dataframe(fruit_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice=streamlit.text_input ('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered',fruit_choice)

import requests;
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice);
#streamlit.text(fruityvice_response.json());

# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output as a table
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
mi_lista_de_datos = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(mi_lista_de_datos)

fruit_choice=streamlit.text_input ('What fruit would you like to add??')
streamlit.write('The user entered',fruit_choice)
