# Face Attendance System

This project implements a Face Attendance System using facial recognition and Firebase Realtime Database. It allows students to mark their attendance by detecting their faces through a webcam and ensures accurate records by storing data in Firebase.

## Features

- **Firebase Integration:** Stores student details and attendance records in a Firebase Realtime Database.
- **Face Encoding:** Generates and saves facial encodings for student images to enable fast and accurate recognition.
- **Real-time Attendance:** Uses a webcam to detect and identify students in real time. Marks attendance only once per day for each student.
- **Custom Interface:** Displays attendance status, student information, and an overlayed camera feed on a background image.

## Installation

### Clone the Repository
```bash
git clone <repository-url>
cd Faceattendance
```

### Dependencies
Create a `requirements.txt` file with the following dependencies:
```
firebase-admin
face_recognition
opencv-python
numpy
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### Set Up Firebase
1. Set up a Firebase Realtime Database in your Firebase project.
2. Download the Firebase Admin SDK key (`.json` file) from the Firebase console.
3. Place the downloaded `.json` file in the root directory of the project.

### Prepare Student Data
1. Create a folder named `Images` in the project directory.
2. Add student images to the folder with filenames matching their IDs (e.g., `12345.jpg`).
3. Add student details to the Firebase database by running:
   ```bash
   python adddatatodatabasefile.py
   ```
4. Generate facial encodings for student images:
   ```bash
   python encodegenerator.py
   ```

### Run the System
Start the face recognition-based attendance system:
```bash
python main.py
```
