import uuid

from model.base import Base

from sqlalchemy import UUID, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Division(Base):
    __tablename__ = "division"

    name: Mapped[str] = mapped_column(Text, doc="Название подразделения")
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id"),
        doc="ID организации",
        nullable=False,
    )

    organization = relationship(
        "Organization", uselist=False, back_populates="divisions"
    )
    doctors = relationship("Doctor", back_populates="division")
