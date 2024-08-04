import sqlalchemy as sa

from dating_backend.infrastructure.persistence.models.base import Base
from dating_backend.infrastructure.persistence.models.mixins import (
    UpdatedAtMixin,
)

from sqlalchemy.orm import Mapped, mapped_column


class UserORM(Base, UpdatedAtMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, primary_key=True
    )
    full_name: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    username: Mapped[str] = mapped_column(
        sa.String(255), nullable=True, default=None
    )
    is_active: Mapped[bool] = mapped_column(
        sa.Boolean, default=True, nullable=False
    )
