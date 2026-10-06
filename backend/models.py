import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from .database import Base


class EnquiryStatus(str, enum.Enum):
    NEW = "New"
    CONTACTED = "Contacted"
    TEST_RIDE_DONE = "Test Ride Done"
    PURCHASED = "Purchased"
    LOST = "Lost"


class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    city = Column(String, nullable=False)
    vehicle_model = Column(String, nullable=False)
    status = Column(Enum(EnquiryStatus), default=EnquiryStatus.NEW, nullable=False)
    notes = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)