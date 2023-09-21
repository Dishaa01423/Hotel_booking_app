import pandas as pd

df = pd.read_csv("hotels.csv",dtype = {"id": str})
df_cards = pd.read_csv("cards.csv",dtype=str).to_dict(orient="records")
df_security = pd.read_csv("card_security.csv",dtype=str)
class Hotel:
    def __init__(self,hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id,"name"].squeeze()

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id ,"available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        df.loc[df["id"]==self.hotel_id,"available"] = "no"
        df.to_csv("hotels.csv",index = False)

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number":self.number, "expiration":expiration,
                       "holder": holder, "cvc":cvc}
        if card_data in df_cards:
            return True
        else:
            return False

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_security.loc[df_security["number"] == self.number,"password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self,customer_name,hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thankyou for your reservation!!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """
        return content

class SpaReservationTicket:
    def __init__(self, spa_customer_name, spa_object):
        self.spa_customer_name = spa_customer_name
        self.spa = spa_object

    def generate(self):
        content = f"""
        Thankyou for your SPA reservation!!
        Here are your booking data:
        Name: {self.spa_customer_name}
        Hotel Name: {self.spa.name}
        """
        return content


print(df)
hotel_Id = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_Id)


if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name = name,hotel_object = hotel)
            print(reservation_ticket.generate())
        else:
            print("Credit card authentication failed.")
    else:
        print("Their was an error in the payment pathway. Transaction incomplete!!")
else:
    print("Hotel is not free.")

spa_package = input("Do you want to book a spa package?  ")
if spa_package == "yes":
    st = SpaReservationTicket(spa_customer_name = name,spa_object = hotel)
    print(st.generate())
else:
    print("Your booking for spa was not confirmed.")