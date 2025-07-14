import streamlit as st
from pathlib import Path
from tempfile import NamedTemporaryFile
from trim_rally import detect_rallies, export_segments


def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary location and return path."""
    with NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def main():
    st.title("Badminton Rally Trimmer")

    uploaded_video = st.file_uploader("Upload Match Video", type=["mp4", "mov", "avi"])
    if uploaded_video:
        video_path = save_uploaded_file(uploaded_video)
        st.video(video_path)

        st.header("Manual Trim")
        col1, col2 = st.columns(2)
        with col1:
            start = st.number_input("Start time (seconds)", min_value=0.0, value=0.0, step=0.1)
        with col2:
            end = st.number_input("End time (seconds)", min_value=0.0, value=0.0, step=0.1)

        if st.button("Export Manual Trim"):
            export_segments(video_path, [(start, end)], output_prefix="manual_trim")
            st.success("Segment exported as manual_trim_000.mp4")

        st.header("Auto Detect Rallies")
        if st.button("Suggest Trim-Out Segments"):
            segments = detect_rallies(video_path)
            if segments:
                st.write("Detected rally segments:")
                for idx, (s, e) in enumerate(segments):
                    st.write(f"Rally {idx+1}: {s:.2f}s - {e:.2f}s")
                st.session_state['segments'] = segments
            else:
                st.info("No rallies detected")

        segments = st.session_state.get('segments')
        if segments:
            if st.button("Trim Non-Rally Sections"):
                # Convert rally segments to keep to segments to remove
                non_rally = []
                last_end = 0.0
                video_duration = None

                import cv2
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    fps = cap.get(cv2.CAP_PROP_FPS) or 30
                    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    video_duration = total_frames / fps
                cap.release()

                for start_s, end_s in segments:
                    if start_s > last_end:
                        non_rally.append((last_end, start_s))
                    last_end = end_s
                if video_duration and last_end < video_duration:
                    non_rally.append((last_end, video_duration))

                if non_rally:
                    export_segments(video_path, non_rally, output_prefix="trimmed")
                    st.success("Non-rally segments exported as trimmed_###.mp4")
                else:
                    st.info("No sections to trim")

        st.header("Annotations")
        st.write("TODO: implement drawing and text annotations on video")

        st.header("Slow Motion")
        st.write("TODO: allow selecting segments to play/export in slow-mo")

        st.header("Voiceover Commentary")
        st.write("TODO: record audio commentary and mix with video")

        st.header("Pose Detection & Shuttlecock Tracking")
        st.write("TODO: overlay player skeletons and track shuttlecock for 4D analytics")


if __name__ == "__main__":
    main()
