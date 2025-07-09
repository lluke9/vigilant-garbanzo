import cv2
import numpy as np
import argparse
from typing import List


def detect_rallies(video_path: str, motion_thresh: float = 25.0, min_motion_frames: int = 15,
                   min_rally_length: float = 2.0) -> List[tuple]:
    """Detect rally segments based on frame-to-frame motion.

    Args:
        video_path: Path to the input video file.
        motion_thresh: Pixel intensity difference threshold for motion detection.
        min_motion_frames: Consecutive frames with motion required to consider rally start.
        min_rally_length: Minimum length of a rally segment in seconds.

    Returns:
        List of (start, end) times for each rally in seconds.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Unable to open {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    ret, prev = cap.read()
    if not ret:
        cap.release()
        return []

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    motion_counter = 0
    rally_started = False
    start_time = 0.0
    segments = []
    frame_idx = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        motion = np.mean(diff)

        if motion > motion_thresh:
            motion_counter += 1
            if not rally_started and motion_counter >= min_motion_frames:
                rally_started = True
                start_time = (frame_idx - motion_counter) / fps
        else:
            if rally_started and motion_counter >= min_motion_frames:
                end_time = frame_idx / fps
                if end_time - start_time >= min_rally_length:
                    segments.append((start_time, end_time))
            rally_started = False
            motion_counter = 0

        prev_gray = gray
        frame_idx += 1

    # Close cap and check final rally
    if rally_started and motion_counter >= min_motion_frames:
        end_time = frame_idx / fps
        if end_time - start_time >= min_rally_length:
            segments.append((start_time, end_time))

    cap.release()
    return segments


def export_segments(video_path: str, segments: List[tuple], output_prefix: str = "rally"):
    """Export rally segments using ffmpeg."""
    import subprocess
    for idx, (start, end) in enumerate(segments):
        output_file = f"{output_prefix}_{idx:03d}.mp4"
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            str(start),
            "-to",
            str(end),
            "-i",
            video_path,
            "-c",
            "copy",
            output_file,
        ]
        subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Trim badminton video to rally segments")
    parser.add_argument("video", help="Input video path")
    parser.add_argument("--export", action="store_true", help="Export rally clips with ffmpeg")
    parser.add_argument("--motion_thresh", type=float, default=25.0, help="Threshold for frame motion")
    parser.add_argument("--min_motion_frames", type=int, default=15, help="Consecutive motion frames to mark rally")
    parser.add_argument("--min_rally_length", type=float, default=2.0, help="Minimum rally duration in seconds")
    args = parser.parse_args()

    segments = detect_rallies(
        args.video,
        motion_thresh=args.motion_thresh,
        min_motion_frames=args.min_motion_frames,
        min_rally_length=args.min_rally_length,
    )

    for s, e in segments:
        print(f"Rally: {s:.2f} - {e:.2f} seconds")

    if args.export:
        export_segments(args.video, segments)


if __name__ == "__main__":
    main()
