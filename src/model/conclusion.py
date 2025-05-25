import uuid

from model.base import Base

from sqlalchemy import UUID, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Conclusion(Base):
    __tablename__ = "conclusion"

    text: Mapped[str] = mapped_column(Text, nullable=False, doc="Текст заключения")
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patient.id"), nullable=False, doc="ID пациента"
    )
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("doctor.id"), nullable=False, doc="ID врача"
    )

    patient = relationship("Patient", back_populates="directions", uselist=False)
    doctor = relationship("Doctor", back_populates="directions", uselist=False)
