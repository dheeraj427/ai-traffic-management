import streamlit as st
import cv2
from util.image_processor import preparing_image
from util.dynamic_signal_switching import switch_signal

st.set_page_config(page_title="AI Traffic Management", layout="wide")

st.title("🚦 Intelligent Traffic Management using YOLO")

uploaded_files = st.file_uploader(
    "Upload lane images",
    type=["jpg","jpeg","png"],
    accept_multiple_files=True
)

vehicle_counts = {}

if uploaded_files:

    for i, uploaded_file in enumerate(uploaded_files):

        file_bytes = uploaded_file.read()

        image_path = f"lane_{i+1}.jpg"

        with open(image_path,"wb") as f:
            f.write(file_bytes)

        image = cv2.imread(image_path)

        vehicles = preparing_image(image)

        vehicle_counts[f"Lane {i+1}"] = vehicles

        st.image(image, caption=f"Lane {i+1} - Vehicles detected: {vehicles}")

    st.subheader("Vehicle Count Per Lane")

    st.write(vehicle_counts)

    green_lane = switch_signal(vehicle_counts)

    st.success(f"🚦 Lane with denser traffic: {green_lane}")

    recommended_time = vehicle_counts[green_lane] * 3

    st.info(f"🕒 Recommended signal switch time based on density: {recommended_time} seconds")

    st.markdown("---")

    st.subheader(f"OPENING {green_lane.upper()}:")

    lanes = ["Lane 1","Lane 2","Lane 3","Lane 4"]

    cols = st.columns(4)

    for idx, lane in enumerate(lanes):

        with cols[idx]:

            st.write(lane)

            if lane == green_lane:
                st.write("🔴")
                st.write("⚪")
                st.write("🟢")
            else:
                st.write("🔴")
                st.write("⚪")
                st.write("⚪")

    st.markdown("---")

    st.write(f"{green_lane.upper()} OPENED !")

    st.write("Calculating Signal Open-Close Timing...")

    st.error(f"{green_lane.upper()} will CLOSE after {recommended_time} seconds .................")

    st.markdown("---")

    st.write(f"CLOSING {green_lane.upper()}")