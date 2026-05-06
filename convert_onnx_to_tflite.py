"""
Direct ONNX → TFLite conversion using onnx2tf.
Requires: yolov8n.onnx already present in the same directory.
"""
import os
import shutil
import onnx2tf

ONNX_PATH = "yolov8n.onnx"
SAVED_MODEL_DIR = "yolov8n_saved_model"
OUTPUT_TFLITE = "assets/models/yolov8n_float32.tflite"

print(f"Converting {ONNX_PATH} to TFLite ...")

onnx2tf.convert(
    input_onnx_file_path=ONNX_PATH,
    output_folder_path=SAVED_MODEL_DIR,
    not_use_onnxsim=False,
)

# onnx2tf writes the tflite file inside the saved_model folder
candidates = [
    os.path.join(SAVED_MODEL_DIR, f)
    for f in os.listdir(SAVED_MODEL_DIR)
    if f.endswith("_float32.tflite") or f.endswith(".tflite")
]

if not candidates:
    raise FileNotFoundError(f"No .tflite file found in {SAVED_MODEL_DIR}")

src = sorted(candidates)[0]
os.makedirs("assets/models", exist_ok=True)
shutil.copy(src, OUTPUT_TFLITE)
size_mb = os.path.getsize(OUTPUT_TFLITE) / 1_048_576
print(f"Done. Saved to {OUTPUT_TFLITE}  ({size_mb:.1f} MB)")
