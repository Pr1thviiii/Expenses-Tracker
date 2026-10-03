from database import Base , engine
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Numeric , String ,ForeignKey
from decimal import Decimal

class UserModel(Base):
  __tablename__="users"

  id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
  email : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  hashed_pass :  Mapped[str] = mapped_column(String(500), nullable=False)
  
Base.metadata.create_all(bind=engine)


class Expenses(Base):
  __tablename__ = "expenses"  

  id: Mapped[int] = mapped_column(
      primary_key=True, autoincrement=True
  )  
  amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
  category: Mapped[str] = mapped_column(String(50), nullable=False)
  description: Mapped[str] = mapped_column(String(150), nullable=False)
  user_id : Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)

Base.metadata.create_all(bind=engine)



  