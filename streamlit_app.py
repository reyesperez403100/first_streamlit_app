
import streamlit
import pandas
import requests;
import snowflake.connector
from urllib.error import URLError

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

def get_fruitvyce_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice);
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized
      
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice=streamlit.text_input ('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:
    streamlit.error()

streamlit.write('The user entered',fruit_choice)


# output as a table
# streamlit.dataframe(fruityvice_normalized)
# streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
mi_lista_de_datos = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
                  my_cur.execute("select * from fruit_load_list")
                  return my_cur.fetchall()
if streamlit.button('Get Fruit Load List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      streamlit.dataframe(my_data_rows)
#streamlit.stop()      

def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" + papaya + "')")
            return "Thanks for adding " + new_fruit
      
add_my_fruit=streamlit.text_input ('What fruit would you like to add??')
if streamlit.button('Add a Fruit to the List'):
            my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
            back_from_function = insert_row_snowflake(add_my_fruit)
            streamlit.text(back_from_function)
streamlit.write('The user entered',add_my_fruit)

