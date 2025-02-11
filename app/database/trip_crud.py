from app.database.db_main import engine
from sqlmodel import Session, select, update
from app.database.user_crud import get_user_by_id_from_db
from app.models import *
from app.database.db_models import *
from sqlalchemy.orm import selectinload
from sqlalchemy import and_
from sqlalchemy import orm

def create_trip_in_db(trip: Trip_Create, current_user: User):
    try:
        with Session(engine) as session:
            user_ids = trip.users
            statement = select(User).where(User.id.in_(user_ids))
            users = session.exec(statement).all()
            new_trip = Trip(title=trip.title, start_date=trip.start_date, end_date=trip.end_date, created_by_id=current_user.id, created_by=current_user, users=users)
            session.add(new_trip)
            session.commit()
            session.refresh(new_trip)
            return new_trip
    except Exception as e:
        session.rollback()
        raise e
    
def get_all_trips_from_db():
    with Session(engine) as session:
        try:
            #statement = select(Trip).options(orm.selectinload(Trip.created_by), orm.selectinload(Trip.users), orm.selectinload(Trip.expenses))
            statement = select(Trip).options(orm.selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                users = item.users
                expenses = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_trip_by_id_from_db(trip_id: int):
    with Session(engine) as session:
        try:
            statement = select(Trip).where(Trip.id == trip_id).options(selectinload(Trip.created_by))
            result = session.exec(statement).first()
            users = result.users
            expenses = result.expenses
            return result
        except Exception as e:
            raise e

def filter_trip_by_user(user_id: int, title: str):
    with Session(engine) as session:
        try:
            statement = select(Trip).where(Trip.created_by_id == user_id, Trip.title.like(f"%{title}%")).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                traveller = item.users
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_after_specified_date(user_id: int, start_after: date, title: str):
    with Session(engine) as session:
        try:
            statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_before_specified_date(user_id: int, start_before: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date < start_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_ending_after_specified_date(user_id: int, end_after: date, title:str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.end_date > end_after, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e

def get_user_trips_ending_before_specified_date(user_id: int, end_before: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_between_specified_dates(user_id: int, start_after: date, start_before: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.start_date < start_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e

def get_user_trips_ending_between_specified_dates(user_id: int, end_after: date, end_before:date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.end_date > end_after, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_and_ending_within_specified_daterange(user_id: int, start_after: date, end_before: date, title: str):  
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_after_and_ending_after_specified_dates(user_id: int, start_after: date, end_after: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.end_date > end_after, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_before_and_ending_after_specified_dates(user_id: int, start_before: date, end_after: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date < start_before, Trip.end_date > end_after, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
               
def get_user_trips_starting_before_and_ending_before_specified_dates(user_id: int, start_before: date, end_before: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date < start_before, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_within_daterange_and_ending_after_specified_date(user_id: int, start_after: date, start_before: date, end_after: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.start_date < start_before, Trip.end_date > end_after, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def get_user_trips_starting_within_daterange_and_ending_before_specified_date(user_id: int, start_after: date, start_before: date, end_before: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.start_date < start_before, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
  
def get_user_trips_ending_within_daterange_and_starting_after_specified_date(user_id: int, start_after: date, end_before: date, end_after: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.end_date > end_after, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
  
def get_user_trips_ending_within_daterange_and_starting_before_specified_date(user_id: int, start_before: date, end_before: date, end_after: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date < start_before, Trip.end_date > end_after, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
  
def get_user_trips_starting_within_daterange_and_ending_within_daterange(user_id: int, start_after: date, start_before: date, end_before: date, end_after: date, title: str):
    with Session(engine) as session:
        try:
            statement = statement = select(Trip).where(and_(Trip.created_by_id == user_id, Trip.start_date > start_after, Trip.start_date < start_before, Trip.end_date > end_after, Trip.end_date < end_before, Trip.title.like(f"%{title}%"))).options(selectinload(Trip.created_by))
            result = session.exec(statement).all()
            for item in result:
                expense = item.expenses
            return result
        except Exception as e:
            raise e
        
def add_traveller_to_the_trip_in_db(trip_id: int, user_id: int):
    with Session(engine) as session:
        try:
            link = UserTripLink(trip_id=trip_id, user_id=user_id)
            session.add(link)
            session.commit()
            session.refresh(link)
        except Exception as e:
            session.rollback()
            raise e
        
def remove_trip_from_db(trip_id: int):
    with Session(engine) as session:
        try:
            statement = select(UserTripLink).where(UserTripLink.trip_id == trip_id)
            result = session.exec(statement).all()
            if result:
                for item in result:
                    session.delete(item)
                    session.commit()

            statement = select(Expense).where(Expense.trip_id == trip_id)
            result = session.exec(statement).all()
            if result:
                for item in result:
                    session.delete(item)
                    session.commit()

            statement = select(Trip).where(Trip.id == trip_id)
            result = session.exec(statement).first()
            if result:
                session.delete(result)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        
def remove_traveller_from_the_trip_in_db(trip_id: int, user_id: int):
    with Session(engine) as session:
        try:
            statement = select(UserTripLink).where(and_(UserTripLink.trip_id == trip_id, UserTripLink.user_id == user_id))
            result = session.exec(statement).first()
            if result:
                session.delete(result)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        
def update_trip_startdate_and_enddate_in_db(trip_id: int, trip_start_date: Optional[date], trip_end_date: Optional[date]):
    with Session(engine) as session:
        try:
            query = update(Trip).where(Trip.id == trip_id)
            statement = None
            if trip_start_date and trip_end_date:
                statement = query.values(start_date=trip_start_date, trip_end_date=trip_end_date)
            elif trip_start_date:
                statement = query.values(start_date=trip_start_date)
            else:
                statement = query.values(trip_end_date=trip_end_date)

            if statement is not None:
                result = session.exec(statement)
                session.commit()
                return result
        except Exception as e:
            session.rollback()
            raise e
        
def update_trip_title_in_db(trip_id: int, trip_title: str):
    with Session(engine) as session:
        try:
            statement = update(Trip).where(Trip.id == trip_id).values(title = trip_title)
            result = session.exec(statement)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
