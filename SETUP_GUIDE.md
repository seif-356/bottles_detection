# Bottle Detection App - Setup Guide

## Overview
- **Backend**: Flask + YOLOv8 (Python)
- **Frontend**: Flutter
- **Flow**: Video upload → Detection → Tracking → Score

---

## Backend Setup (Python)

### 1. Install dependencies
```bash
pip install flask ultralytics opencv-python numpy
```

### 2. Run backend
```bash
python bottle_detection_backend.py
```

The backend will start on `http://localhost:5000`

**Important**: YOLOv8 will auto-download on first run (~100MB)

---

## Flutter Setup

### 1. Create new Flutter project
```bash
flutter create bottle_detection_app
cd bottle_detection_app
```

### 2. Update `pubspec.yaml`
Add these dependencies:
```yaml
dependencies:
  flutter:
    sdk: flutter
  video_player: ^2.7.0
  image_picker: ^0.9.0
  http: ^1.1.0
  dio: ^5.3.0
```

Run:
```bash
flutter pub get
```

### 3. Replace `lib/main.dart` with the Flutter code provided

### 4. Update backend URL
In the Flutter code, find:
```dart
'http://YOUR_BACKEND_URL:5000/process_video',
```

Replace with:
- **Local testing**: `http://10.0.2.2:5000` (Android emulator)
- **Real device**: `http://YOUR_MACHINE_IP:5000`
- **Production**: Your deployed backend URL

### 5. Android Permissions
Edit `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

### 6. iOS Permissions
Edit `ios/Runner/Info.plist`:
```xml
<key>NSPhotoLibraryUsageDescription</key>
<string>We need access to your video library</string>
<key>NSCameraUsageDescription</key>
<string>We need camera access</string>
```

### 7. Run app
```bash
flutter run
```

---

## How It Works

### Input
User selects a video showing:
- Car being controlled by remote
- 3-6 bottles on ground
- Car hitting bottles one by one

### Processing
1. Video uploaded to backend
2. YOLOv8 detects all bottles (COCO class 39)
3. Tracker monitors each bottle's position
4. When bottle disappears from frame → marked as "fallen"
5. Order of falls recorded
6. Annotated video generated with:
   - Green boxes around detected bottles
   - Hit sequence displayed on video

### Output
```json
{
  "score": 5,
  "fall_sequence": [1, 3, 2],
  "total_bottles_detected": 3
}
```

Score = number of bottles successfully knocked down

---

## Troubleshooting

### "Connection refused" error
- Make sure backend is running
- Check backend URL in Flutter code
- Use correct IP (not localhost on actual device)

### YOLOv8 detection misses bottles
- Bottles must be visible in frame
- Good lighting helps
- Model detects "bottle" class - if your bottles look unusual, detection may be poor
- Can adjust confidence threshold in backend (`confidence_threshold=0.5`)

### Video processing takes forever
- Processing time = video length × inference time
- 30-second video on CPU: ~2-5 minutes
- Use smaller video or shorter clips for testing
- Consider running on GPU if available

### Flutter app crashes on upload
- Check internet permissions (see Android/iOS setup)
- Verify backend URL is correct
- Check video file size (shouldn't be >500MB)

---

## Deployment Options

### Option A: Local Network
- Backend: Run on your computer
- Flutter: Run on phone connected to same WiFi
- Update URL to your computer's IP

### Option B: Cloud Deployment
1. Deploy backend to Heroku/AWS/Google Cloud
2. Update Flutter URL to cloud backend
3. Handle video storage (backend currently doesn't persist videos)

### Option C: On-Device Processing (Advanced)
- Run TFLite YOLOv8 model directly on phone
- Requires model conversion: `yolov8n.pt` → `.tflite`
- Use `tflite_flutter` package
- Much faster, no server needed

---

## Performance Notes

**Current bottleneck**: Video processing on CPU
- YOLOv8 inference: ~500ms per frame on modern CPU
- 900 frames (30 sec @ 30fps) = ~7-8 minutes

**To optimize:**
- Use `yolov8n.pt` (nano) - already in code
- Could use `yolov8s.pt` for accuracy vs speed tradeoff
- GPU deployment would reduce to ~30 seconds

---

## Next Steps After Getting It Working

1. **Test with real video**: Drive car, hit bottles, record
2. **Adjust confidence**: Change `confidence_threshold` if detection is poor
3. **Fine-tune tracking**: Adjust distance threshold in `BottleTracker.update()`
4. **Add video saving**: Store processed video on device or cloud
5. **Improve UI**: Add progress bar, show detection confidence, etc.

---

## Questions?

If detection isn't working on your bottles:
1. Check if bottles are detected at all (adjust confidence lower)
2. Video must be clear and well-lit
3. Bottles must be fully visible in frame
4. Model is trained on standard bottles - unusual shapes may not work

The simple solution if detection fails: Switch to color-based detection (mark bottles with colored tape) - would be much more reliable but requires manual marking.
