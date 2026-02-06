# """
# AI Service for Gastric Cancer Classification using ResNet50
# 위암 분류 AI 서비스 (ResNet50 기반)
# """

# import os
# import torch
# import torch.nn as nn
# from torchvision import models, transforms
# from PIL import Image
# import numpy as np
# from pathlib import Path
# from typing import Dict, Tuple
# import time

# from app.core.config import settings


# class GastricCancerAIService:
#     """위암 분류 AI 서비스"""
    
#     # 클래스 레이블
#     CLASS_NAMES = ["STDI", "STNT", "STIN", "STMX"]
#     CLASS_NAMES_KR = {
#         "STDI": "미만형선암",
#         "STNT": "위염",
#         "STIN": "장형선암",
#         "STMX": "혼합형선암"
#     }
    
#     def __init__(self):
#         self.device = torch.device(settings.AI_DEVICE if torch.cuda.is_available() else "cpu")
#         self.model = None
#         self._load_model()
        
#     def _load_model(self):
#         """모델 로드"""
#         try:
#             # 모델 파일 경로 확인
#             if not os.path.exists(settings.AI_MODEL_PATH):
#                 print(f"⚠️  모델 파일 없음: {settings.AI_MODEL_PATH}")
#                 print(f"   현재 경로: {os.getcwd()}")
#                 print(f"   모델 파일을 다음 위치에 배치하세요: {settings.AI_MODEL_PATH}")
#                 return
            
#             # ResNet50 모델 구조 생성
#             self.model = models.resnet50(weights=None)
#             num_ftrs = self.model.fc.in_features
#             self.model.fc = nn.Linear(num_ftrs, len(self.CLASS_NAMES))
            
#             # 체크포인트 로드 (weights_only=False 경고 억제)
#             checkpoint = torch.load(settings.AI_MODEL_PATH, map_location=self.device, weights_only=False)
            
#             # state_dict 추출
#             if isinstance(checkpoint, dict):
#                 if 'model_state_dict' in checkpoint:
#                     state_dict = checkpoint['model_state_dict']
#                 elif 'state_dict' in checkpoint:
#                     state_dict = checkpoint['state_dict']
#                 else:
#                     state_dict = checkpoint
#             else:
#                 state_dict = checkpoint
            
#             # 모델 로드
#             self.model.load_state_dict(state_dict, strict=False)
#             self.model.to(self.device)
#             self.model.eval()
            
#             print(f"✅ AI 모델 로드 성공2: {settings.AI_MODEL_PATH}")
#             print(f"   Device: {self.device}")
            
#         except Exception as e:
#             print(f"❌ 모델 로드 실패: {e}")
#             self.model = None
    
#     def _preprocess_image(self, image: Image.Image) -> torch.Tensor:
#         """이미지 전처리"""
#         transform = transforms.Compose([
#             transforms.Resize((512, 512)),
#             transforms.ToTensor(),
#             transforms.Normalize(
#                 mean=[0.485, 0.456, 0.406],
#                 std=[0.229, 0.224, 0.225]
#             )
#         ])
        
#         # RGB 변환
#         if image.mode != 'RGB':
#             image = image.convert('RGB')
        
#         return transform(image).unsqueeze(0)
    
#     def predict(self, image_path: str) -> Dict:
#         """이미지 예측"""
#         if self.model is None:
#             return {
#                 "error": "Model not loaded",
#                 "message": f"모델 파일을 찾을 수 없습니다: {settings.AI_MODEL_PATH}"
#             }
        
#         try:
#             start_time = time.time()
            
#             # 이미지 로드 및 전처리
#             image = Image.open(image_path)
#             input_tensor = self._preprocess_image(image).to(self.device)
            
#             # 예측
#             with torch.no_grad():
#                 outputs = self.model(input_tensor)
#                 probabilities = torch.softmax(outputs, dim=1)
#                 confidence, predicted = torch.max(probabilities, 1)
            
#             # 결과 변환
#             pred_idx = predicted.item()
#             pred_class = self.CLASS_NAMES[pred_idx]
#             pred_class_kr = self.CLASS_NAMES_KR[pred_class]
#             confidence_score = confidence.item()
            
#             # 클래스별 확률
#             probs = probabilities[0].cpu().numpy()
#             probabilities_dict = {
#                 self.CLASS_NAMES[i]: float(probs[i])
#                 for i in range(len(self.CLASS_NAMES))
#             }
#             probabilities_kr_dict = {
#                 self.CLASS_NAMES_KR[self.CLASS_NAMES[i]]: float(probs[i])
#                 for i in range(len(self.CLASS_NAMES))
#             }
            
#             # Raw logits
#             raw_logits = outputs[0].cpu().numpy().tolist()
            
#             processing_time = time.time() - start_time
            
#             return {
#                 "prediction": pred_class,
#                 "prediction_kr": pred_class_kr,
#                 "confidence": confidence_score,
#                 "probabilities": probabilities_dict,
#                 "probabilities_kr": probabilities_kr_dict,
#                 "raw_logits": raw_logits,
#                 "processing_time": processing_time,
#                 "model_info": {
#                     "model_type": "ResNet50",
#                     "device": str(self.device),
#                     "image_size": "512x512"
#                 }
#             }
            
#         except Exception as e:
#             return {
#                 "error": str(e),
#                 "message": "예측 중 오류가 발생했습니다."
#             }


# # 싱글톤 인스턴스
# ai_service = GastricCancerAIService()
"""
위암 진단 AI 서비스 - Multi-Task Learning (MTL) 버전
Segmentation + Classification 동시 수행
segmentation_models_pytorch (smp) 기반
"""

import torch
import torch.nn as nn
import segmentation_models_pytorch as smp
from torchvision import transforms
from PIL import Image
import numpy as np
import io
import base64
import logging
from pathlib import Path
from typing import Dict, Union
import time

from app.core.config import settings

logger = logging.getLogger(__name__)


class GastricMTLModel(nn.Module):
    def __init__(self, n_seg_classes=5, n_cls_classes=4):
        super().__init__()
        # 공유 인코더 및 세그먼테이션 디코더
        self.unet = smp.Unet(
            encoder_name="resnet50",
            encoder_weights="imagenet",
            in_channels=3,
            classes=n_seg_classes
        )
        
        # 분류 헤드: 인코더의 마지막 특징(2048ch) 활용
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Linear(2048, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(512, n_cls_classes)
        )

    def forward(self, x):
        # 1. Shared Encoder
        features = self.unet.encoder(x)
        
        # 2. Segmentation Branch
        decoder_output = self.unet.decoder(features)
        seg_out = self.unet.segmentation_head(decoder_output)
        
        # 3. Classification Branch
        cls_feat = self.avgpool(features[-1]) # 마지막 레이어 (Batch, 2048, 1, 1)
        cls_feat = torch.flatten(cls_feat, 1)
        cls_out = self.classifier(cls_feat)
        
        return seg_out, cls_out

    def freeze_encoder(self):
        for param in self.unet.encoder.parameters():
            param.requires_grad = False

    def unfreeze_all(self):
        for param in self.parameters():
            param.requires_grad = True


class MTLAIService:
    """AI 진단 서비스 (MTL)"""
    
    CLASS_NAMES = ["STDI", "STNT", "STIN", "STMX"]
    CLASS_NAMES_KR = ["위샘암종", "위샘종양", "위샘내", "위샘혼합"]
    SEG_CLASS_NAMES = ["Background", "Tumor", "Stroma", "Normal", "Immune"]
    SEG_CLASS_NAMES_KR = ["배경", "종양", "기질", "정상", "면역세포"]
    SEG_COLORS = {
        0: [0, 0, 0], 1: [255, 0, 0], 2: [0, 255, 0],
        3: [0, 0, 255], 4: [255, 255, 0],
    }
    
    def __init__(self, model_path: str = None):
        self.model_path = Path(model_path or settings.AI_MODEL_PATH)
        self.device = torch.device(settings.AI_DEVICE if torch.cuda.is_available() else "cpu")
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self._load_model()
    
    def _load_model(self):
        print("DEBUG: [1/5] _load_model 진입")
        if not self.model_path.exists():
            print(f"DEBUG: [ERR] 모델 파일 없음: {self.model_path}")
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        try:
            print("DEBUG: [2/5] GastricMTLModel 객체 생성 중...")
            self.model = GastricMTLModel(n_seg_classes=5, n_cls_classes=4)

            print(f"DEBUG: [3/5] 가중치 파일 로드 시작 (장치: {self.device})...")
            state_dict = torch.load(self.model_path, map_location=self.device, weights_only=False)

            print("DEBUG: [4/5] state_dict 정제 및 주입 중...")
            # 최종 로드
            missing_keys, unexpected_keys = self.model.load_state_dict(state_dict, strict=False)

            print(f"⚠️ Missing keys: {len(missing_keys)}")
            print(f"⚠️ Unexpected keys: {len(unexpected_keys)}")

                
            print("DEBUG: [5/5] 모델을 디바이스로 이동 및 eval 모드 전환")
            self.model.to(self.device)
            self.model.eval()
            print("✅✅✅ 모든 로드 과정 완료! ✅✅✅")
            logger.info(f"✅ MTL Model loaded: {self.model_path}, Device: {self.device}")
        except Exception as e:
            print(f"❌❌❌ 로드 중 예외 발생: {str(e)}")
            logger.error(f"❌ Failed to load MTL model: {e}")
            raise

    
    def predict(self, image_input: Union[str, bytes]) -> Dict:
        start_time = time.time()
        print("DEBUG: 1. 전처리 시작")
        try:
            print("DEBUG: 2. 모델 입력 직전") # <--- 여기까지 찍히는지 확인
            if isinstance(image_input, str):
                image = Image.open(image_input).convert('RGB')
            else:
                image = Image.open(io.BytesIO(image_input)).convert('RGB')
            original_size = image.size
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            print(f"DEBUG: Input Shape: {input_tensor.shape}") 
            # 반드시 torch.Size([1, 3, 512, 512]) 여야 합니다. (앞에 1이 필수)
            print(f"DEBUG: Input Device: {input_tensor.device}")
            print(f"DEBUG: Model Device: {next(self.model.parameters()).device}")
            # with torch.no_grad():
            #     print("DEBUG: 4. no_grad") # <
            #     seg_out, cls_out = self.model(input_tensor)
            with torch.no_grad():
                print("DEBUG: 4. no_grad 진입")
                
                # 1단계: 인코더만 실행해보기
                features = self.model.unet.encoder(input_tensor)
                print(f"DEBUG: 4-1. 인코더 완료 (특징 맵 개수: {len(features)})")
                
                # 2단계: 디코더 실행
                decoder_output = self.model.unet.decoder(*features)
                seg_out = self.model.unet.segmentation_head(decoder_output)
                print("DEBUG: 4-2. 세그멘테이션 완료")
                
                # 3단계: 분류기 실행
                cls_feat = self.model.avgpool(features[-1])
                cls_feat = torch.flatten(cls_feat, 1)
                cls_out = self.model.classifier(cls_feat)
                print("DEBUG: 4-3. 분류 완료")
                
            print("DEBUG: 5. cls_out") # <
            cls_probs = torch.softmax(cls_out, dim=1)[0]
            cls_pred = torch.argmax(cls_probs).item()
            confidence = cls_probs[cls_pred].item()

            seg_pred = torch.argmax(seg_out, dim=1)[0].cpu().numpy()
            seg_stats = self._calculate_segmentation_stats(seg_pred)
            seg_image_b64 = self._create_segmentation_overlay(image, seg_pred)

            processing_time = time.time() - start_time
            return {
                "prediction": self.CLASS_NAMES[cls_pred],
                "prediction_kr": self.CLASS_NAMES_KR[cls_pred],
                "confidence": float(confidence),
                "probabilities": {name: float(prob) for name, prob in zip(self.CLASS_NAMES, cls_probs.cpu().numpy())},
                "probabilities_kr": {name: float(prob) for name, prob in zip(self.CLASS_NAMES_KR, cls_probs.cpu().numpy())},
                "raw_logits": cls_out[0].cpu().numpy().tolist(),
                "segmentation": {"stats": seg_stats, "image_base64": seg_image_b64, "class_colors": self.SEG_COLORS},
                "processing_time": processing_time,
                "model_info": {
                    "model_type": "UNet + ResNet50 (MTL)",
                    "input_size": [512, 512],
                    "original_size": list(original_size),
                    "device": str(self.device),
                }
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            logger.error(f"Prediction error: {e}")
            return {"error": True, "message": str(e)}
    
    def _calculate_segmentation_stats(self, seg_mask: np.ndarray) -> Dict:
        total_pixels = seg_mask.size
        stats = {"ratios": {}, "pixel_counts": {}}
        for cls_id, cls_name in enumerate(self.SEG_CLASS_NAMES):
            count = np.sum(seg_mask == cls_id)
            ratio = count / total_pixels
            stats["ratios"][cls_name.lower()] = float(ratio)
            stats["pixel_counts"][cls_name.lower()] = int(count)
        return stats
    
    def _create_segmentation_overlay(self, original_image: Image.Image, seg_mask: np.ndarray) -> str:
        img_resized = original_image.resize((512, 512))
        img_np = np.array(img_resized)
        color_mask = np.zeros((512, 512, 3), dtype=np.uint8)
        for cls_id, color in self.SEG_COLORS.items():
            color_mask[seg_mask == cls_id] = color
        alpha = 0.5
        overlay = (img_np * (1 - alpha) + color_mask * alpha).astype(np.uint8)
        overlay_img = Image.fromarray(overlay)
        buffered = io.BytesIO()
        overlay_img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def get_model_info(self) -> Dict:
        return {
            "model_path": str(self.model_path),
            "device": str(self.device),
            "model_type": "UNet + ResNet50 (MTL)",
            "num_seg_classes": 5,
            "num_cls_classes": 4,
            "classification_classes": self.CLASS_NAMES_KR,
            "segmentation_classes": self.SEG_CLASS_NAMES_KR,
        }

print("!!!!!!!!!!!!!!!! AI SERVICE FILE LOADING START !!!!!!!!!!!!!!!!")
try:
    ai_service = MTLAIService()
    logger.info("✅ MTL AI Service initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize MTL AI Service: {e}")
    ai_service= None

