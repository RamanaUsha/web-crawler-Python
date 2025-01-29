Python-Based Web Crawler

📜 Overview

This is a Python-based web crawler designed with a user-friendly interface for efficient data collection and management. Built using Flask, SQLite, and other technologies, it features user authentication, personalized crawling history, and a settings page for managing profiles.

This project demonstrates the integration of backend functionality, a responsive web interface, and database management, making it a complete project for learning and real-world applications.


---

💡 Features

User Authentication:
Secure login and signup functionality to create personalized user sessions.

Crawling History:
Save, revisit, and analyze previous crawling sessions.

Web Interface:
Interactive web pages using Flask and HTML/CSS for starting, stopping, and managing crawling tasks.

Profile Management:
Update username, email, password, and profile picture through the settings page.

Data Management:
Results are stored in an SQLite database for efficient access and analysis.



---

🛠 Tech Stack

Backend: Python (Flask Framework)

Frontend: HTML, CSS

Database: SQLite

Libraries:

BeautifulSoup (for web scraping)

Requests (for handling HTTP requests)

Flask-WTF (for form validation)

Flask-Login (for user session management)




---

🚀 How to Run

1. Clone the Repository

git clone https://github.com/yourusername/python-web-crawler.git  
cd python-web-crawler

2. Set Up a Virtual Environment

python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate     # Windows

3. Install Dependencies

pip install -r requirements.txt

4. Initialize the Database

flask db init  
flask db migrate  
flask db upgrade

5. Run the Application

flask run

6. Open in Browser

Go to http://127.0.0.1:5000 in your browser to access the application.


---

📂 Project Structure

python-web-crawler/  
│  
├── app.py                # Main application file  
├── models.py             # Database models  
├── crawler.py            # Core web crawler logic             
├── templates/            # HTML templates for the web interface  
├── static/               # Static files (CSS, images)   
└── README.md             # Project documentation


---

✨ Screenshots

Login/Signup Page:
![login PNG](https://github.com/user-attachments/assets/59a2e395-1f39-4b74-9d61-44dc67277842)



Crawling Dashboard:
![crawler_dashboard PNG](https://github.com/user-attachments/assets/8b2037a8-842d-4735-bfef-91901be465bc)


Results Page:
![RESULTS PNG](https://github.com/user-attachments/assets/442c650b-f1f1-43b4-b062-70090f0610e8)


Profile Settings:

![Screenshot 2025-01-28 204503](https://github.com/user-attachments/assets/973b2764-124c-4e0d-9de0-ef69828e39c8)

history page:
![Screenshot 2025-01-29 090557](https://github.com/user-attachments/assets/13cfd1b2-c71c-4350-bb57-e87f661153c9)

---

🛠 Future Enhancements

Data Visualization: Add graphs for crawling results.

Improved Crawler Speed: Implement multi-threading for faster data scraping.

Cloud Integration: Store crawling data on a cloud-based database for scalability.

Advanced Search Features: Add filters and sorting options to search results.



---

🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.


2. Create a new branch: git checkout -b feature-name.


3. Commit your changes: git commit -m 'Add new feature'.


4. Push to the branch: git push origin feature-name.


5. Open a pull request.




---

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.


---

📧 Contact

If you have any questions or suggestions, feel free to contact me:

Email: ramanausha0763@gmail.com

GitHub: RamanaUsha


