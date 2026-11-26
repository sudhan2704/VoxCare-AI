
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)

    call_reference = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    agent_name = Column(String(100), nullable=False)

    transcript = Column(Text, nullable=False)

    status = Column(
        String(30),
        default="uploaded",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
