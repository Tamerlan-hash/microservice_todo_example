from app.settings.database_configs.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, BigInteger, String,
    DateTime, Text, Boolean,
    Integer, Enum, ForeignKey,
    Table,
)

accounts_task_association = Table(
    'accounts-task',
    Base.metadata,
    Column('Account_id', BigInteger, ForeignKey('Accounts.account_id')),
    Column('Task_id', BigInteger, ForeignKey('Tasks.id', ondelete="CASCADE")),
)


class Task(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(BigInteger, ForeignKey("Projects.id", ondelete="CASCADE"))
    accounts = relationship(
        "Account",
        secondary=accounts_task_association,
        backref='tasks',
        lazy='select',
    )
    deadline = Column(DateTime, nullable=True)

