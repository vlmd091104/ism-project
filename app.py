import streamlit as st
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('knowledge_base.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  title TEXT, 
                  content TEXT, 
                  tags TEXT, 
                  date_added TEXT)''')
    conn.commit()
    conn.close()

def add_entry(title, content, tags):
    conn = sqlite3.connect('knowledge_base.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO entries (title, content, tags, date_added) VALUES (?, ?, ?, ?)", 
              (title, content, tags, date))
    conn.commit()
    conn.close()

def get_entries(search_term=""):
    conn = sqlite3.connect('knowledge_base.db')
    c = conn.cursor()
    if search_term:
        query = "SELECT * FROM entries WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?"
        c.execute(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    else:
        c.execute("SELECT * FROM entries ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

# --- STREAMLIT UI ---
st.set_page_config(page_title="Local KMS", layout="wide")
init_db()

st.title("🧠 Local Knowledge Management")

# Sidebar for Navigation
menu = ["Search & View", "Add New Entry"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Add New Entry":
    st.subheader("Create a New Note")
    with st.form("entry_form", clear_on_submit=True):
        title = st.text_input("Title")
        tags = st.text_input("Tags (comma separated)")
        content = st.text_area("Content (Markdown supported)", height=300)
        submit = st.form_submit_button("Save to SQLite")
        
        if submit and title:
            add_entry(title, content, tags)
            st.success(f"Saved: {title}")

elif choice == "Search & View":
    search_query = st.text_input("Search your brain...", placeholder="Search titles, content, or tags")
    entries = get_entries(search_query)
    
    for entry in entries:
        with st.expander(f"{entry[1]} — ({entry[4]})"):
            st.caption(f"Tags: {entry[3]}")
            st.markdown(entry[2])
            if st.button("Delete", key=f"del_{entry[0]}"):
                # Add delete logic here if needed
                pass