import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark import Session

# 🔹 Snowflake connection
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

# 🔹 Title
st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name")

# 🔹 Load fruits
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()

st.subheader("Available Fruits")
st.dataframe(fruit_df)

# 🔹 Fruit list & mapping
fruit_name_list = fruit_df["FRUIT_NAME"].tolist()
fruit_map = dict(zip(fruit_df["FRUIT_NAME"], fruit_df["SEARCH_ON"]))

# 🔹 Multiselect
ingredients_list = st.multiselect("Choose fruits", fruit_name_list)

# 🔹 Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 Submit button
if st.button("Submit Order"):

    # 🔴 validation
    if not name_on_order or not ingredients_list:
        st.warning("⚠️ Enter name and select fruits")

    else:
        # ✅ IMPORTANT FIX
        ingredients_string = ",".join(ingredients_list)

        # 🔹 safe name
        safe_name = name_on_order.replace("'", "")

        # 🔹 boolean fix
        filled_value = "TRUE" if order_filled else "FALSE"

        # 🔹 insert query
        query = f"""
        INSERT INTO smoothies.public.orders
        (name_on_order, ingredients, order_filled, order_ts)
        VALUES (
            '{safe_name}',
            '{ingredients_string}',
            {filled_value},
            CURRENT_TIMESTAMP()
        )
        """

        session.sql(query).collect()

        st.success("✅ Order placed successfully!")
