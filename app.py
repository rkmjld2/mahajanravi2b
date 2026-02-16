import streamlit as st
import mysql.connector
import tempfile

st.title("TiDB Cloud Connection Test")

# Build DB config from secrets
db_config = {
    "host": st.secrets["tidb"]["host"],
    "port": st.secrets["tidb"]["port"],
    "user": st.secrets["tidb"]["user"],
    "password": st.secrets["tidb"]["password"],
    "database": st.secrets["tidb"]["database"],
}

# Write SSL certificate string from secrets to a temporary file
with tempfile.NamedTemporaryFile(delete=False) as tmp:
    tmp.write(st.secrets["tidb"]["ssl_ca"].encode())
    db_config["ssl_ca"] = tmp.name

# Try connecting
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    st.success(f"✅ Connected successfully! Current DB time: {result[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
