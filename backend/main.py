from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import engine, Base, get_db
from .models import Enquiry, EnquiryStatus
from .schemas import EnquiryCreate, EnquiryResponse, EnquiryStatusUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpeedForce EV Vehicle Enquiry Tracker")


@app.post("/enquiries", response_model=EnquiryResponse, status_code=status.HTTP_201_CREATED)
def create_enquiry(enquiry: EnquiryCreate, db: Session = Depends(get_db)):
    db_enquiry = Enquiry(**enquiry.dict())
    db.add(db_enquiry)
    db.commit()
    db.refresh(db_enquiry)
    return db_enquiry


@app.get("/enquiries", response_model=List[EnquiryResponse])
def get_enquiries(
    status: Optional[EnquiryStatus] = None,
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Enquiry)
    if status:
        query = query.filter(Enquiry.status == status)
    if city:
        query = query.filter(Enquiry.city.ilike(f"%{city}%"))
    return query.all()


@app.patch("/enquiries/{enquiry_id}/status", response_model=EnquiryResponse)
def update_enquiry_status(
    enquiry_id: int,
    status_update: EnquiryStatusUpdate,
    db: Session = Depends(get_db)
):
    db_enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not db_enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    
    db_enquiry.status = status_update.status
    db.commit()
    db.refresh(db_enquiry)
    return db_enquiry


@app.delete("/enquiries/{enquiry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    db_enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not db_enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    
    db.delete(db_enquiry)
    db.commit()
    return None


@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    summary = {s.value: 0 for s in EnquiryStatus}
    
    results = db.query(
        Enquiry.status, func.count(Enquiry.id)
    ).group_by(Enquiry.status).all()
    
    for status_enum, count in results:
        summary[status_enum.value] = count
        
    return summary