"""
Railway Track Inspection System - FastAPI Backend
YOLOv5 Inference API
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import cv2
import numpy as np
from PIL import Image
import io
from typing import List, Dict
import os
import sys
import pathlib
from contextlib import asynccontextmanager

# Fix for PosixPath error on Windows
if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath

app = FastAPI(title="Railway Track Inspection API", version="1.0.0")

# CORS middleware untuk akses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv5 model
MODEL_PATH = "../models/best.pt"
model = None
model_error = None

# Kelas deteksi (WAJIB sesuai dataset)
CLASS_NAMES = [
    'fishplate',
    'fishplate_bolthead',
    'fishplate_boltmissing',
    'fishplate_boltnut',
    'track_bolt',
    'track_boltmissing',
    'track_crack'
]

# Severity mapping
HIGH_RISK_CLASSES = ['track_crack', 'fishplate_boltmissing', 'track_boltmissing']
MEDIUM_RISK_CLASSES = ['fishplate', 'track_bolt']
LOW_RISK_CLASSES = ['fishplate_bolthead', 'fishplate_boltnut']

def load_model():
    """Load YOLOv5 model with Windows compatibility"""
    global model, model_error
    if model is None and model_error is None:
        try:
            print("[*] Loading model...")
            
            # Try to load custom trained model first
            if os.path.exists(MODEL_PATH):
                print(f"[*] Loading custom trained model from: {MODEL_PATH}")
                try:
                    model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                          path=MODEL_PATH, force_reload=False, trust_repo=True, verbose=False)
                    print("[+] Custom trained model loaded successfully")
                except Exception as e1:
                    print(f"[!] Custom model load failed: {e1}")
                    print("[*] Falling back to YOLOv5s pretrained...")
                    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', 
                                          force_reload=False, trust_repo=True, verbose=False)
                    print("[+] Pretrained YOLOv5s loaded successfully")
            else:
                print(f"[!] Custom model not found at {MODEL_PATH}")
                print("[*] Loading YOLOv5s pretrained model...")
                model = torch.hub.load('ultralytics/yolov5', 'yolov5s', 
                                      force_reload=False, trust_repo=True, verbose=False)
                print("[+] Pretrained model loaded successfully")
            
            if model is not None:
                model.conf = 0.25  # Confidence threshold
                model.iou = 0.45   # NMS IOU threshold
                print("[+] Model configured: conf=0.25, iou=0.45")
            
        except Exception as e:
            model_error = str(e)
            print(f"[-] Error loading model: {e}")
            import traceback
            traceback.print_exc()
    
    return model




@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Railway Track Inspection API",
        "model": "YOLOv5",
        "classes": len(CLASS_NAMES)
    }

@app.post("/detect")
async def detect_faults(file: UploadFile = File(...)):
    """
    Detect railway track faults from uploaded image
    
    Returns:
        JSON with detections, severity analysis, and inspection status
    """
    global model
    
    try:
        # Load model if not loaded yet
        if model is None:
            model = load_model()
        
        if model is None:
            raise HTTPException(status_code=503, detail="Model tidak siap. Coba lagi dalam beberapa saat.")
        
        # Validasi file
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File harus berupa gambar")
        
        # Baca image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Convert RGB jika perlu
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        # Inference
        results = model(img_array)
        
        # Parse results
        detections = []
        class_counts = {name: 0 for name in CLASS_NAMES}
        high_risk_count = 0
        
        # results is a Detections object, xyxy is a list of tensors (one per image)
        if hasattr(results, 'xyxy') and len(results.xyxy) > 0:
            # results.xyxy[0] contains detections for first image
            pred_boxes = results.xyxy[0]
            
            # Iterate through each detection
            for detection in pred_boxes:
                if len(detection) >= 6:  # x1, y1, x2, y2, conf, cls
                    x1, y1, x2, y2, conf, cls = detection[:6]
                    class_id = int(cls)
                    confidence = float(conf)
                    bbox = [float(x1), float(y1), float(x2), float(y2)]
                    
                    if class_id < len(CLASS_NAMES):
                        class_name = CLASS_NAMES[class_id]
                        
                        # Determine severity
                        if class_name in HIGH_RISK_CLASSES:
                            severity = "HIGH"
                            color = "#ef4444"  # red
                            high_risk_count += 1
                        elif class_name in MEDIUM_RISK_CLASSES:
                            severity = "MEDIUM"
                            color = "#f59e0b"  # orange
                        else:
                            severity = "LOW"
                            color = "#10b981"  # green
                        
                        detection_obj = {
                            "class": class_name,
                            "class_id": class_id,
                            "confidence": round(confidence, 3),
                            "bbox": bbox,
                            "severity": severity,
                            "color": color
                        }
                        
                        detections.append(detection_obj)
                        class_counts[class_name] += 1
        
        # Determine inspection status
        if high_risk_count > 0:
            status = "BAHAYA"
            status_icon = "🚨"
            status_color = "#dc2626"
        elif len(detections) > 5:
            status = "PERLU PERBAIKAN"
            status_icon = "⚠️"
            status_color = "#f59e0b"
        else:
            status = "AMAN"
            status_icon = "✅"
            status_color = "#10b981"
        
        # Statistics
        total_detections = len(detections)
        critical_percentage = (high_risk_count / total_detections * 100) if total_detections > 0 else 0
        
        response = {
            "success": True,
            "total_detections": total_detections,
            "detections": detections,
            "class_counts": class_counts,
            "statistics": {
                "high_risk": high_risk_count,
                "medium_risk": sum(1 for d in detections if d["severity"] == "MEDIUM"),
                "low_risk": sum(1 for d in detections if d["severity"] == "LOW"),
                "critical_percentage": round(critical_percentage, 1)
            },
            "inspection_status": {
                "status": status,
                "icon": status_icon,
                "color": status_color
            },
            "image_size": {
                "width": img_array.shape[1],
                "height": img_array.shape[0]
            }
        }
        
        return JSONResponse(content=response)
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Detection error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error saat deteksi: {str(e)}")

@app.post("/detect-batch")
async def detect_batch(files: List[UploadFile] = File(...)):
    """Batch detection untuk multiple images"""
    results = []
    
    for file in files:
        try:
            result = await detect_faults(file)
            results.append({
                "filename": file.filename,
                "result": result
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse(content={"results": results})

@app.get("/classes")
async def get_classes():
    """Get all detection classes"""
    return {
        "classes": CLASS_NAMES,
        "total": len(CLASS_NAMES),
        "high_risk": HIGH_RISK_CLASSES,
        "medium_risk": MEDIUM_RISK_CLASSES,
        "low_risk": LOW_RISK_CLASSES
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)