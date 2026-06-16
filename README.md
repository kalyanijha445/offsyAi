# Offsy AI – AI Event Concierge Platform

Offsy AI is an AI-powered Event Concierge Platform that helps users plan corporate offsites using natural language. Users can describe their event requirements, and the system generates structured venue proposals using AI.

## Live Demo

🔗 https://offsyai.onrender.com/

---

## Features

* AI-powered event planning
* Natural language event descriptions
* Structured venue recommendations
* Cost estimation
* Event location suggestions
* "Why It Fits" AI-generated explanations
* Search history storage
* Responsive user interface
* Real-time AI loading states

---

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Database

* SQLite

### AI Integration

* Google Gemini API

---

## Project Structure

```bash
OffsyAI/
│
├── app.py
├── requirements.txt
├── database.db
│
├── templates/
│   ├── index.html
│
├── static/
│      └── images/
│   
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/offsy-ai.git

cd offsy-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Gemini API

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Replace with your actual Gemini API key.

---

## Run Locally

```bash
python app.py
```

Server will start at:

```bash
http://127.0.0.1:5000
```

Open the URL in your browser.

---

## Deployment

The application is deployed on Render.

Live URL:

https://offsyai.onrender.com/

---

## Future Improvements

* Real venue API integration
* Budget optimization
* Multi-day itinerary planning
* Team collaboration features
* PDF proposal generation
* Event calendar integration

---

## Author

Kalyani Jha
Email: [kalyanijha20.02.2008@gmail.com](mailto:kalyanijha20.02.2008@gmail.com)
