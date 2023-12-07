import streamlit as st
import os
import cv2
import supervision as sv
from ultralytics import YOLO
from time import sleep
from tqdm.notebook import tqdm
from tqdm.notebook import tqdm
import numpy as np
from PIL import Image
import tempfile
import gdown
import glob
from PIL import Image
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
# constants
MODEL_NAME = 'yolov8n.pt' 
HOME = os.getcwd()
MODEL_DEFAULT_PATH = os.path.join(HOME, 'models', MODEL_NAME)
VIDEO_PATHS = {
    'source': os.path.join(HOME, 'data/raw', 'conveyor_test.mp4'),
    'target': os.path.join(HOME, 'data/processed', 'temp_output_video.mp4')
}

# flags
user_video_upload = True


# ------------------------ Helper Functions---------------------------------

# Helper function to download model from Google Drive
def download_from_gdrive(gdrive_url, output_path):
    gdown.download(gdrive_url, output_path, quiet=False, fuzzy=True)


# Helper function to load model, with caching for 60 minutes
@st.cache_resource(ttl=60*60) 
def load_model(path):
    return YOLO(path)

# Helper function to remove all mp4 files in a directory except  conveyor_test.mp4 to clean up the space
def remove_mp4_except_conveyor_test(directory):
    for filepath in glob.glob(f"{directory}/*.mp4"):
        if filepath != f"{directory}/conveyor_test.mp4":
            os.remove(filepath)

# ------------------------ Streamlit App Description ---------------------------------

st.set_page_config(
    page_title="E.S.R.A",
    page_icon="🤖",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yash-chaudhary/E.S.R.A',
        'About': 'Demo app for YOLOV8 Object Counting'
    }
)

st.header("""E.S.R.A (Enhanced Sensory Recognition w/ AI)""", divider='rainbow')

st.markdown('''This demonstration aims to showcase the utility of computer vision as a means of instantaneously demonstrating OFS-X software by
                removing the hurdles of Puppy installation and connectivity and providing access to richer data contexts.'''
)

st.markdown("### How to Use")

st.markdown('1️⃣ Define your detection specifications (min confidence threshold and object selection')
st.markdown('2️⃣ Point your devices camera to the manufacturing line you want to begin counting.')
st.markdown('3️⃣ Whenever you\'re ready, hit the start button to begin the real-time video stream')
st.markdown('4️⃣ Analyse the operation and performance of the computer vision model')

def main():
    # ------------------------pre-loading---------------------------------

    # Downloading default source video from Google Drive if it doesn't exist
    if not os.path.exists(VIDEO_PATHS['source']):
        download_from_gdrive('https://drive.google.com/file/d/1U_6VpkMDYdbT_kkwlEFryaxPnkfEUTV1/view?usp=sharing', VIDEO_PATHS['source'])
    

    # Initialize YOLO model
    placeholder = st.empty()
    if os.path.exists(MODEL_DEFAULT_PATH):
        model = load_model(MODEL_DEFAULT_PATH)
    else:
        placeholder.info('Model does not exist, downloading and this may take a while', icon="ℹ️")
        model = load_model(MODEL_NAME)
        os.rename(MODEL_NAME, MODEL_DEFAULT_PATH)
    placeholder.success('The model is loaded successfully')
    sleep(1)
    placeholder.empty()

    # Remove *.mp4 in data/raw/ except  conveyor_test.mp4
    remove_mp4_except_conveyor_test("data/raw")

    # Remove *.mp4 in data/processed/
    remove_mp4_except_conveyor_test("data/processed")

    # ------------------------ Streamlit Sidebar ---------------------------------
    #Show mode size info in sidebar
    st.sidebar.markdown(f"Model Type: {MODEL_NAME[:-3]}")
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space

    option = st.sidebar.radio(
    "Select Video Source",
    ["Via video upload", "Via device camera"],
    captions = ["Allows you to upload a .mp4", "Allows you to stream from device camera"])
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space

    if option == 'Via video upload':
        user_video_upload = True
    elif option == 'Via device camera':
        user_video_upload = False

    
    # Video File Uploader and use a temp file to store the uploaded file and delete it after the process automatically
    if user_video_upload:
        uploaded_file = st.sidebar.file_uploader("Upload a video file", type=["mp4"])
        if uploaded_file is not None:
            with open("data/raw/temp_input_video.mp4", "wb") as f:
                f.write(uploaded_file.read())
            VIDEO_PATHS['source'] = "data/raw/temp_input_video.mp4"
            # Adding space between sidebar items
            st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space

    else:
        # Render WebRTC streamer component
        class VideoProcessor:
            def recv(self, frame):
                img = frame.to_ndarray(format="bgr24")

                return av.VideoFrame.from_ndarray(img, format="bgr24")

        webrtc_streamer(
            key="object-detection",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessor,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )

    #Confidence threshold
    confidence_threshold = st.sidebar.slider("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space

    # Select desired detection classes
    class_names_dict = model.model.names
    selected_class_names = st.sidebar.multiselect("Select Desired Classes", list(class_names_dict.values()), ['cup'])
    selected_class_ids = [k for k, v in class_names_dict.items() if v in selected_class_names]


    # Show video info
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space
    st.sidebar.markdown(f"Source Video Information:")
    video_info = sv.VideoInfo.from_video_path(VIDEO_PATHS['source'])
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.write(f"Width:\n{video_info.width}")
    with col2:
        st.write(f"Height:\n{video_info.height}")
    with col3:
        st.write(f"Frames:\n{video_info.total_frames}")


    # Point Configuration
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space
    with st.sidebar.expander("⚙️ Line Points Configuration: ", expanded=True):
        LINE_START = tuple(map(int, st.text_input("Starting Point (x,y)", "250,1500").split(',')))
        LINE_END = tuple(map(int, st.text_input("Ending Point (x,y)", "1000,1350").split(',')))

    if user_video_upload:
        # Check x from either LINE_START or LINE_END should be smaller than  video_information.width otherwise raise error
        if LINE_START[0] > video_info.width or LINE_END[0] > video_info.width:
            st.error('x from either LINE_START or LINE_END should be smaller or equal to video width')
            st.stop()
        # Check y from either LINE_START or LINE_END should be smaller than  video_information.height otherwise raise error
        if LINE_START[1] > video_info.height or LINE_END[1] > video_info.height:
            st.error('y from either LINE_START or LINE_END should be smaller or equal to  video height')
            st.stop()

    # Box annotator
    # st.sidebar.markdown(f"Box Annotator Configuration:")
    with st.sidebar.expander("⚙️ Box Annotator Configuration: ", expanded=False):
        box_annotator_thickness = st.number_input("Box Thickness", min_value=1, value=1)
        box_annotator_text_thickness = st.number_input("Box Text Thickness", min_value=1, value=1)
        box_annotator_text_scale = st.number_input("Box Text Scale", min_value=0.1, max_value=1.0, value=0.5)


    # Line counter annotator
    # st.sidebar.markdown(f"Line Counter Annotator Configuration:")
    with st.sidebar.expander("⚙️ Line Annotator Configuration: ", expanded=False):
        line_thickness = st.number_input("Line Thickness", min_value=1, value=1)
        line_text_thickness = st.number_input("Line Text Thickness", min_value=1, value=1)
        line_text_scale = st.number_input("Line Text Scale", min_value=0.1, max_value=1.0, value=0.5)


    # ------------------------ Video Processing---------------------------------

    # Initialize Streamlit placeholder
    frame_placeholder = st.empty()

    def callback(frame: np.ndarray, index:int) -> np.ndarray:
        # model prediction on single frame and conversion to supervision Detections
        results = model(frame, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        # only consider class id from selected_classes define above
        detections = detections[np.isin(detections.class_id, selected_class_ids)]
        detections = detections[detections.confidence > confidence_threshold]
        # tracking detections
        detections = byte_tracker.update_with_detections(detections)
        labels = [
            f"#{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, tracker_id
            in detections
        ]
        box_annotated_frame=box_annotator.annotate(scene=frame.copy(),
                                        detections=detections,
                                        labels=labels)
        # update line counter
        line_zone.trigger(detections)
        line_counter_annotated_frame = line_zone_annotator.annotate(box_annotated_frame, line_counter=line_zone)
        # # display frame
        # image_pil = Image.fromarray(cv2.cvtColor(line_counter_annotated_frame, cv2.COLOR_BGR2RGB))
        # frame_placeholder.image(image_pil, use_column_width=True)

        _, buffer = cv2.imencode('.jpg', line_counter_annotated_frame)
        frame_as_bytes = buffer.tobytes()
        frame_placeholder.image(frame_as_bytes, channels="BGR", use_column_width=True, output_format="auto")
        return  line_counter_annotated_frame
    

    # Video display
    LINE_START = sv.Point(*LINE_START)
    LINE_END = sv.Point(*LINE_END)

    # create BYTETracker instance
    byte_tracker = sv.ByteTrack(track_thresh= 0.25, track_buffer = 30,match_thresh = 0.8,frame_rate =30)

    # create frame generator
    generator = sv.get_video_frames_generator(VIDEO_PATHS['source'])

    # create LineZone instance, it is previously called LineCounter class
    line_zone = sv.LineZone(start=LINE_START, end=LINE_END)

    # create instance of BoxAnnotator
    box_annotator = sv.BoxAnnotator(thickness=box_annotator_thickness, text_thickness=box_annotator_text_thickness, text_scale=box_annotator_text_scale)

    # create LineZoneAnnotator instance, it is previously called LineCounterAnnotator class
    line_zone_annotator = sv.LineZoneAnnotator(thickness=line_thickness, text_thickness=line_text_thickness, text_scale=line_text_scale)

    # process the whole video
    sv.process_video(
        source_path = VIDEO_PATHS['source'],
        target_path = VIDEO_PATHS['target'],
        callback=callback
    )

if __name__ == "__main__":
    # call main function
    main()



# Start the WebRTC streamer
    # ctx = webrtc_streamer(
    #     key="object-detection",
    #     mode=WebRtcMode.SENDRECV,
    #     media_stream_constraints={"video": True, "audio": False},
    #     video_processor_factory=ObjectDetector,
    #     async_processing=True
    # )


    # Initialize Streamlit placeholder
    # frame_placeholder = st.empty()

    # # Define the WebRTC video transformer
    # class ObjectDetector(VideoTransformerBase):
    #     def recv(self, frame):

    #         # video display
    #         LINE_START = sv.Point(*LINE_START)
    #         LINE_END = sv.Point(*LINE_END)

    #         # create BYTETracker instance
    #         byte_tracker = sv.ByteTrack(track_thresh= 0.25, track_buffer = 30,match_thresh = 0.8,frame_rate =30)

    #         # create LineZone instance, it is previously called LineCounter class
    #         line_zone = sv.LineZone(start=LINE_START, end=LINE_END)

    #         # create instance of BoxAnnotator
    #         box_annotator = sv.BoxAnnotator(thickness=box_annotator_thickness, text_thickness=box_annotator_text_thickness, text_scale=box_annotator_text_scale)

    #         # create LineZoneAnnotator instance, it is previously called LineCounterAnnotator class
    #         line_zone_annotator = sv.LineZoneAnnotator(thickness=line_thickness, text_thickness=line_text_thickness, text_scale=line_text_scale)

    #         frame = frame.to_ndarray(format="bgr24")

    #         results = model(frame, verbose=False)[0]    # able to return a list of frame but we only index 0 as we are passing one frame

    #         detections = sv.Detections.from_ultralytics(results)

    #         # only consider class id from selected_classes define above
    #         detections = detections[np.isin(detections.class_id, selected_class_ids)]
    #         detections = detections[detections.confidence > confidence_threshold]

    #         # tracking detections
    #         detections = byte_tracker.update_with_detections(detections)

    #         labels = [
    #             f"#{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
    #             for _, _, confidence, class_id, tracker_id
    #             in detections
    #         ]
    #         box_annotated_frame=box_annotator.annotate(scene=frame.copy(),
    #                                         detections=detections,
    #                                         labels=labels)
    #         # update line counter
    #         line_zone.trigger(detections)
    #         line_counter_annotated_frame = line_zone_annotator.annotate(box_annotated_frame, line_counter=line_zone)
    #         _, buffer = cv2.imencode('.jpg', line_counter_annotated_frame)
    #         frame_as_bytes = buffer.tobytes()
    #         frame_placeholder.image(frame_as_bytes, channels="BGR", use_column_width=True, output_format="auto")
    #         return  line_counter_annotated_





