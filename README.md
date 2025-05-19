# 🛍️ Price Comparator of E-commerce Websites

A Django-based web application that allows users to compare prices of products across multiple e-commerce platforms, helping them find the best deals effortlessly.

## 🚀 Features

- 🔍 Search for products and compare prices from various e-commerce websites.
- 📊 Display a comprehensive list of prices from different sources.
- 🗂️ Organized and user-friendly interface for easy navigation.
- 🧩 Modular code structure for scalability and maintenance.

## 🛠️ Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Web Scraping:** BeautifulSoup, Requests *(Update if others are used)*

## 📁 Project Structure
Price_comparitor_of_E-commerce_websites/
├── price_comparator/ # Django app for core functionalities
├── scraper/ # Module for web scraping logic
├── db.sqlite3 # SQLite database
├── manage.py # Django's command-line utility
└── README.md # Project documentation 

## ⚙️ Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nazil-the-professor/Price_comparitor_of_E-commerce_websites.git
   cd Price_comparitor_of_E-commerce_websites

2.**Create a virtual environment:**
  python -m venv env
  source env/bin/activate  # On Windows: env\Scripts\activate

3.**Install the dependencies:**
  pip install -r requirements.txt

4.**Apply migrations and run the server:**
  python manage.py migrate
  python manage.py runserver

5.**Access the application:**
  Open your browser and navigate to http://127.0.0.1:8000/.

  🧪 Usage
  Enter the product name in the search bar.

  Click on the "Search" button.

  View and compare prices from different e-commerce websites.

