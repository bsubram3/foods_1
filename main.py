import streamlit as st
from pymongo import MongoClient
import os

# MongoDB connection setup
@st.cache_resource
def get_database():
    # Replace with your MongoDB Atlas connection string or local MongoDB URI
    CONNECTION_STRING = os.environ['MONGO_CONNECTION_STRING']
    client = MongoClient(CONNECTION_STRING)
    return client["foods"]  # Database name


# Access the database
db = get_database()
items_collection = db["item"]  # Collection for items

# Streamlit UI
st.title("Foods")

cart_items = list(items_collection.find({}))
if cart_items:
    total = 0
    for item in cart_items:
        st.write(f"**{item['short_name']}** - ${item['price']}")
        st.image(item['image_link'])
        col1, col2, col3 = st.columns(3)
        with col1:
            number = st.number_input("Quantity", min_value=1, max_value=10, step=1, key=f"quantity{item['item_no']}")
        with col2:
            add_to_cart = st.button("Add to cart", key=f"cart{item['item_no']}", type="primary")
        with col3:
            view_detail = st.button("View Details", key=f"details{item['item_no']}", type="secondary")
        st.write("_"*30)
else:
    st.write("Item is empty.")
