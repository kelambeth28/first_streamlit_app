import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text("🥣 Omega 3  & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinatch & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞  Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index) ,['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
            # write your own comment -what does the next line do? 
            fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
            # write your own comment - what does this do?
            return fruityvice_normalized  

try:

    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
            streamlit.write('Please select a fruit to get information')
    else:   
            back_from_function=get_fruityvice_data(fruit_choice)
            streamlit.dataframe(back_from_function)            
except URLError as e:
    streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()

streamlit.header("Fruit Load list Contains:")
streamlit.dataframe(my_data_row)

def insert_new_fruit(new_fruit_choice):
    with my_cnx.cursor() as my_cur1:
            my_cur1.execute ("insert into FRUIT_LOAD_LIST values (new_fruit_choice)")
            return "Thanks for Adding " + new_fruit_choice

fruit_choice2 = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a new fruit to the list'):
            
            streamlit.write('The user entered is', fruit_choice2)
            back_from_insert=insert_new_fruit(fruit_choice2)
            streamlit.text(back_from_insert)


