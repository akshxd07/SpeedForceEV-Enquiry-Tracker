import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from .models import EnquiryStatus


class EnquiryBase(BaseModel):
    customer_name: str = Field(..., min_length=1, description="Customer name cannot be empty")
    phone: str
    city: str = Field(..., min_length=1)
    vehicle_model: str = Field(..., min_length=1)
    notes: Optional[str] = None

    @validator("phone")
    def validate_indian_phone(cls, v):

        cleaned_phone = re.sub(r"\D", "", v)
        if not re.match(r"^[6-9]\d{9}$", cleaned_phone):
            raise ValueError("Phone number must be a valid 10-digit Indian mobile number")
        return cleaned_phone

    @validator("customer_name")
    def validate_name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Customer name cannot be empty or only whitespace")
        return v.strip()


# Schema for creating an enquiry (POST request)
class EnquiryCreate(EnquiryBase):
    pass


# Schema for updating status (PATCH request)
class EnquiryStatusUpdate(BaseModel):
    status: EnquiryStatus


# Schema for returning enquiry data in responses
class EnquiryResponse(EnquiryBase):
    id: int
    status: EnquiryStatus
    created_date: datetime

class Config:
    from_attributes = True