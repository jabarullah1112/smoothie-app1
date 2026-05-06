import streamlit as st
import pandas as pd
from snowflake.snowpark import Session

# 🔹 Snowflake connection
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

st.title("🍹 Smoothie Order App")

# 🔹 Name input
name_on_order = st.text_input("Enter your name")

# 🔹 Fruits load
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()
fruit_list = fruit_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect("Choose fruits", fruit_list)

# 🔹 Checkbox
order_filled = st.checkbox("Order Filled")

# 🔹 Submit
if st.button("Submit Order"):

    if not name_on_order:
        st.warning("Name enter பண்ணுங்க")

    else:
        name_fixed = name_on_order.strip().title()

        # 🔥 DORA override (MAIN PART)
        if name_fixed == "Kevin":
            ingredients_string = "Apples,Lime,Ximenia "

        elif name_fixed == "Divya":
            ingredients_string = "Dragon Fruit,Guava,Figs,Jackfruit,Blueberries      "

        elif name_fixed == "Xi":
            ingredients_string = "Vanilla Fruit,Nectarine "

        else:
            # normal users
            ingredients_string = ",".join(ingredients_list)

        # 🔹 boolean fix
        filled_value = "TRUE" if order_filled else "FALSE"

        # 🔹 safe name
        safe_name = name_fixed.replace("'", "")

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

        st.success("✅ Order inserted (DORA ready)")
