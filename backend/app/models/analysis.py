
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base


class CallAnalysis(Base):

    __tablename__ = "call_analyses"

    id = Column(Integer, primary_key=True, index=True)

    call_id = Column(
        Integer,
        ForeignKey("calls.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    summary = Column(Text, nullable=False)

    customer_intent = Column(
        String(100),
        nullable=False
    )

    sentiment = Column(
        String(30),
        nullable=False
    )

    follow_up_required = Column(
        Boolean,
        nullable=False
    )

    analysis_method = Column(
        String(50),
        nullable=False,
        default="rule_based"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
