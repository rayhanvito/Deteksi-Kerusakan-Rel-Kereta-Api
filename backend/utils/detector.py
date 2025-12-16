"""
Detection Utilities for Railway Track Inspection
Helper functions untuk YOLOv5 detection & visualization
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict
import torch

class RailwayDetector:
    """YOLOv5 Railway Track Fault Detector"""
    
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
    HIGH_RISK = ['track_crack', 'fishplate_boltmissing', 'track_boltmissing']
    MEDIUM_RISK = ['fishplate', 'track_bolt']
    LOW_RISK = ['fishplate_bolthead', 'fishplate_boltnut']
    
    # Color mapping (BGR format for OpenCV)
    COLORS = {
        'HIGH': (0, 0, 255),      # Red
        'MEDIUM': (0, 165, 255),  # Orange
        'LOW': (0, 255, 0)        # Green
    }
    
    def __init__(self, model_path: str, conf_threshold: float = 0.25, iou_threshold: float = 0.45):
        """
        Initialize detector
        
        Args:
            model_path: Path ke YOLOv5 model weights
            conf_threshold: Confidence threshold untuk deteksi
            iou_threshold: IOU threshold untuk NMS
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load YOLOv5 model"""
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                       path=self.model_path, force_reload=False)
            self.model.conf = self.conf_threshold
            self.model.iou = self.iou_threshold
            print(f"✅ Model loaded: {self.model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise e
    
    def get_severity(self, class_name: str) -> str:
        """Get severity level dari class name"""
        if class_name in self.HIGH_RISK:
            return 'HIGH'
        elif class_name in self.MEDIUM_RISK:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def detect(self, image: np.ndarray) -> Dict:
        """
        Run detection pada image
        
        Args:
            image: Input image (numpy array, RGB)
        
        Returns:
            Dictionary dengan detection results
        """
        # Run inference
        results = self.model(image)
        
        # Parse results
        detections = []
        class_counts = {name: 0 for name in self.CLASS_NAMES}
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for *box, conf, cls in results.xyxy[0]:
            class_id = int(cls)
            class_name = self.CLASS_NAMES[class_id]
            confidence = float(conf)
            severity = self.get_severity(class_name)
            
            detection = {
                'class': class_name,
                'class_id': class_id,
                'confidence': round(confidence, 3),
                'bbox': [float(b) for b in box],
                'severity': severity
            }
            
            detections.append(detection)
            class_counts[class_name] += 1
            severity_counts[severity] += 1
        
        # Calculate inspection status
        status = self._get_inspection_status(severity_counts)
        
        return {
            'detections': detections,
            'total': len(detections),
            'class_counts': class_counts,
            'severity_counts': severity_counts,
            'status': status,
            'image_shape': image.shape
        }
    
    def _get_inspection_status(self, severity_counts: Dict) -> Dict:
        """Determine inspection status berdasarkan severity"""
        if severity_counts['HIGH'] > 0:
            return {
                'status': 'BAHAYA',
                'icon': '🚨',
                'color': '#dc2626',
                'message': f"Ditemukan {severity_counts['HIGH']} kerusakan kritis!"
            }
        elif severity_counts['MEDIUM'] > 3:
            return {
                'status': 'PERLU PERBAIKAN',
                'icon': '⚠️',
                'color': '#f59e0b',
                'message': 'Beberapa komponen perlu perhatian'
            }
        else:
            return {
                'status': 'AMAN',
                'icon': '✅',
                'color': '#10b981',
                'message': 'Kondisi rel dalam keadaan baik'
            }
    
    def draw_detections(self, image: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """
        Draw bounding boxes & labels pada image
        
        Args:
            image: Input image (numpy array)
            detections: List of detection dictionaries
        
        Returns:
            Image dengan bounding boxes
        """
        img_copy = image.copy()
        
        for det in detections:
            # Get bbox coordinates
            x1, y1, x2, y2 = [int(coord) for coord in det['bbox']]
            
            # Get color berdasarkan severity
            color = self.COLORS[det['severity']]
            
            # Draw bounding box
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), color, 2)
            
            # Prepare label
            label = f"{det['class']} {det['confidence']:.2f}"
            
            # Draw label background
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(img_copy, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), color, -1)
            
            # Draw label text
            cv2.putText(img_copy, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return img_copy
    
    def annotate_image(self, image: np.ndarray, detections: List[Dict], 
                      show_confidence: bool = True) -> np.ndarray:
        """
        Annotate image dengan informasi deteksi lengkap
        
        Args:
            image: Input image
            detections: List of detections
            show_confidence: Tampilkan confidence score
        
        Returns:
            Annotated image
        """
        img_copy = self.draw_detections(image, detections)
        
        # Add summary text di corner
        h, w = img_copy.shape[:2]
        
        # Background untuk text
        cv2.rectangle(img_copy, (10, 10), (250, 100), (0, 0, 0), -1)
        cv2.rectangle(img_copy, (10, 10), (250, 100), (255, 255, 255), 2)
        
        # Text information
        cv2.putText(img_copy, f"Total: {len(detections)}", 
                   (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Count by severity
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for det in detections:
            severity_counts[det['severity']] += 1
        
        y_offset = 60
        for severity, color in self.COLORS.items():
            count = severity_counts[severity]
            cv2.putText(img_copy, f"{severity}: {count}", 
                       (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            y_offset += 20
        
        return img_copy
    
    def save_detection_report(self, image: np.ndarray, detections: List[Dict], 
                             output_path: str):
        """
        Save annotated image dengan detection report
        
        Args:
            image: Input image
            detections: Detection results
            output_path: Path untuk save image
        """
        annotated = self.annotate_image(image, detections)
        cv2.imwrite(output_path, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
        print(f"✅ Report saved: {output_path}")


class VideoDetector:
    """Video detection untuk railway track inspection"""
    
    def __init__(self, detector: RailwayDetector):
        self.detector = detector
    
    def process_video(self, video_path: str, output_path: str, 
                     skip_frames: int = 1):
        """
        Process video dan save hasil deteksi
        
        Args:
            video_path: Path ke input video
            output_path: Path untuk output video
            skip_frames: Process setiap n frames (untuk speed up)
        """
        cap = cv2.VideoCapture(video_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        total_detections = 0
        
        print("🎥 Processing video...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Skip frames untuk speed up
            if frame_count % skip_frames != 0:
                out.write(frame)
                continue
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect
            results = self.detector.detect(rgb_frame)
            detections = results['detections']
            total_detections += len(detections)
            
            # Annotate
            annotated = self.detector.annotate_image(rgb_frame, detections)
            annotated_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
            
            # Write frame
            out.write(annotated_bgr)
            
            if frame_count % 30 == 0:
                print(f"Processed {frame_count} frames, {total_detections} detections")
        
        cap.release()
        out.release()
        
        print(f"✅ Video processed: {output_path}")
        print(f"Total frames: {frame_count}, Total detections: {total_detections}")


# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = RailwayDetector(model_path="models/best.pt")
    
    # Test image detection
    test_image = cv2.imread("test_image.jpg")
    test_image_rgb = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
    
    results = detector.detect(test_image_rgb)
    print(f"Detections: {results['total']}")
    print(f"Status: {results['status']}")
    
    # Save annotated image
    detector.save_detection_report(test_image_rgb, results['detections'], 
                                   "output_detection.jpg")