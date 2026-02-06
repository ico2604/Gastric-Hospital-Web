"""
Checkpoint 구조 확인 스크립트
실행: python debug_checkpoint.py
"""

import torch
from pathlib import Path

# checkpoint 파일 경로
checkpoint_path = Path("unet_resnet50_best.pth")

if not checkpoint_path.exists():
    print(f"❌ 파일을 찾을 수 없습니다: {checkpoint_path}")
    print("경로를 확인하거나 실제 파일 위치로 이동하세요.")
    exit(1)

print(f"📁 Checkpoint 파일: {checkpoint_path}")
print(f"📊 파일 크기: {checkpoint_path.stat().st_size / 1024 / 1024:.2f} MB\n")

# checkpoint 로드
print("⏳ Checkpoint 로딩 중...")
checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)

# checkpoint 타입 확인
print(f"✅ Checkpoint 타입: {type(checkpoint)}\n")

if isinstance(checkpoint, dict):
    print("📋 Checkpoint Keys:")
    for key in checkpoint.keys():
        print(f"  - {key}")
    print()
    
    # state_dict가 있는 경우
    if 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
        print("📦 state_dict Keys (처음 20개):")
    elif 'model' in checkpoint:
        state_dict = checkpoint['model']
        print("📦 model Keys (처음 20개):")
    else:
        # checkpoint 자체가 state_dict인 경우
        state_dict = checkpoint
        print("📦 State Dict Keys (처음 20개):")
    
    # 키 목록 출력
    keys = list(state_dict.keys())
    for i, key in enumerate(keys[:20]):
        tensor = state_dict[key]
        print(f"  {i+1:2d}. {key:60s} → shape: {list(tensor.shape)}")
    
    if len(keys) > 20:
        print(f"  ... (총 {len(keys)}개 키)")
    
    print("\n" + "="*80)
    print("🔍 구조 분석:")
    print("="*80)
    
    # 키 패턴 분석
    patterns = {}
    for key in keys:
        prefix = key.split('.')[0] if '.' in key else key
        patterns[prefix] = patterns.get(prefix, 0) + 1
    
    print("\n주요 모듈 (prefix):")
    for prefix, count in sorted(patterns.items(), key=lambda x: -x[1]):
        print(f"  - {prefix:20s}: {count:3d}개 파라미터")
    
    # 인코더 구조 확인
    print("\n인코더 구조:")
    encoder_keys = [k for k in keys if k.startswith('encoder')]
    if encoder_keys:
        print(f"  ✅ 발견: {len(encoder_keys)}개 인코더 키")
        print(f"  예시: {encoder_keys[0]}")
    else:
        print("  ❌ 'encoder'로 시작하는 키 없음")
    
    # 디코더 구조 확인
    print("\n디코더 구조:")
    decoder_keys = [k for k in keys if 'decoder' in k.lower() or 'upconv' in k.lower()]
    if decoder_keys:
        print(f"  ✅ 발견: {len(decoder_keys)}개 디코더 키")
        print(f"  예시: {decoder_keys[0]}")
    else:
        print("  ❌ 디코더 관련 키 없음")
    
    # Segmentation head 확인
    print("\nSegmentation Head:")
    seg_keys = [k for k in keys if 'seg' in k.lower()]
    if seg_keys:
        print(f"  ✅ 발견: {len(seg_keys)}개 segmentation 키")
        print(f"  예시: {seg_keys[0]}")
    else:
        print("  ❌ segmentation 관련 키 없음")
    
    # Classification head 확인
    print("\nClassification Head:")
    cls_keys = [k for k in keys if k.startswith('fc') or 'classifier' in k.lower()]
    if cls_keys:
        print(f"  ✅ 발견: {len(cls_keys)}개 classification 키")
        for k in cls_keys:
            print(f"    - {k}: {list(state_dict[k].shape)}")
    else:
        print("  ❌ classification 관련 키 없음")

else:
    print("⚠️ Checkpoint가 딕셔너리가 아닙니다. 직접 state_dict일 수 있습니다.")
    print(f"전체 구조:\n{checkpoint}")

print("\n" + "="*80)
print("💡 분석 완료!")
print("="*80)
