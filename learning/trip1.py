import uuid
from fastapi import FastAPI, Query, status, HTTPException
from pydantic import BaseModel, Field, field_validator, EmailStr
from enum import Enum
from typing import Dict, List, Optional
from datetime import date
import requests


app = FastAPI()

def get_exchange_rates():
    exchange_rates = {}
    base_currency = "INR"
    url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "rates" in data:
            exchange_rates = data.get("rates")
        return exchange_rates
    else:
        raise HTTPException(status_code=500, detail="Something Went Wrong")
   
exchange_rates = get_exchange_rates()

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(min_length=2, max_length=50, description="User's name")
    email: EmailStr = Field(description="User's Email id")
    date_of_birth: date = Field(description="User's date of birth")

class PaymentMode(str, Enum):
    CASH = "Cash",
    CREDIT_CARD = "Credit Card",
    DEBIT_CARD = "Debit Card",
    BANK_TRANSFER = "Bank Transfer",
    CHECK = "Check",
    DIGITAL_WALLET = "Digital Wallet",
    UPI = "UPI",
    BNPL = "Buy Now, Pay Later"

class CurrencyCode(str, Enum):
    INR = "INR",
    USD = "USD",
    EUR = "EUR"

class Payment(BaseModel):
    currency: CurrencyCode
    amount: float
    payment_mode: PaymentMode

class Expense(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = Field(default=None, min_length=10, max_length=100, description="Details of expense, eg: 2000 rupees spend for dinner at cafe")
    amount: float = Field(gt=0, description="Total amount paid as a part of this expense")
    payment_Details_By_UserId: Dict[str, Payment] = Field(description="Stores who has contributed how much in the total amount paid as part of this expense")
    split_between: List[str] = Field(description="List of user ids of users between whom amount needs to be splitted")

class Trip(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(min_length=3, max_length=50, description="Title of the trip")
    start_date: date = Field(description="Start date of the trip")
    end_date: Optional[date] = Field(default=None, description="End date of the trip")
    travellers: Optional[List[User]] = Field(default=[], description="List of User ids of users who are part of the trip")
    expenses: Optional[List[Expense]] = Field(default=[], description="List of Expense ids of expenses that incurred during the trip")
    places_travelled: Optional[List[str]] = Field(default=[], description="List of places visited as a part of the trip")

user1 = User(name="kartik", email="singhkartik45057@gmail.com", date_of_birth="2001-04-06")
user2 = User(name="vatsal", email="vatsalMishra77@gmail.com", date_of_birth="2000-07-23")
user3 = User(name="rajat", email="rajatnigam57@gmail.com", date_of_birth="1997-12-06")
users = [user1, user2, user3]

expense1 = Expense(description="Day 1 lunch", amount=1200, payment_Details_By_UserId={user1.id: Payment(currency=CurrencyCode.INR, amount=1200, payment_mode=PaymentMode.UPI)}, split_between=[user1.id, user2.id, user3.id])
expense2 = Expense(description="Day 1 dinner", amount=800, payment_Details_By_UserId={user2.id: Payment(currency=CurrencyCode.INR, amount=500, payment_mode=PaymentMode.UPI), user3.id:Payment(currency=CurrencyCode.INR, amount=300, payment_mode=PaymentMode.UPI)}, split_between=[user1.id, user2.id, user3.id])
expense3 = Expense(description="Day 1 drinks", amount=645, payment_Details_By_UserId={user3.id: Payment(currency=CurrencyCode.INR, amount=645, payment_mode=PaymentMode.CASH)}, split_between=[user1.id, user2.id, user3.id])
expenses = [expense1, expense2, expense3]

trip1 = Trip(**{"title":"Pondicherry", "start_date":"2025-01-15", "end_date":"2025-01-20", "travellers":[user1, user2, user3], "expenses":[expense1, expense2, expense3]})
trip2 = Trip(**{"title":"Mysore", "start_date":"2025-02-25", "end_date":"2025-02-26", "travellers":[user1]})
trip3 = Trip(**{"title":"Somanath/Dwarka", "start_date":"2025-03-25"})
trips = [trip1, trip2, trip3]

@app.get("/")
def root():
    return "Welcome Users"

@app.get("/users/all", status_code=status.HTTP_200_OK)
def get_all_users():
    return users

@app.get("/trips/all", status_code=status.HTTP_200_OK)
def get_all_trips():
    return trips

@app.get("/trips/{id}", status_code=status.HTTP_200_OK)
def get_trip_by_id(id: str):
    for trip in trips:
        tripId = trip.id
        if tripId == id:
            return trip

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/trips", response_model=List[Trip])
def get_filtered_trips(title:Optional[str] = Query(None, min_length=3, max_length=50), start_date: Optional[date] = Query(None), end_date: Optional[date] = Query(None)):
    filtered_trips = []
    for trip in trips:
        trip_title = trip.title
        trip_start_date = trip.start_date
        trip_end_date = trip.end_date
        if title and start_date and end_date:
            if trip_title.lower() == title.lower() and trip_start_date == start_date and trip_end_date == end_date:
                filtered_trips.append(trip)
        elif title and start_date:
            if trip_title.lower() == title.lower() and trip_start_date == start_date:
                filtered_trips.append(trip)
        elif title and end_date:
            if trip_title.lower() == title.lower() and trip_end_date == end_date:
                filtered_trips.append(trip)
        elif title:
            if trip_title.lower() == title.lower():
                filtered_trips.append(trip)
        elif start_date:
            if trip_start_date == start_date:
                filtered_trips.append(trip)
        elif end_date:
            if trip_end_date == end_date:
                filtered_trips.append(trip)

    if not filtered_trips:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return filtered_trips

@app.get("/users/trips/{id}", status_code=status.HTTP_200_OK)
def get_trips_by_user_id(id: str):
    trips_by_user = []
    for trip in trips:
        travellers = trip.travellers
        for traveller in travellers:
            traveller_id = traveller.id
            if traveller_id == id:
                trips_by_user.append(trip)

    if not trips_by_user:
        raise HTTPException(status_code=404, detail="Item not found")

    return trips_by_user

@app.get("/trips/expenses/{id}", status_code=status.HTTP_200_OK)
def get_total_amount_spent_during_trip(id: str, currency: CurrencyCode):
    total_amount = 0.0
    trip_with_id = None
    for trip in trips:
        trip_id = trip.id
        if trip_id == id:
            trip_with_id = trip
    
    trip_expenses = trip_with_id.expenses if trip_with_id else []
    for expense in trip_expenses:
        total_amount += expense.amount if expense.amount else 0

    if currency == CurrencyCode.USD:
        if CurrencyCode.USD in exchange_rates:
            total_amount = total_amount * exchange_rates[CurrencyCode.USD]
            return total_amount
    elif currency == CurrencyCode.EUR:
        if CurrencyCode.EUR in exchange_rates:
            total_amount = total_amount * exchange_rates[CurrencyCode.EUR]
            return total_amount
    else:
        return total_amount

@app.get("trips/expenses/all", status_code=status.HTTP_200_OK)
def get_expenses_for_trip(id: str):
    for trip in trips:
        trip_id = trip.id
        if trip_id == id:
            trip_expenses = trip.expenses
            return trip_expenses

    raise HTTPException(status_code=404, detail="Iten not found")

@app.post("/trips", status_code=status.HTTP_201_CREATED)
def create_trip(trip: Trip):
    trips.append(trip)




