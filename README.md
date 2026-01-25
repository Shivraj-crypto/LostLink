# LostLink

## Overview

LostLink is a Kivy/KivyMD desktop app that helps match a missing person’s photo against a stored database using face recognition. It supports scanning from the camera, selecting an image from disk, and displaying matched profile details pulled from a Google Cloud Storage bucket.

## Key Features

- Face recognition against a stored image database
- Camera scan and gallery upload workflows
- Auto-cropping of detected faces for review
- Profile info display for matched records
- Upload flow to add new missing-person entries

## Project Structure

```
LostLink/
├── .github/
├── Camera Roll/
├── Images/
├── buildozer.spec
├── capstone-project-5cd4a-firebase-adminsdk-rcagk-2dafde0ec0 (1).json
├── haarcascade_frontalface_default.xml
├── main.py
└── My.kv
```

## Requirements

- Python 3.x
- Kivy
- KivyMD
- OpenCV
- face_recognition
- NumPy
- Google Cloud Storage client

Install dependencies:

```bash
pip install kivy kivymd opencv-python face_recognition numpy google-cloud-storage google-auth
```

## Setup

### 1. Google Cloud credentials

This app uses a service account JSON file for Google Cloud Storage. Update the path in `main.py` if you move or rename it:

```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "capstone-project-5cd4a-firebase-adminsdk-rcagk-2dafde0ec0 (1).json"
```

### 2. Storage bucket

Ensure your bucket name matches the code:

```python
bucket = client.get_bucket('capstone-project-5cd4a.appspot.com')
```

### 3. Local assets

Keep the `Camera Roll/` and `Images/` folders in place since the UI references those assets directly in `My.kv`.

## Run the App

```bash
python main.py
```

## How It Works

- **Face scan**: captures an image from the webcam and compares it to images in `Camera Roll/database` (synced from the cloud bucket).
- **Gallery match**: lets a user select a file and tries to match it against the same database.
- **Match result**: if a match is found, the app displays the matched image and the corresponding `.txt` info from `Camera Roll/information`.
- **No match**: if no match is found, the app shows the “not found” flow.
- **Add new record**: the “Add image of a missing person” flow copies the selected image, collects details, and uploads both the image and a text file to the cloud bucket.

## Notes and Limitations

- `face_recognition` depends on dlib and may require platform-specific build tools.
- Webcam access is required for the scan flow.
- The JSON credentials file is currently in the repo; avoid committing real credentials for public use.
- Paths in the UI reference `Camera Roll` and `Images` directories with exact names.

## Disclaimer

This project is intended for educational and demonstration purposes only.
