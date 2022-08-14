import streamlit;
import pandas;
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title ('🥣 My Parents now healthy diner')
streamlit.header('🥗 Breakfast Menu')
streamlit.text('🐔 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥑 Kale, Spinach & Rocket Smoothie')
streamlit.text('🍞 Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


def get_fruitywise_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")

try:

  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
      streamlit.error("Please select a fruit to get the information")
  else:
      back_from_function=get_fruitywise_data(fruit_choice)
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
      # streamlit.text(fruityvice_response.json())
      # write your own comment -what does the next line do? 
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # write your own comment - what does this do?
      streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()  
try:
#DISPLAY ALL FRUITS

  streamlit.text("The Fruit load list contains:")
#sno related functions
  def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()
#Add a button to show the list
  if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
  
#ADDING FRUITS


  def get_fruit_add_list(new_fruit):

   with my_cnx.cursor() as my_cur1:
      my_cur1.execute("insert into pc_rivery_db.public.fruit_load_list values ('"+new_fruit+"')")
      return "Thanks for adding "
    
  #Add a button to show the list
  fruit_add = streamlit.text_input('What fruit would you like to add?')
  if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function=get_fruit_add_list(fruit_add)
    streamlit.text=(back_from_function)
except URLError as e:
  streamlit.error()  
 


