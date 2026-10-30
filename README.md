# Face Recognition & Facial Expression Analysis

A Python desktop application that captures face images from a webcam, trains a face recognizer, identifies registered people in a live camera feed, and displays a predicted facial expression alongside their saved profile details.

Built with **OpenCV**, **DeepFace**, **Tkinter**, and **SQLite**.

> **Important:** The expression label is a prediction based on visible facial features, not a reliable measure of a person's internal emotional state.

## Features

- **Face registration:** Enter a numeric user ID, name, and age in a Tkinter interface.
- **Face image capture:** Detect faces with a Haar Cascade and save 100 preprocessed grayscale images per capture session.
- **Model training:** Train an OpenCV Local Binary Patterns Histograms (LBPH) face recognizer using saved images.
- **Live recognition:** Identify registered faces using the webcam and display their saved name and age.
- **Facial-expression analysis:** Use DeepFace to display a predicted expression, such as `happy`, `neutral`, or `sad`.
- **Local storage:** Store user profiles in SQLite and the trained LBPH model on disk.

## Tech stack

| Component | Technology |
| --- | --- |
| Language | Python 3.12 |
| Desktop interface | Tkinter |
| Camera capture and face detection | OpenCV, Haar Cascade |
| Face recognition | OpenCV LBPH recognizer (`opencv-contrib-python`) |
| Facial-expression analysis | DeepFace |
| Model inference runtime | ONNX Runtime (with the tested DeepFace installation) |
| User profiles | SQLite |
| Numerical operations | NumPy |

## Project structure

```text
face-recognition-mood/
├── main_gui.py                         # Tkinter interface and actions
├── capture_faces.py                    # Capture and preprocess face images
├── train_model.py                      # Train and save the LBPH recognizer
├── recognize_faces.py                  # Live recognition and expression analysis
├── database.py                         # Create/update SQLite user profiles
├── database.db                         # SQLite database (tracked in current repo)
├── haarcascade_frontalface_default.xml # Haar Cascade face detector
├── requirements.txt                    # Python dependencies (add this to Git)
├── .gitignore
├── dataset/                            # Generated face images (Git-ignored)
└── recognizer/                         # Generated trainingdata.yml (Git-ignored)
```

`dataset/` and `recognizer/` are generated locally and are not included in the repository. The application expects to be run from the project root because it uses relative file paths.

## Getting started (macOS / Apple Silicon)

The project was tested with **Python 3.12.16** on macOS. You will need a working webcam (USB webcam or compatible iPhone Continuity Camera).

### 1. Clone the repository

```bash
git clone https://github.com/ribhupramanik/face-recognition-mood.git
cd face-recognition-mood
```

### 2. Install Python and Tkinter

If using Homebrew Python 3.12:

```bash
brew install python@3.12 python-tk@3.12
python3.12 -m tkinter
```

The second command should open a small Tkinter test window. Close it before continuing.

### 3. Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install --upgrade pip
```

### 4. Install Python dependencies

**OpenCV compatibility note:** The app needs the GUI-enabled `opencv-contrib-python` package for `cv2.imshow()` and `cv2.face.LBPHFaceRecognizer_create()`. DeepFace 0.0.103 declares the overlapping headless OpenCV distribution as a dependency. The tested setup intentionally avoids installing both distributions together.

After committing a `requirements.txt` generated from the verified working environment with `python -m pip freeze > requirements.txt`, install the full frozen package set without resolving the conflicting OpenCV dependency again:

```bash
python -m pip install --no-deps -r requirements.txt
```

This approach is specific to the fully frozen, tested environment and is **not** a general-purpose installation pattern. Installations on other platforms or Python versions may require adjustments. `pip check` may flag DeepFace's declared headless OpenCV dependency even when the GUI-enabled contrib distribution works at runtime.

Verify the important imports:

```bash
python -c "import tkinter, cv2; from deepface import DeepFace; print('OpenCV:', cv2.__version__); print('LBPH:', hasattr(cv2.face, 'LBPHFaceRecognizer_create')); print('DeepFace import OK')"
```

The LBPH check should print `True`.

### 5. Create the dataset directory and launch

```bash
mkdir -p dataset
python main_gui.py
```

## How to use

1. **Register a user:** Enter a numeric **User ID**, **Name**, and **Age** in the GUI.
2. **Capture Face:** Click **Capture Face** and look toward the webcam in good lighting. The app detects faces and collects 100 grayscale samples, resized to 200 × 200 pixels and contrast-normalized.
3. **Train Model:** After successful capture, click **Train Model**. The app creates `recognizer/trainingdata.yml`.
4. **Recognize Face:** Click **Recognize Face** to start live face recognition. For recognized profiles, the app displays name, age, and a predicted facial-expression label.
5. **Exit recognition:** Focus the OpenCV camera window and press **Q**.

Capture images before training: an empty `dataset/` directory causes the LBPH training step to fail.

On first use, DeepFace may download pretrained model weights into `~/.deepface/weights/`. Internet access may be required for that initial download.

## How it works

**Registration and capture:** `main_gui.py` calls `capture_faces.py`, which creates or updates the user's SQLite profile and reads webcam frames. The Haar Cascade detects faces; each sample is converted to grayscale, resized, and histogram-equalized before being saved to `dataset/`.

**Training:** `train_model.py` loads the saved face images, extracts user IDs from filenames, trains an LBPH recognizer, and saves its learned data as `recognizer/trainingdata.yml`.

**Recognition:** `recognize_faces.py` detects faces in each webcam frame, uses the LBPH recognizer to predict a registered user ID, and looks up that person's details in `database.db`. It also calls `DeepFace.analyze(..., actions=['emotion'])` for a predicted facial-expression label. The existing code uses an LBPH distance threshold of `60` to decide whether to show a known profile.

The two prediction systems serve different purposes: **LBPH recognizes identity**, while **DeepFace predicts facial expressions**. DeepFace is not used to train the project's identity recognizer.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `No module named '_tkinter'` | Install `python-tk@3.12` when using Homebrew Python 3.12. |
| `No module named 'cv2'` | Activate `.venv` and install the project dependencies. |
| `cv2.face` is missing | Use `opencv-contrib-python`, not the standard or headless-only OpenCV distribution. |
| Camera fails / `!_src.empty()` | Check webcam connection, macOS **Privacy & Security → Camera** permissions, and whether OpenCV can read camera index `0`. |
| `Empty training data was given` | Capture face images first and verify that `dataset/` contains image files. |
| `recognizer/trainingdata.yml` not found | Run **Train Model** after capturing samples. |
| Expression shows `Unknown` | The app catches errors from DeepFace. Inspect the terminal and test the emotion model separately. |
| Slow first recognition run | DeepFace may need to download or initialize pretrained weights. |

To test camera access independently:

```bash
python -c "import cv2; cap=cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION); print('Camera opened:', cap.isOpened()); ok, frame=cap.read() if cap.isOpened() else (False, None); print('Frame captured:', ok); cap.release()"
```

Both values should be `True`. On systems other than macOS, a different camera backend may be needed.

## Current limitations

- Camera index `0` is hard-coded; systems with multiple cameras may need configuration.
- Camera-read failures and empty training datasets are not gracefully handled in the current GUI.
- The identity recognizer relies on LBPH rather than a modern embedding-based recognition system.
- The emotion-analysis call runs during live recognition and can affect frame rate.
- SQLite stores registered user details locally; there is no user-authentication or multi-user access-control layer.
- Recognition and facial-expression predictions can be inaccurate under poor lighting, motion, occlusion, or unfamiliar conditions.

## Privacy

Face images and identity records are personal data. Only capture people who have agreed to participate; restrict access to the local files and do not publish face images, trained data, or real user records. The repository already tracks `database.db`, so check it for personal information before pushing further changes. The `.gitignore` excludes generated `dataset/` and `recognizer/` folders but does not untrack files already committed.

## Future improvements

- Add camera initialization and frame-read error handling.
- Show clear messages when no training images or model file are available.
- Allow camera selection and a way to stop image capture early.
- Improve model testing and measure recognition accuracy and latency.
- Separate model errors from an actual `Unknown` expression result.
- Add automated tests and a demo video or screenshots using consented sample data.

## Acknowledgments

Uses [OpenCV](https://opencv.org/), [DeepFace](https://github.com/serengil/deepface), and the Python standard library's Tkinter and SQLite interfaces.
