# Badminton Rally Trimmer

This example script (`trim_rally.py`) detects active rallies in a badminton match
video and outputs the start/end times of each rally. Optionally it can export
individual rally clips using `ffmpeg`.

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
