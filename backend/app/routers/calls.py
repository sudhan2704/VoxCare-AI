
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.call import Call
from app.models.analysis import CallAnalysis
from app.schemas.call import (
    CallCreate,
    CallResponse,
    CallDetailResponse
)
from app.schemas.analysis import(
    CallAnalysisResponse,
    CallAnalysisHistoryResponse
)
from app.services.local_analysis import analyze_call


router = APIRouter(
    prefix="/api/v1/calls",
    tags=["Calls"]
)


# Create a new call
@router.post("/", response_model=CallResponse)
def create_call(
    call_data: CallCreate,
    db: Session = Depends(get_db)
):
    existing_call = db.query(Call).filter(
        Call.call_reference == call_data.call_reference
    ).first()

    if existing_call:
        raise HTTPException(
            status_code=409,
            detail="Call reference already exists"
        )

    new_call = Call(**call_data.model_dump())

    db.add(new_call)
    db.commit()
    db.refresh(new_call)

    return new_call


# Get all calls
@router.get("/", response_model=list[CallResponse])
def get_calls(db: Session = Depends(get_db)):
    return db.query(Call).order_by(
        Call.created_at.desc()
    ).all()


# Get one call by ID
@router.get("/{call_id}", response_model=CallResponse)
def get_call(
    call_id: int,
    db: Session = Depends(get_db)
):
    call = db.query(Call).filter(
        Call.id == call_id
    ).first()

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    return call


# Analyse a saved call
@router.post(
    "/{call_id}/analyze",
    response_model=CallAnalysisResponse
)
def analyze_saved_call(
    call_id: int,
    db: Session = Depends(get_db)
):
    # Step 1: Find the call
    call = db.query(Call).filter(
        Call.id == call_id
    ).first()

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    # Step 2: Analyse the transcript
    analysis_result = analyze_call(call.transcript)

    # Step 3: Create analysis record
    new_analysis = CallAnalysis(
        call_id=call.id,
        **analysis_result
    )

    # Step 4: Save analysis in PostgreSQL
    try:
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)

    except Exception:
        db.rollback()
        raise

    # Step 5: Return analysis result
    return new_analysis


@router.get("/{call_id}/details", response_model=CallDetailResponse)
def get_call_details(
    call_id: int,
    db: Session = Depends(get_db)
):
    result = (
        db.query(Call, CallAnalysis)
        .outerjoin(
            CallAnalysis,
            Call.id == CallAnalysis.call_id
        )
        .filter(Call.id == call_id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    call, analysis = result

    return {
        "call_reference": call.call_reference,
        "agent_name": call.agent_name,
        "transcript": call.transcript,
        "status": call.status,
        "created_at": call.created_at,
        "analysis": analysis
    }


@router.get(
    "/{call_id}/analyses",
    response_model=CallAnalysisHistoryResponse
)
def get_call_analysis_history(
    call_id: int,
    db: Session = Depends(get_db)
):
    # Step 1: Check whether the call exists
    call = db.query(Call).filter(
        Call.id == call_id
    ).first()

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    # Step 2: Retrieve all analysis records
    analyses = (
        db.query(CallAnalysis)
        .filter(CallAnalysis.call_id == call_id)
        .order_by(
            CallAnalysis.created_at.desc(),
            CallAnalysis.id.desc()
        )
        .all()
    )

    # Step 3: Return analysis history
    return {
        "call_id": call_id,
        "total_analyses": len(analyses),
        "analyses": analyses
    }
