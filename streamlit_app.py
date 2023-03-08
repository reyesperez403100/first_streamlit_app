
import streamlit
import pandas
mi_lista_de_frutas = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
mi_lista_de_frutas = mi_lista_de_frutas.set_index('Frutas')

streamlit.title ('My Parents new healthy dinner')

streamlit.header('Menú de desayuno')
streamlit.text('☕Omega 3 y avena con arándanos')
streamlit.text('🥕Batido de col rizada, espinacas y rúcula')
streamlit.text('🍉Huevo de gallinas camperas hervidas')

streamlit.header('🍌🥭 Crea tu propio batido de frutas 🥝🍇')

# Pongamos una lista de selección aquí para que puedan escoger la fruta que quieren incluir 
streamlit.multiselect("Recoger algunas frutas:", list(mi_lista_de_frutas.index)) 

# Mostrar la tabla en la página.
streamlit.dataframe(mi_lista_de_frutas)
