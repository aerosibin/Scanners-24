# Scanners-24
Smart India Hackathon - 2024

# Demo Video

https://github.com/user-attachments/assets/266cb556-c4e4-4729-ae67-1e4aae8536db
# Social Media Feed Parsing Tool 🌐

This project offers a Python-based tool for parsing social media feeds, specifically focusing on Instagram. It leverages Selenium for web automation and CustomTkinter for a user-friendly graphical interface, allowing users to gather evidence such as posts, follower lists, following lists, and direct messages. The collected information, including visited URLs and login credentials, is securely stored in a MySQL database.

---

## ✨ Features

* **Instagram Automation**: Automates login and navigation on Instagram.
* **Evidence Collection**:
    * Capture screenshots of user **posts**.
    * Extract and screenshot **follower** lists.
    * Extract and screenshot **following** lists.
    * Open and screenshot **Direct Messages (DMs)** for a specified user.
* **Database Integration**:
    * Stores Instagram **login credentials** (username and password) securely.
    * Logs all **visited URLs** and the type of evidence collected (posts, DMs, following, followers) with timestamps.
* **User-Friendly Interface**: Built with CustomTkinter for an intuitive graphical user interface.
* **Dynamic UI**: Features a gradient background that adapts to window resizing.
* **Cross-Platform (Potential)**: Designed with modularity to allow for future expansion to other social media platforms like Twitter and WhatsApp.

---

## 🛠️ Technologies Used

* **Python**: The core programming language.
* **Selenium**: For browser automation and interaction with web elements.
* **CustomTkinter**: For creating modern and responsive graphical user interfaces.
* **MySQL Connector**: To interact with the MySQL database for data storage.
* **WebDriver Manager**: Simplifies the management and installation of browser drivers (e.g., ChromeDriver).
* **python-dotenv**: For loading environment variables securely (e.g., database credentials).

---

## 🚀 Getting Started

### Prerequisites

Before running the application, ensure you have the following installed:

* **Python 3.x**: Download from [python.org](https://www.python.org/downloads/).
* **Google Chrome**: The Selenium WebDriver is configured for Chrome.
* **MySQL Server**: A running MySQL instance to store data.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url> # Replace <repository_url> with your repository's URL
    cd <repository_name>       # Replace <repository_name> with your project's directory name
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install the required Python packages**:
    ```bash
    pip install mysql-connector-python selenium customtkinter webdriver-manager python-dotenv
    ```
    *(Alternatively, if you have a `requirements.txt` file from `pip freeze > requirements.txt`, you can use `pip install -r requirements.txt`)*

4.  **Set up environment variables** (Optional but recommended for sensitive data):
    Create a `.env` file in the root directory of your project and add any sensitive information.

    ```dotenv
    # Example (if you move database credentials here from the script)
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=root
    DB_NAME=thescanners24
    ```

5.  **Set up the MySQL Database**:
    Create a database named `thescanners24` and the necessary tables.

    ```sql
    CREATE DATABASE IF NOT EXISTS thescanners24;

    USE thescanners24;

    CREATE TABLE IF NOT EXISTS credentials (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL,
        Last_Access_Date DATE,
        Last_Access_Time TIME
    );

    CREATE TABLE IF NOT EXISTS url (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        links_visited TEXT,
        Date DATE,
        Time TIME,
        Platform VARCHAR(50),
        Posts VARCHAR(3) DEFAULT 'No',
        DM VARCHAR(3) DEFAULT 'No',
        Following VARCHAR(3) DEFAULT 'No',
        Followers VARCHAR(3) DEFAULT 'No',
        FOREIGN KEY (username) REFERENCES credentials(username)
    );
    ```

---

## 🏃‍♀️ Usage

1.  **Run the application**:
    ```bash
    python your_script_name.py # Replace 'your_script_name.py' with the actual name of your Python file (e.g., `main.py` or `app.py`)
    ```

2.  **Interact with the GUI**:
    * A main window will appear with "Start" and "Exit" buttons.
    * Click "Start" to begin.
    * Select "Instagram" from the platform selection dialog.
    * Enter your Instagram **username** and **password** in the pop-up prompts.
    * The tool will attempt to log in to Instagram.
    * After successful login, a "Gather Evidence" dialog will appear, allowing you to choose what type of data to collect (Posts, Following, Followers, or Messages).
    * For "Messages", you'll be prompted to enter the username of the chat you wish to open.
    * Screenshots will be saved to `C:\Users\aeros\OneDrive\Documents\SIH\Instagram\<USERNAME>\` under respective folders (e.g., `Posts`, `following`, `followers`, `DM`).
    * After collecting evidence, you'll be asked if you want to continue gathering more evidence.

---
## 🚧 Future Enhancements

* **Error Handling Improvements**: More robust error handling for network issues and unexpected website changes.
* **Configurable Paths**: Allow users to configure screenshot save paths through the GUI or a configuration file.
* **Multi-threading**: Implement multi-threading for background tasks to keep the UI responsive during long operations.
* **More Social Media Platforms**: Expand support to Twitter, WhatsApp, Facebook, etc.
* **Detailed Logging**: Implement a more comprehensive logging system for better debugging and monitoring.
* **Headless Mode Option**: Add an option to run Selenium in headless mode for background execution without a visible browser.
* **User Account Management**: Potentially add features to manage multiple social media accounts.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and send pull requests.

---
