from model.base import Base

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Organization(Base):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(Text, unique=True, doc="Название организации")

    divisions = relationship("Division", back_populates="organization")
    positions = relationship("Position", back_populates="organization")
    doctors = relationship("Doctor", back_populates="organization")
