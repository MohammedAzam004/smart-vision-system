# app.py
import streamlit as st
import cv2
import numpy as np
import time
from threading import Event

st.set_page_config(
    page_title="AI Vision Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #2c3e50, #4ca1af);
        color: white;
    }
    
    .title-text {
        font-size: 3rem !important;
        font-weight: bold;
        color: #f1c40f;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .css-1d391kg {
        background-color: rgba(0, 0, 0, 0.2);
    }
    
    .stRadio > label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ecf0f1;
    }

    .stButton > button {
        background-color: #f1c40f;
        color: #2c3e50;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #f39c12;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

CLOAK_COLORS = {
    'Red': {
        'lower1': np.array([0, 120, 70]),
        'upper1': np.array([10, 255, 255]),
        'lower2': np.array([170, 120, 70]),
        'upper2': np.array([180, 255, 255]),
        'has_two_ranges': True,
        'emoji': '🔴'
    },
    'Blue': {
        'lower1': np.array([100, 150, 50]),
        'upper1': np.array([140, 255, 255]),
        'has_two_ranges': False,
        'emoji': '🔵'
    },
    'Green': {
        'lower1': np.array([40, 50, 50]),
        'upper1': np.array([80, 255, 255]),
        'has_two_ranges': False,
        'emoji': '🟢'
    },
    'Yellow': {
        'lower1': np.array([20, 100, 100]),
        'upper1': np.array([30, 255, 255]),
        'has_two_ranges': False,
        'emoji': '🟡'
    },
    'Black': {
        'lower1': np.array([0, 0, 0]),
        'upper1': np.array([180, 255, 50]),
        'has_two_ranges': False,
        'emoji': '⚫'
    }
}

def run_face_detection(frame):
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 165, 0), 3)
        cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)
    return frame

def run_face_eye_smile_detection(frame):
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('models/haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('models/haarcascade_smile.xml')
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 22)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sh+sy), (0, 0, 255), 2)
            
    return frame

def run_number_plate_detection(frame):
    plate_cascade = cv2.CascadeClassifier('models/haarcascade_russian_plate_number.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    for (x, y, w, h) in plates:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, "Number Plate", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

def run_invisibility_cloak(stop_event, placeholder, selected_color_name='Red'):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Cannot open camera.")
        return

    time.sleep(2)
    color_settings = CLOAK_COLORS[selected_color_name]
    
    st.info("Capturing background for Invisibility Cloak... Please step out of frame for a moment.")
    background_frame = None
    for i in range(30):
        ret, bg = cap.read()
        if ret:
            background_frame = np.flip(bg, axis=1)
    st.success(f"Background captured! You can now use the {selected_color_name} cloak.")

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video.")
            break
            
        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv, color_settings['lower1'], color_settings['upper1'])
        
        if color_settings['has_two_ranges']:
            mask2 = cv2.inRange(hsv, color_settings['lower2'], color_settings['upper2'])
            mask = mask1 + mask2
        else:
            mask = mask1
        
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)
        
        mask_inv = cv2.bitwise_not(mask)
        
        res1 = cv2.bitwise_and(background_frame, background_frame, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        final_output_bgr = cv2.addWeighted(res1, 1, res2, 1, 0)
        final_output_rgb = cv2.cvtColor(final_output_bgr, cv2.COLOR_BGR2RGB)
        placeholder.image(final_output_rgb, use_container_width=True)

    cap.release()

st.markdown("<h1 class='title-text'>AI Vision Hub 📸</h1>", unsafe_allow_html=True)
st.sidebar.title("Project Selection")
app_mode = st.sidebar.radio(
    "Choose a Project",
    ["Home", "Face Detection", "Face, Eye & Smile Detection", "Number Plate Detection", "Invisibility Cloak"]
)

if app_mode == "Home":
    st.header("Welcome to the AI Vision Hub!")
    st.write("""
        This is a collection of Computer Vision projects built with OpenCV and Streamlit.
        Select a project from the sidebar to get started. 
        Each project uses your webcam to demonstrate real-time image processing. Enjoy!
    """)
    st.image("https://i.imgur.com/k4QYj0m.gif", caption="AI in Action", use_container_width=True)

elif app_mode == "Invisibility Cloak":
    st.header("The Invisibility Cloak 🧙‍♂️")
    st.write("Select a color and use a matching cloth to become invisible! Make sure your background is set before you start.")
    
    st.subheader("🎨 Select Cloak Color")
    color_options = [f"{CLOAK_COLORS[color]['emoji']} {color}" for color in CLOAK_COLORS.keys()]
    selected_color_display = st.selectbox(
        "Choose the color of your invisibility cloak:",
        color_options,
        index=0
    )
    
    selected_color = selected_color_display.split(' ', 1)[1]
    
    st.info(f"✨ You selected: **{selected_color}** cloak. Use a {selected_color.lower()} colored cloth for best results!")
    
    col1, col2 = st.columns(2)
    with col1:
        start_button = st.button('🚀 Start Cloak', key='invisibility_start_cloak')
    with col2:
        stop_button = st.button('⏹️ Stop Cloak', key='invisibility_stop_cloak')
    
    if 'cloak_running' not in st.session_state:
        st.session_state.cloak_running = False
    if 'stop_event' not in st.session_state:
        st.session_state.stop_event = Event()

    image_placeholder = st.empty()
    
    if start_button:
        st.session_state.cloak_running = True
        st.session_state.stop_event.clear()
        run_invisibility_cloak(st.session_state.stop_event, image_placeholder, selected_color)
        
    if stop_button:
        st.session_state.cloak_running = False
        st.session_state.stop_event.set()
        st.info("Invisibility Cloak has been stopped.")
        image_placeholder.empty()

else:
    st.header(f"{app_mode} in Real-Time")
    st.write("Click 'Start Camera' to begin the detection.")

    start_cam = st.button('Start Camera')
    stop_cam = st.button('Stop Camera')
    
    if 'stop' not in st.session_state:
        st.session_state.stop = True
    
    if start_cam:
        st.session_state.stop = False
    if stop_cam:
        st.session_state.stop = True

    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)

    while not st.session_state.stop:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image from camera.")
            st.session_state.stop = True
            break
        
        if app_mode == "Face Detection":
            output_frame_bgr = run_face_detection(frame)
        elif app_mode == "Face, Eye & Smile Detection":
            output_frame_bgr = run_face_eye_smile_detection(frame)
        elif app_mode == "Number Plate Detection":
            output_frame_bgr = run_number_plate_detection(frame)
        else:
            output_frame_bgr = frame
        
        output_frame_rgb = cv2.cvtColor(output_frame_bgr, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(output_frame_rgb)
        
    else:
        cap.release()
        st.info("Camera is off.")