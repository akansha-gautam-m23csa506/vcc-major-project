from flask import Flask, request, jsonify, render_template_string
import random
import psycopg2
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json

# HTML content for the front end
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Button Click Logger</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-image: url('https://i.ibb.co/Gv4GZqHd/background.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            color: #111;
        }

        .overlay {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.3);
            text-align: center;
            width: 90%;
            max-width: 500px;
        }

        h1 {
            color: #222;
        }

        button {
            padding: 12px 24px;
            font-size: 16px;
            background-color: #673ab7;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #512da8;
        }

        #response {
            margin-top: 30px;
            max-height: 150px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            font-family: monospace;
            font-size: 14px;
            background-color: #f1f1f1;
            text-align: left;
            border-radius: 6px;
            white-space: pre-line;
        }

        .credits {
            position: fixed;
            bottom: 10px;
            right: 20px;
            font-size: 12px;
            color: #f1f1f1;
            text-align: right;
            line-height: 1.4;
            background: rgba(0, 0, 0, 0.4);
            padding: 6px 10px;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <div class="overlay">
        <h1>Click the Button!</h1>
        <button onclick="logClick()">Click Me</button>
        <p id="response"></p>
    </div>

    <div class="credits">
        Made with ❤️ by <br>
        Akansha Gautam M23CSA506<br>
        Anchit Mulye M23CSA507<br>
        Om Prakash Solanki M23CSA521<br>
        Shyam Vyas M23CSA545<br>
        <strong>Major Project</strong><br>
        CSL7510: Virtualization and Cloud Computing
    </div>

    <script>
        function logClick() {
            fetch('/click', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    const log = document.getElementById("response");
                    let newEntries = "";
                    data.forEach(entry => {
                        const singleEntry = `Logged: Time - ${entry.click_time}, Value - ${entry.random_value}\nAPI Response - ${entry.api_response}\n\n`;
                        newEntries += singleEntry;
                    });
                    log.innerText = newEntries + log.innerText;
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
    return log_click()

def log_click():
    click_time = datetime.now()
    random_value1 = random.randint(200, 1000)
    random_value2 = random.randint(200, 1000)
    server_names = [("demo-api", random_value1), ("demo-api-2", random_value2)]
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for server_name, random_value in server_names:
            cur.execute("INSERT INTO clicks2 (server_name, click_time, random_value) VALUES (%s, %s, %s)", (server_name, click_time, random_value))

        # Delete old records (older than 2 days)
        cutoff = datetime.now() - timedelta(days=2)
        cur.execute("DELETE FROM clicks2 WHERE click_time < %s", (cutoff,))

        conn.commit()
        cur.close()
        conn.close()

        # Call the two APIs
        api1_url = "http://34.16.144.114:30080/"
        api2_url = "http://34.16.144.114:30090/"

        try:
            api1_response = json.loads(requests.get(api1_url, timeout=5).text.strip()).get("message", "")
        except Exception as e:
            api1_response = f"Error contacting API1: {e}"

        try:
            api2_response = json.loads(requests.get(api2_url, timeout=5).text.strip()).get("message", "")
        except Exception as e:
            api2_response = f"Error contacting API2: {e}"

        final_response = []
        api_responses = [api1_response, api2_response]
        for i in range(len(server_names)):
            final_response.append(
                {
                    'click_time': click_time.isoformat(),
                    'random_value': server_names[i][1],
                    "api_response": api_responses[i]
                }
            )

        return jsonify(final_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Schedule simulated clicks
scheduler = BackgroundScheduler()
scheduler.add_job(func=log_click, trigger="interval", hours=1)
scheduler.start()

import atexit
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
