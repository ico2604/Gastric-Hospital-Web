from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user, get_password_hash
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel

router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)  # 인증 필요
):
    """
    사용자 목록 조회
    
    - 인증 필요 (Bearer Token)
    """
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@router.post("/", response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)  # 인증 필요
):
    """
    사용자 생성
    
    - 인증 필요 (Bearer Token)
    - 관리자 권한 필요
    """
    # 관리자 권한 체크
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # 이메일 중복 체크
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 사용자명 중복 체크
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # 사용자 생성
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)  # 인증 필요
):
    """
    사용자 상세 조회
    
    - 인증 필요 (Bearer Token)
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)  # 인증 필요
):
    """
    사용자 정보 수정
    
    - 인증 필요 (Bearer Token)
    - 본인 또는 관리자만 수정 가능
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 권한 체크: 본인 또는 관리자
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # 업데이트
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)  # 인증 필요
):
    """
    사용자 삭제
    
    - 인증 필요 (Bearer Token)
    - 관리자 권한 필요
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
