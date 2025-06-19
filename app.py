# === app.py ===
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av
from gesture_detection import detect_hand_sign
from adb_control import *

st.set_page_config(page_title="Gesture-Controlled Android Device", layout="centered")

# Streamlit UI app selection
app_options = ["None", "WhatsApp", "YouTube", "Chrome", "Camera", "Settings"]
selected_app = st.selectbox("📱 Select an App to Launch with Gesture", app_options)

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.gesture = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        gesture, annotated_image = detect_hand_sign(img)

        # Debounce gesture detection
        if gesture and gesture != self.gesture:
            self.gesture = gesture
            sync_mobile_ui(gesture, selected_app)

        return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")

st.title("🤖 Full Gesture-Controlled Android System")

webrtc_streamer(
    key="gesture",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={
        "video": {"width": 640, "height": 480},
        "audio": False
    },
    async_processing=True,
)

st.markdown("""
### Supported Gestures:
- ✊ `FIST`: Unlock Device (stays at home screen)
- ✌️ `TWO_FINGERS`: Lock Device
- 👍 `THUMBS_UP`: Launch Selected App
- 🤟 `THREE_FINGERS`: Open YouTube
- ✋ `PALM`: Scroll Down
- 👉 `SWIPE_RIGHT`: Navigate Right
- 👈 `SWIPE_LEFT`: Navigate Left
- 👆 `OK_SIGN`: Go Home
- 🤏 `VICTORY`: Open Notification Panel
""")