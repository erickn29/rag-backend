import uuid

from model.base import Base

from sqlalchemy import UUID, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Position(Base):
    __tablename__ = "position"

    name: Mapped[str] = mapped_column(Text, unique=True, doc="Название должности")
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
    )

    organization = relationship(
        "Organization", uselist=False, back_populates="positions"
    )
    doctors = relationship("Doctor", back_populates="position")
