from datetime import date
from sqlmodel import Session, SQLModel, create_engine
"""
from db_models import *

sqlite_file_name = "Trip Planner.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def add_data():
    trip1 = Trip(title="Pondicherry", start_date=date(2025, 1, 15), end_date=date(2025, 1, 16))
    trip2 = Trip(title="Mysore", start_date=date(2025, 2, 5), end_date=date(2025, 2, 15))
    trip3 = Trip(title="Somanath/Dwarka", start_date=date(2025, 3, 25))

    
    user1 = User(name="kartik", email="singhkartik45057@gmail.com", date_of_birth=date(2001, 4, 6), trips=[trip1, trip2, trip3])
    user2 = User(name="vatsal", email="vatsalmishra557@gmail.com", date_of_birth=date(2000, 7, 15), trips=[trip1])
    user3 = User(name="rajat", email="rajatnigam357@gmail.com", date_of_birth=date(1997, 1, 19), trips=[trip1])
    with Session(engine) as session:
        session.add(user1)  
        session.add(user2)
        session.add(user3)

        session.commit()

def main():  
    create_db_and_tables()  
    add_data()


if __name__ == "__main__":  
    main()
"""