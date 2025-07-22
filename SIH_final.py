import mysql.connector
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from datetime import datetime
import customtkinter as ctk
from tkinter import Canvas

# Load environment variables
load_dotenv()

# Selenium WebDriver setup
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

def draw_gradient(canvas, width, height, color1, color2):
    """Draw a vertical gradient from color1 to color2."""
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr // 256:02x}{ng // 256:02x}{nb // 256:02x}'
        canvas.create_line(0, i, width, i, fill=color)

def screenshot(driver, url, save_path, obj, USERNAME):
    driver.get(url)
    save_url(USERNAME, url, obj)  # Save the URL to the database
    i = 1
    time.sleep(10)
    try:  # Handle the "Turn on Notifications" pop-up
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click()
    except:
        time.sleep(5)
    if obj == "followers":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'followers'))).click()
    elif obj == "following":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'following'))).click()
    elif obj == 'DM':
        try:
            time.sleep(5)
            username_to_search = ask_string("Open DM", "Enter the username: ")
            driver.find_element(By.XPATH, f"//*[contains(text(), '{username_to_search}')]").click()
            time.sleep(5)
            show_info("Scanners24", "DM chat opened successfully")
        except:
            show_warning("Scanners24", "DM chat failed to open")

    while True:
        if obj == "followers":
            pop_up_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
            time.sleep(10)
            while True:
                save_loc = os.path.join(save_path, f'followers_{USERNAME}_screenshot_{i}.png')
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up_window)
                driver.save_screenshot(save_loc)
                time.sleep(5)
                if i>10:
                    break
                i+=1
        elif obj == "following":
            pop_up_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
            time.sleep(10)
            while True:
                save_loc = os.path.join(save_path, f'following_{USERNAME}_screenshot_{i}.png')
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up_window)
                driver.save_screenshot(save_loc)
                time.sleep(5)
                if i>10:
                    break
                i+=1
        elif obj == "DM":
            scroll_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='x78zum5 xdt5ytf x1iyjqo2 xs83m0k x1xzczws x6ikm8r x1rife3k x1n2onr6 xh8yej3 x16o0dkt' and @style='--card-background: rgb(var(--ig-primary-background)); --comment-background: rgb(var(--ig-highlight-background)); --messenger-card-background: rgb(var(--ig-primary-background)); --mwp-message-list-actions-width: calc(84px + 3*0px); --mwp-message-row-background: var(--messenger-card-background); --primary-text: rgb(var(--ig-primary-text)); --chat-composer-button-color: #0084ff; --chat-composer-input-background-color: var(--comment-background); --chat-edit-message-overlay-color: var(--surface-background); --chat-outgoing-message-background-gradient: initial; --chat-outgoing-message-bubble-background-color: #0084ff; --mwp-header-button-color: #0084ff; --mwp-message-list-actions-gap: 0px; --mwp-primary-theme-color: #0084ff; --reaction-pill-background-color: var(--wash); --reaction-pill-multireact-selected-color: #c7e4ff;']")))
            time.sleep(10)
            while True:
                save_loc = os.path.join(save_path, f'DM_{username_to_search}_{USERNAME}_screenshot{i}.png')
                driver.save_screenshot(save_loc)
                driver.execute_script("arguments[0].scrollTop -= 100;", scroll_window)
                time.sleep(5)
                if i>10:
                    break
                i+=1
        elif obj == "posts":
            save_loc = os.path.join(save_path, f'posts_{USERNAME}_screenshot{i}.png')
        driver.save_screenshot(save_loc)
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        driver.save_screenshot(save_loc)
        if new_height == last_height:
            break
    show_info("Scanners24", "Screenshot saved successfully")

# Function to insert URL visited into the database
def save_url(username, url, evidence):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        if evidence=="posts":
            query = "INSERT INTO url (username, links_visited, Date, Time, Platform, Posts) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, url, datetime.now().date(), datetime.now().time(), "Instagram", "Yes"))
        elif evidence=="DM":
            query = "INSERT INTO url (username, links_visited, Date, Time, Platform, DM) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, url, datetime.now().date(), datetime.now().time(), "Instagram", "Yes"))
        elif evidence=="following":
            query = "INSERT INTO url (username, links_visited, Date, Time, Platform,  Following) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, url, datetime.now().date(), datetime.now().time(),"Instagram", "Yes"))
        elif evidence=="followers":
            query = "INSERT INTO url (username, links_visited, Date, Time, Platform, Followers) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, url, datetime.now().date(), datetime.now().time(),"Instagram", "Yes"))
        
        connection.commit()
        cursor.close()
        connection.close()
        show_info("Database", f"URL saved successfully for {username}.")
    except mysql.connector.Error as err:
        show_warning("Database Error", f"Failed to save URL: {err}")

def connect_db():
    try:
        connection=mysql.connector.connect(
            host="localhost",       
            user="root",        
            password="root",
            database="thescanners24"   
        )
        return connection
    except mysql.connector.Error as err:
        show_warning("Database Error", f"Error connecting to MySQL: {err}")
        sys.exit(1)

def save_credentials(username, password):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        # Use 'INSERT ... ON DUPLICATE KEY UPDATE' to update the password if the username exists
        query = """
        INSERT INTO credentials (username, password, Last_Access_Date, Last_Access_Time)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        password = VALUES(password), 
        Last_Access_Date = CURDATE(), 
        Last_Access_Time = CURTIME(); """

        cursor.execute(query, (username, password, datetime.now().date(), datetime.now().time()))
        connection.commit()
        cursor.close()
        connection.close()
        show_info("Database", "Credentials saved successfully.")
    except mysql.connector.Error as err:
        show_warning("Database Error", f"Failed to save credentials: {err}")


def gather_evidence(USERNAME, insta_url):
    def gather_post():
        url1 = insta_url + USERNAME + "/"
        screenshot_dir = f'C:\\Users\\aeros\\OneDrive\\Documents\\SIH\\Instagram\\{USERNAME}\\Posts'
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot(driver, url1, screenshot_dir, "posts", USERNAME)
    
    def gather_following():
        url2 = insta_url + USERNAME + "/following/"
        screenshot_dir = f'C:\\Users\\aeros\\OneDrive\\Documents\\SIH\\Instagram\\{USERNAME}\\following'
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot(driver, url2, screenshot_dir, "following", USERNAME)
    
    def gather_followers():
        url3 = insta_url + USERNAME + "/followers/"
        screenshot_dir = f'C:\\Users\\aeros\\OneDrive\\Documents\\SIH\\Instagram\\{USERNAME}\\followers'
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot(driver, url3, screenshot_dir, "followers", USERNAME)
    
    def gather_dm():
        url4 = insta_url + "direct/inbox/"
        screenshot_dir = f'C:\\Users\\aeros\\OneDrive\\Documents\\SIH\\Instagram\\{USERNAME}\\DM'
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot(driver, url4, screenshot_dir, "DM", USERNAME)
    evidence_dialog = ctk.CTkToplevel()
    evidence_dialog.title("Gather Evidence")

    label = ctk.CTkLabel(evidence_dialog, text="Select evidence type to gather:")
    label.pack(padx=20, pady=10)
    
    # Add buttons for each option
    post_button = ctk.CTkButton(evidence_dialog, text="Posts", command=lambda: [evidence_dialog.destroy(), gather_post()])
    post_button.pack(pady=10)

    following_button = ctk.CTkButton(evidence_dialog, text="Following", command=lambda: [evidence_dialog.destroy(), gather_following()])
    following_button.pack(pady=10)

    followers_button = ctk.CTkButton(evidence_dialog, text="Followers", command=lambda: [evidence_dialog.destroy(), gather_followers()])
    followers_button.pack(pady=10)

    dm_button = ctk.CTkButton(evidence_dialog, text="Messages", command=lambda: [evidence_dialog.destroy(), gather_dm()])
    dm_button.pack(pady=10)
    # Show the dialog and wait for user input
    evidence_dialog.transient(root)
    evidence_dialog.grab_set()
    root.wait_window(evidence_dialog)

    cont = ctk.CTkToplevel()
    cont.title("Tool")
    label = ctk.CTkLabel(cont, text="Do you want to continue?")
    label.pack(padx=20, pady=10)
    Yes_button = ctk.CTkButton(cont, text="Yes", command=lambda: [cont.destroy(), gather_evidence(USERNAME, insta_url)])
    Yes_button.pack(pady=10)
    No_button = ctk.CTkButton(cont, text="No", command=lambda: [cont.destroy()])
    No_button.pack(pady=10)
    cont.transient(root)
    cont.grab_set()
    root.wait_window(cont)

# Main application
def start():
    # Function to open Instagram and take screenshots
    def open_instagram():
        USERNAME = ask_string("Username", "Enter the username:")
        PASSWORD = ask_string("Password", "Enter password:")

        insta_url = 'https://www.instagram.com/'
        driver.get(insta_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(USERNAME)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(PASSWORD)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))).click()
        time.sleep(10)

        try:
            saveinfo_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/section/div/button')
            ))
            saveinfo_button.click()
        except:
            pass

        show_info("Login", "Logged in successfully")

        # Save credentials to MySQL database
        save_credentials(USERNAME, PASSWORD)
        gather_evidence(USERNAME, insta_url)

    def open_twitter():
        show_info("Twitter", "Twitter option selected.")
        # Add Twitter handling logic here

    def open_whatsapp():
        show_info("WhatsApp", "WhatsApp option selected.")
        # Add WhatsApp handling logic here
    dialog = ctk.CTkToplevel()
    dialog.title("Select Platform")

    label = ctk.CTkLabel(dialog, text="Select Platform:")
    label.pack(padx=20, pady=10)

    instagram_button = ctk.CTkButton(dialog, text="Instagram", command=lambda: [dialog.destroy(),open_instagram()])
    instagram_button.pack(pady=10)

    twitter_button = ctk.CTkButton(dialog, text="Twitter", command=lambda: [dialog.destroy(), open_twitter()])
    twitter_button.pack(pady=10)

    whatsapp_button = ctk.CTkButton(dialog, text="WhatsApp", command=lambda: [dialog.destroy(), open_whatsapp()])
    whatsapp_button.pack(pady=10)

    dialog.update_idletasks()  # Ensure the dialog is drawn and sized correctly

    # Center the dialog on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)


def show_info(title, message):
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    label = ctk.CTkLabel(dialog, text=message, wraplength=300)
    label.pack(padx=20, pady=20)
    ok_button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
    ok_button.pack(pady=(0, 20))
    dialog.update_idletasks()  # Ensure the dialog is drawn and sized correctly

    # Center the dialog on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

def show_warning(title, message):
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    label = ctk.CTkLabel(dialog, text=message, wraplength=300)
    label.pack(padx=20, pady=20)
    ok_button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
    ok_button.pack(pady=(0, 20))
    dialog.update_idletasks()  # Ensure the dialog is drawn and sized correctly

    # Center the dialog on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

# Custom input dialogs using CustomTkinter
def ask_string(title, prompt):
    def on_submit():
        nonlocal input_value
        input_value = entry.get()
        dialog.destroy()

    input_value = None
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    label = ctk.CTkLabel(dialog, text=prompt)
    label.pack(padx=20, pady=10)
    entry = ctk.CTkEntry(dialog)
    entry.pack(padx=20, pady=10)
    submit_button = ctk.CTkButton(dialog, text="Submit", command=on_submit)
    submit_button.pack(pady=(0, 20))
    entry.bind("<Return>", on_submit)
    dialog.update_idletasks()  # Ensure the dialog is drawn and sized correctly
    
    # Center the dialog on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)
    return input_value

root = ctk.CTk()
root.title("Scanners24")
root.geometry("600x400")
def on_resize(event):
    # Get the new window width and height
    width = event.width
    height = event.height

    # Clear the previous gradient and redraw it with the new dimensions
    canvas.delete("all")
    draw_gradient(canvas, width, height, "#89CFF0", "#00008B")

# Create a canvas to draw the gradient background
canvas = Canvas(root, highlightthickness=0)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

# Bind the resizing event of the window to adjust the canvas size dynamically
canvas.bind("<Configure>", on_resize)

# Draw the initial gradient background
draw_gradient(canvas, 600, 400, "#89CFF0", "#00008B")  # Light blue to dark blue gradient

# Create a canvas to draw the gradient background
canvas = Canvas(root, width=600, height=400, highlightthickness=0)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

# Draw a gradient from light blue to dark blue
draw_gradient(canvas, 600, 400, "#89CFF0", "#00008B")  # Light blue to dark blue gradient

# Add your widgets on top of the gradient background
start_button = ctk.CTkButton(root, text="Start", command=start)
start_button.pack(pady=20)

exit_button = ctk.CTkButton(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)
root.mainloop()
driver.quit()


