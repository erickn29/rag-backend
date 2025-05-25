import uuid

from model.base import Base

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Direction(Base):
    __tablename__ = "direction"

    type: Mapped[str] = mapped_column(String(50), doc="Тип направления")
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patient.id"), nullable=False, doc="ID пациента"
    )
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("doctor.id"), nullable=True, doc="ID врача"
    )

    patient = relationship("Patient", back_populates="directions", uselist=False)
    doctor = relationship("Doctor", back_populates="directions", uselist=False)
