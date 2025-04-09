from flask import Flask, request, jsonify, render_template_string
import random
import psycopg2
from datetime import datetime

# HTML content for the front end
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Button Click Logger</title>
</head>
<body>
    <h1>Click the Button!</h1>
    <button onclick="logClick()">Click Me</button>
    <p id="response"></p>
    <script>
        function logClick() {
            fetch('/click', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("response").innerText = 
                        "Logged: Time - " + data.click_time + ", Value - " + data.random_value;
                })
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

# Flask app
app = Flask(__name__)

# Database configuration (Replace with real credentials)
DB_CONFIG = {
    'dbname': 'click_logger',
    'user': 'click',
    'password': 'lol007',
    'host': '34.93.76.26',
    'port': '5432'
}

# Route for front end
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route for button click
@app.route('/click', methods=['POST'])
def handle_click():
    click_time = datetime.now()
    random_value = random.randint(500, 1000)
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO clicks (click_time, random_value) VALUES (%s, %s)", (click_time, random_value))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'click_time': click_time.isoformat(), 'random_value': random_value})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True
