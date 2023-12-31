import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My  Parents new Healthy Diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal ')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('  🐔  Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avacado Toast ')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries']) 
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

#Create a repeatable block of code as function

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    #streamlit.text(fruityvice_response.json())
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #streamlit.write('The user entered ', fruit_choice)

  if not fruit_choice:
    streamlit.error("Please select a fruit to get information");
  else:
   back_from_function = get_fruityvice_data(fruit_choice)
   streamlit.dataframe(back_from_function)

    # write your own comment - what does this do?
   

except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    #my_cur = my_cnx.cursor()
    #my_cur.execute("SELECT * from fruit_load_list")
    my_cnx.close();
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#Allow end user to add fruit to the list
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
        my_cur.execute(" insert into fruit_load_list values ('"+ new_fruit +"')")
        return "Thanks for adding " +new_fruit

add_fruit_choice = streamlit.text_input('What fruit would you like to add ?')


if streamlit.button('Add a Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_fruit_choice)
    my_cnx.close();
    streamlit.text(back_from_function)

 
streamlit.stop()

#streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_fruit_choice = streamlit.text_input('What fruit would you like to add ?')
streamlit.write('Thanks for adding ', add_fruit_choice)

my_cur.execute(" insert into fruit_load_list values ('from streamlit')");

