# Badminton Rally Trimmer

This example script (`trim_rally.py`) detects active rallies in a badminton match
video and outputs the start/end times of each rally. Optionally it can export
individual rally clips using `ffmpeg`.

You can also experiment with a basic Streamlit interface (`streamlit_app.py`)
that exposes manual trimming and rally detection from the browser.

## Requirements

- Python 3
- OpenCV (`cv2`)
- `ffmpeg` installed and available in `PATH`

## Usage

```bash
python trim_rally.py input.mp4 --export
```

This prints the detected rally segments and creates `rally_###.mp4` files with
only the active rally portions.

Adjust detection parameters with `--motion_thresh`, `--min_motion_frames` and
`--min_rally_length` if needed.

## Streamlit UI

To launch the experimental Streamlit interface run:

```bash
streamlit run streamlit_app.py
```

The UI currently supports manual trimming and auto rally detection. Annotation,
slow motion and voiceover features are marked as TODOs in the app. Additional
plans include overlaying player skeletons with pose detection and tracking the
shuttlecock to generate 4D data for analysis.
