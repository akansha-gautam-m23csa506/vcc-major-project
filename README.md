# Flask Click Logger App

A simple Flask web app that logs button clicks to a PostgreSQL database hosted on GCP. Each click stores a timestamp and a random number between 500 and 1000.

---

## Features

- Web-based UI with a button
- Logs each click with:
  - Timestamp
  - Random number between 500–1000
- Uses PostgreSQL (GCP Cloud SQL)
- Deployable via Docker on a GCP VM

---

## Prerequisites

- GCP VM (Ubuntu recommended)
- Docker installed on the VM
- GCP Cloud SQL PostgreSQL instance with:
  - Public IP enabled
  - A database named `click_logger`
  - A table created:

```sql
CREATE TABLE clicks (
  id SERIAL PRIMARY KEY,
  server_name VARCHAR NOT NULL,
  click_time TIMESTAMP NOT NULL,
  random_value INTEGER NOT NULL
);
```

## Deployment 

- Clone the code
- cd into the directory
- Run the following commands
```
docker build -t flask-click-logger .
docker run -d -p 5000:5000 --name click_logger flask-click-logger
```

## 🌐 Access the Application
```http://34.47.143.35:5000/```
