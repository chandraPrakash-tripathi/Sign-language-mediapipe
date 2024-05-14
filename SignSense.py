import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from styles import page_setup, hide_navbar, unhide_nav_bar
import json
import sqlite3


# Database connection
def get_db_connection():
    return sqlite3.connect("signsense.db")


# Initialize database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Profile (
                        username TEXT PRIMARY KEY,
                        name TEXT,
                        email_id TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Alphabet (
                        username TEXT,
                        letter TEXT,
                        PRIMARY KEY (username, letter),
                        FOREIGN KEY(username) REFERENCES Profile(username)
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Words (
                        username TEXT,
                        word TEXT,
                        PRIMARY KEY (username, word),
                        FOREIGN KEY(username) REFERENCES Profile(username)
                    )''')
    conn.commit()
    conn.close()


init_db()

st.markdown(page_setup(), unsafe_allow_html=True)
st.markdown(hide_navbar(), unsafe_allow_html=True)


def get_username(self):
    if st.session_state['LOGOUT_BUTTON_HIT'] == False:
        fetched_cookies = self.cookies
        if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
            username = fetched_cookies['__streamlit_login_signup_ui_username__']
            return username


def get_name(self):
    with open("_secret_auth_.json", "r") as auth:
        user_data = json.load(auth)
        current_user = get_username(self)
        for user in user_data:
            if user["username"] == current_user:
                return user["name"]


def get_email(self):
    with open("_secret_auth_.json", "r") as auth:
        user_data = json.load(auth)
        current_user = get_username(self)
        for user in user_data:
            if user["username"] == current_user:
                return user["email"]


def add_profile_to_database(user_info):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Profile (username, name, email_id)
                VALUES (?, ?, ?)""",
            (user_info["username"], user_info["name"], user_info["email"]),
        )
        conn.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if conn:
            conn.close()


login_obj = __login__(
    auth_token="courier_auth_token",
    company_name="SignSense",
    width=200,
    height=250,
    logout_button_name="Logout",
    hide_menu_bool=True,
    hide_footer_bool=True,
    lottie_url="https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json",
)

logged_in = login_obj.build_login_ui()

if logged_in:

    current_user = {
        "username": get_username(login_obj),
        "name": get_name(login_obj),
        "email": get_email(login_obj),
        "id": None,
    }

    if "current_user" not in st.session_state:
        st.session_state["current_user"] = current_user
    else:
        st.session_state["current_user"] = current_user

    add_profile_to_database(current_user)

    st.markdown(unhide_nav_bar(), unsafe_allow_html=True)
    # Display other content
    # st.write("# Welcome to SignSense! 👋")
    st.write("<h1 style='font-size: 55px; color: #fff;'>Welcome to SignSense! 👋</h1>", unsafe_allow_html=True)

    # Other content...
    # st.markdown(
    #     """
    # <div class="section">
    #     <a class="link" href="About_Us">About</a> |
    #     <a class="link" href="#features">Features</a> |
    #     <a class="link" href="#contact">Contact</a>
    # </div>
    #
    # <div class="section">
    #     <h2 class="header">Master Sign Language Effortlessly</h2>
    #     <p>SignSense is an innovative web application designed for individuals who are mute or communicate primarily through sign language. Similar to popular language learning platforms like DuoLingo, SignSense aims to provide an interactive and engaging way for users to learn and practice sign language.</p>
    #
    # </div>
    #
    # <div class="section">
    #     <h2 class="header">About SignSense</h2>
    #     <p>SignSense is revolutionizing the way we learn and practice sign language. Powered by cutting-edge technology, SignSense utilizes OpenCV for image processing and MediaPipe action detection, ensuring an accurate and seamless learning experience.</p>
    # </div>
    #
    # <div class="section">
    #     <h2 class="header">Features</h2>
    #     <ul>
    #         <li>Interactive lessons</li>
    #         <li>Real-time feedback</li>
    #         <li>Engaging practice sessions</li>
    #         <li>Progress tracking</li>
    #     </ul>
    # </div>
    #
    # <div class="section">
    #     <h2 class="header">Contact Us</h2>
    #     <p>Have questions or feedback? We'd love to hear from you!</p>
    # </div>
    # """,
    #     unsafe_allow_html=True,
    # )
    st.markdown(
        """
        <style>
            body {
                color: #fff; /* White text color */
                background-color: #000; /* Black background */
            }
            .section {
                margin: 10px;
                padding: 20px;
                border-radius: 10px;
                background: #333; /* Dark grey background for the sections */
                box-shadow: 0 4px 8px rgba(255,255,255,0.1); /* Subtle white shadow for depth */
            }
            .header {
                color: #00BFFF; 
                font-family: 'Arial', sans-serif;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            ul li:before {
                content: "•";
                color: #00BFFF; 
                font-weight: bold;
                display: inline-block;
                width: 1em;
                margin-left: -1em;
            }
            ul li {
                margin-bottom: 5px;
                color: #fff; /* Khaki color for list text to be soft yet readable on dark backgrounds */
            }
        </style>

        <div class="section">
            <h2 class="header">Master Sign Language Effortlessly</h2>
            <p>SignSense is an innovative web application designed for individuals who are mute or communicate primarily through sign language. Similar to popular language learning platforms like DuoLingo, SignSense aims to provide an interactive and engaging way for users to learn and practice sign language.</p>
        </div>

        <div class="section">
            <h2 class="header">About SignSense</h2>
            <p>SignSense is revolutionizing the way we learn and practice sign language. Powered by cutting-edge technology, SignSense utilizes OpenCV for image processing and MediaPipe action detection, ensuring an accurate and seamless learning experience.</p>
        </div>

        <div class="section">
            <h2 class="header">Features</h2>
            <ul>
                <li>Interactive lessons</li>
                <li>Real-time feedback</li>
                <li>Engaging practice sessions</li>
                <li>Progress tracking</li>
            </ul>
        </div>

        <div class="section">
            <h2 class="header">Contact Us</h2>
            <p>Have questions or feedback? We'd love to hear from you!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
