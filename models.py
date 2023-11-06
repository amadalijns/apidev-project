from sqlalchemy import Boolean, Column, Index, Integer, String

from database import Base

# Definieer de database tabel voor taken
class Task(Base):
    __tablename__ = "tasks"

    # Kolommen voor de takentabel
    id = Column(Integer, primary_key=True, index=True)  # ID van de taak, is de primaire sleutel
    name = Column(String)  # Naam van de taak
    completed = Column(Boolean, default=False)  # Veld dat aangeeft of de taak is voltooid of niet
