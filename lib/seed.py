from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie


engine = create_engine('sqlite:///freebies.db')


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


session.query(Freebie).delete()
session.commit()


companies_data = [
    {"name": "Google", "founding_year": 1998},
    {"name": "Microsoft", "founding_year": 1975},
    {"name": "Amazon", "founding_year": 1994},
    {"name": "Apple", "founding_year": 1976}
]

companies = {}
for company_data in companies_data:
    company = session.query(Company).filter_by(name=company_data["name"]).first()
    if not company:
        company = Company(**company_data)
        session.add(company)
    companies[company_data["name"]] = company


devs_data = [
    {"name": "Alice Smith"},
    {"name": "Bob Johnson"},
    {"name": "Charlie Williams"},
    {"name": "Dana Brown"}
]

devs = {}
for dev_data in devs_data:
    dev = session.query(Dev).filter_by(name=dev_data["name"]).first()
    if not dev:
        dev = Dev(**dev_data)
        session.add(dev)
    devs[dev_data["name"]] = dev

session.commit()

# Creating freebies
freebies_data = [
    {"item_name": "T-Shirt", "value": 20, "dev": devs["Alice Smith"], "company": companies["Google"]},
    {"item_name": "Sticker Pack", "value": 5, "dev": devs["Alice Smith"], "company": companies["Microsoft"]},
    {"item_name": "Water Bottle", "value": 15, "dev": devs["Bob Johnson"], "company": companies["Google"]},
    {"item_name": "Backpack", "value": 50, "dev": devs["Bob Johnson"], "company": companies["Amazon"]},
    {"item_name": "Laptop Sleeve", "value": 30, "dev": devs["Charlie Williams"], "company": companies["Microsoft"]},
    {"item_name": "Notebook", "value": 10, "dev": devs["Charlie Williams"], "company": companies["Apple"]},
    {"item_name": "Hoodie", "value": 40, "dev": devs["Dana Brown"], "company": companies["Amazon"]},
    {"item_name": "Coffee Mug", "value": 12, "dev": devs["Dana Brown"], "company": companies["Google"]}
]

for freebie_data in freebies_data:
    freebie = Freebie(**freebie_data)
    session.add(freebie)

session.commit()

print("Database seeded successfully!")


print("\nSample data verification:")
print(f"Total companies: {session.query(Company).count()}")
print(f"Total devs: {session.query(Dev).count()}")
print(f"Total freebies: {session.query(Freebie).count()}")


alice = devs["Alice Smith"]
google = companies["Google"]

print(f"\nAlice's freebies: {[f.item_name for f in alice.freebies]}")
print(f"Companies Alice has freebies from: {[c.name for c in alice.companies]}")
print(f"Google's freebies: {[f.item_name for f in google.freebies]}")
print(f"Devs with Google freebies: {[d.name for d in google.devs]}")

import ipdb 

ipdb.set_trace(context=10)