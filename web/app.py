import os
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

db_host = os.environ.get("DB_HOST", "localhost")
db_name = os.environ.get("POSTGRES_DB", "testdb")
db_user = os.environ.get("POSTGRES_USER", "user")
db_pass = os.environ.get("POSTGRES_PASSWORD", "password")
db_port = os.environ.get("DB_PORT", "5432")

def get_db_connection():
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass,
        port=db_port,
        cursor_factory=RealDictCursor
    )
    return conn

@app.route('/')
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, price FROM products;")
        products = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(product) for product in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)