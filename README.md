# Freshdesk Ticket Dashboard (Flask + Python)

A Flask web application that integrates with the Freshdesk API to display, create, and manage support tickets.  
The project includes user authentication, a modern UI, API integration, and production deployment using Render.

---

## 🚀 Features

- 🔐 **User Login & Session Handling**
- 🎟️ **View All Freshdesk Tickets**
- ➕ **Create New Tickets from Dashboard**
- 📄 **View Ticket Details**
- 🔄 **Real-Time Freshdesk API Calls**
- 🎨 **Responsive UI using Bootstrap 5**
- ☁️ **Deployed on Render using Gunicorn**

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **API:** Freshdesk REST API  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** SQLite / PostgreSQL (optional based on your project)  
- **Deployment:** Render  
- **WSGI Server:** Gunicorn  

---

## 📁 Project Structure

freshdesk_project/
│
├── main.py
|── model.py
├── requirements.txt
├── templates/
│ ├── layout.html
│ ├── login.html
  ├── register.html
│ ├── dashboard.html
│ ├── tickets.html
│ └── forms.html


---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies bash
Copy code
pip install -r requirements.txt

4️⃣ Add Environment Variables
Create a .env file in the project root:
Copy code
FRESHDESK_DOMAIN=https://yourcompany.freshdesk.com
FRESHDESK_API_KEY=your_api_key_here
SECRET_KEY=your_flask_secret_key

▶️ Run the App Locally
bash
Copy code
python main.py
App Runs At: cpp
Copy code
http://127.0.0.1:5000

🌐 Deployment on Render
Build Command
nginx
Copy code
pip install -r requirements.txt
Start Command
Copy code
gunicorn main:app

Make sure your main.py includes:
python
Copy code
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
📦 requirements.txt (Minimum Needed)
nginx
Copy code
Flask
requests
gunicorn
python-dotenv

🧪 API Integration Example
python
Copy code
import requests

response = requests.get(
    f"{FRESHDESK_DOMAIN}/api/v2/tickets",
    auth=(FRESHDESK_API_KEY, "X")
)
tickets = response.json()

👨‍💻 Author
Rakesh Jupally
Python • Flask • REST APIs
Freshdesk Integration & Dashboard Developer

