from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import List, Union, Optional

from fastapi import APIRouter
from pydantic import BaseModel
import json
from apps.web.models.models import Models, ModelModel, ModelForm, ModelResponse

from utils.utils import get_verified_user, get_admin_user
from constants import ERROR_MESSAGES

router = APIRouter()

###########################
# getModels
###########################


@router.get("/", response_model=List[ModelResponse])
async def get_models(user=Depends(get_verified_user)):
    return Models.get_all_models()


############################
# AddNewModel
############################


@router.post("/add", response_model=Optional[ModelModel])
async def add_new_model(form_data: ModelForm, user=Depends(get_admin_user)):
    model = Models.insert_new_model(form_data, user.id)

    if model:
        return model
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.DEFAULT(),
        )


############################
# GetModelById
############################


@router.get("/{id}", response_model=Optional[ModelModel])
async def get_model_by_id(id: str, user=Depends(get_verified_user)):
    model = Models.get_model_by_id(id)

    if model:
        return model
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateModelById
############################


@router.post("/{id}/update", response_model=Optional[ModelModel])
async def update_model_by_id(
    id: str, form_data: ModelForm, user=Depends(get_admin_user)
):
    model = Models.get_model_by_id(id)
    if model:
        model = Models.update_model_by_id(id, form_data)
        return model
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )


############################
# DeleteModelById
############################


@router.delete("/{id}/delete", response_model=bool)
async def delete_model_by_id(id: str, user=Depends(get_admin_user)):
    result = Models.delete_model_by_id(id)
    return result
