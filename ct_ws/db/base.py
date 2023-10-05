from sqlalchemy.orm import DeclarativeBase

from ct_ws.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
