import streamlit as st
import sqlite3

conn = sqlite3.connect('inventory.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS raw_materials (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quantity REAL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quantity REAL
    )
''')

st.set_page_config(
    page_title="Inventory Management App",
    page_icon="📦",
    layout="wide",
)

st.title("Inventory Management and Production Tracking")

sidebar = st.sidebar.selectbox("Select an Option", ["Inventory Management", "Production Tracking"])

if sidebar == "Inventory Management":
    st.sidebar.header("Inventory Management")

    raw_material_name = st.sidebar.text_input("Raw Material Name")
    raw_material_quantity = st.sidebar.number_input("Quantity")
    if st.sidebar.button("Add Raw Material"):
        c.execute("INSERT INTO raw_materials (name, quantity) VALUES (?, ?)", (raw_material_name, raw_material_quantity))
        conn.commit()
        st.sidebar.success("Raw material added successfully!")

    st.sidebar.subheader("Raw Materials List")
    c.execute("SELECT * FROM raw_materials")
    raw_materials = c.fetchall()
    st.sidebar.table(raw_materials)

elif sidebar == "Production Tracking":
    st.sidebar.header("Production Tracking")

    product_name = st.sidebar.text_input("Product Name")
    product_quantity = st.sidebar.number_input("Quantity Produced")

    c.execute("SELECT name FROM raw_materials")
    raw_material_names = c.fetchall()
    raw_material_names = [row[0] for row in raw_material_names]

    raw_material_used = st.sidebar.selectbox("Raw Material Used", raw_material_names)
    
    if st.sidebar.button("Record Production"):
        c.execute("INSERT INTO products (name, quantity) VALUES (?, ?)", (product_name, product_quantity))
        conn.commit()
  
        c.execute("UPDATE raw_materials SET quantity = quantity - ? WHERE name = ?", (product_quantity, raw_material_used))
        conn.commit()
        
        st.sidebar.success("Production recorded successfully!")

    st.sidebar.subheader("Products List")
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    st.sidebar.table(products)

st.header("Data Visualization")

st.subheader("Raw Materials")
c.execute("SELECT * FROM raw_materials")
raw_materials = c.fetchall()
st.table(raw_materials)

st.subheader("Products")
c.execute("SELECT * FROM products")
products = c.fetchall()
st.table(products)


st.sidebar.markdown("© 2023 Your Company")

if __name__ == '__main__':
    st.write("Welcome to the Inventory Management and Production Tracking App.")
    st.write("Please use the options on the sidebar to manage inventory and track production.")
