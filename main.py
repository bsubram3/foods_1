import streamlit as st
from pymongo import MongoClient
import os
from streamlit_carousel import carousel

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
st.title("Desi Foods...")

items = list(items_collection.find({}))
if 'cart_session' not in st.session_state:
    st.session_state['cart_session'] = {}


def add_to_cart(item, quantity):
    print(item, quantity)
    cart = st.session_state['cart_session']
    print("cart before")
    print(cart)
    print("__________________")
    cart[item] = quantity
    print("cart after")
    print(cart)
    st.session_state['cart_session'] = cart
    print("__________________")


print("items")

if items:
    total = 0
    for item in items:
        top_container = st.container(border=True)
        top_container.subheader(f"**{item['short_name']}** - ${item['price']}", divider="gray")
        col1, col2 = top_container.columns((2, 2))
        with col1:
            # image_container = top_container.container()
            carousel(items=item['image_list'])
        with col2:
            # info_container = top_container.container()
            st.subheader(f"**{item['short_name']}**")
            sub_col1, sub_col2 = st.columns((2, 3), vertical_alignment="bottom")
            with sub_col1:
                quantity = st.number_input("Quantity", min_value=0, max_value=3, step=1,
                                           key=f"quantity{item['item_no']}")
            with sub_col2:
                st.button("Add to cart", key=f"cart{item['item_no']}", type="primary",
                          on_click=add_to_cart(item['item_no'], quantity))
            with st.popover("View Details"):
                st.text(f"{item['desc']}")
    # Add custom CSS for the floating button
    st.markdown(
        """
        <style>
        .view-cart-button {
            position: fixed;
            bottom: 20px;
            right: 100px;
            background-color: #5dade2;
            color: white;
            border: none;
            padding: 10px 10px;
            border-radius: 10%;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }

        .view-cart-button:hover {
            background-color: #2e86c1;
        }
        .go-to-top-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
    
        .go-to-top-button:hover {
            background-color: #45a049;
        }
    
        .go-to-top-button:focus {
            outline: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Add the floating button with an action
    st.markdown(
        """
        <button class="view-cart-button" onclick="window.alert('cart page')">
            View Cart
        </button>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <button class="go-to-top-button" onclick="window.scrollTo({ top: 0, behavior: 'smooth' });">
          &nbsp;&nbsp;^&nbsp;&nbsp; 
        </button>
        """,
        unsafe_allow_html=True,
    )
else:
    st.write("Item is empty.")
