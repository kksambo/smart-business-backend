"""
Seed database with demo data for ML training and testing
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
import random
import math
from database import SessionLocal
from models import Product, Sale, SalesItem, Customer, Location, Analytics, User
from utils import hash_password


def seed_demo_data(user_id: int = None):
    """Generate realistic demo/training data for ML models"""
    db = SessionLocal()

    try:
        # Define users to create
        users_data = [
            {
                "email": "sicelo.sambo@smart.com",
                "username": "sicelo.sambo",
                "business_name": "Sambo Electronics",
                "business_type": "Electronics Retail",
                "password": "123456@smart"
            },
            {
                "email": "vuthlari.maswanganyi@smart.com",
                "username": "vuthlari.maswanganyi",
                "business_name": "Maswanganyi Trading",
                "business_type": "General Trading",
                "password": "123456@smart"
            },
            {
                "email": "mhangwani.karabo@smart.com",
                "username": "mhangwani.karabo",
                "business_name": "Karabo Supplies",
                "business_type": "Office Supplies",
                "password": "123456@smart"
            },
            {
                "email": "mapulaa.mpelane@smart.com",
                "username": "mapulaa.mpelane",
                "business_name": "Mpelane Fashion",
                "business_type": "Fashion Retail",
                "password": "123456@smart"
            }
        ]

        # Create users if they don't exist
        created_users = []
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    hashed_password=hash_password(user_data["password"]),
                    business_name=user_data["business_name"],
                    business_type=user_data["business_type"],
                    is_active=True
                )
                db.add(user)
                db.flush()
                created_users.append(user)
            else:
                created_users.append(existing_user)

        # If specific user_id provided, only seed for that user
        users_to_seed = [db.query(User).filter(User.id == user_id).first()] if user_id else created_users

        for user in users_to_seed:
            if not user:
                continue

            print(f"Seeding data for user: {user.username}")

            # Define product categories and names (tailored to business type)
            if user.business_type == "Electronics Retail":
                products_data = [
                    {"name": "Laptop", "category": "Electronics", "cost": 400, "price": 750, "supplier": "Tech Suppliers Ltd"},
                    {"name": "Smartphone", "category": "Electronics", "cost": 180, "price": 350, "supplier": "Tech Suppliers Ltd"},
                    {"name": "Headphones", "category": "Electronics", "cost": 30, "price": 80, "supplier": "Audio Tech"},
                    {"name": "USB Cable", "category": "Accessories", "cost": 2, "price": 8, "supplier": "Cable Co"},
                    {"name": "Phone Case", "category": "Accessories", "cost": 3, "price": 12, "supplier": "Case Masters"},
                    {"name": "Screen Protector", "category": "Accessories", "cost": 1, "price": 5, "supplier": "Protection Plus"},
                    {"name": "Power Bank", "category": "Electronics", "cost": 15, "price": 45, "supplier": "Power Tech"},
                    {"name": "Keyboard", "category": "Electronics", "cost": 25, "price": 60, "supplier": "Input Devices Inc"},
                    {"name": "Mouse", "category": "Electronics", "cost": 10, "price": 25, "supplier": "Input Devices Inc"},
                    {"name": "Webcam", "category": "Electronics", "cost": 20, "price": 50, "supplier": "Vision Tech"},
                ]
            elif user.business_type == "General Trading":
                products_data = [
                    {"name": "Rice 5kg", "category": "Food", "cost": 25, "price": 45, "supplier": "Food Corp"},
                    {"name": "Cooking Oil 2L", "category": "Food", "cost": 15, "price": 28, "supplier": "Oil Traders"},
                    {"name": "Sugar 2kg", "category": "Food", "cost": 12, "price": 22, "supplier": "Sweet Supplies"},
                    {"name": "Soap Bars", "category": "Household", "cost": 2, "price": 5, "supplier": "Clean Corp"},
                    {"name": "Toothpaste", "category": "Personal Care", "cost": 3, "price": 8, "supplier": "Care Products"},
                    {"name": "Shampoo 500ml", "category": "Personal Care", "cost": 8, "price": 18, "supplier": "Hair Care Ltd"},
                    {"name": "Laundry Detergent", "category": "Household", "cost": 20, "price": 35, "supplier": "Clean Corp"},
                    {"name": "Batteries AA", "category": "Electronics", "cost": 1, "price": 3, "supplier": "Power Tech"},
                    {"name": "Matches Box", "category": "Household", "cost": 0.5, "price": 2, "supplier": "Utility Supplies"},
                    {"name": "Plastic Bags", "category": "Household", "cost": 0.1, "price": 0.5, "supplier": "Packaging Co"},
                ]
            elif user.business_type == "Office Supplies":
                products_data = [
                    {"name": "A4 Paper Pack", "category": "Stationery", "cost": 8, "price": 15, "supplier": "Paper Corp"},
                    {"name": "Ballpoint Pens", "category": "Stationery", "cost": 1, "price": 3, "supplier": "Writing Tools"},
                    {"name": "Notebooks", "category": "Stationery", "cost": 5, "price": 12, "supplier": "Book Makers"},
                    {"name": "Desk Lamp", "category": "Office", "cost": 15, "price": 45, "supplier": "Office Essentials"},
                    {"name": "Stapler", "category": "Office", "cost": 4, "price": 10, "supplier": "Office Tools"},
                    {"name": "Printer Paper", "category": "Stationery", "cost": 12, "price": 25, "supplier": "Paper Corp"},
                    {"name": "Whiteboard Markers", "category": "Office", "cost": 2, "price": 6, "supplier": "Writing Tools"},
                    {"name": "File Folders", "category": "Office", "cost": 1, "price": 3, "supplier": "Organization Co"},
                    {"name": "Calculator", "category": "Office", "cost": 8, "price": 20, "supplier": "Office Tools"},
                    {"name": "Correction Tape", "category": "Stationery", "cost": 1, "price": 4, "supplier": "Writing Tools"},
                ]
            else:  # Fashion Retail
                products_data = [
                    {"name": "T-Shirt", "category": "Clothing", "cost": 8, "price": 25, "supplier": "Fashion House"},
                    {"name": "Jeans", "category": "Clothing", "cost": 20, "price": 60, "supplier": "Denim Co"},
                    {"name": "Sneakers", "category": "Footwear", "cost": 25, "price": 80, "supplier": "Shoe Factory"},
                    {"name": "Dress", "category": "Clothing", "cost": 15, "price": 45, "supplier": "Fashion House"},
                    {"name": "Jacket", "category": "Clothing", "cost": 30, "price": 90, "supplier": "Outerwear Ltd"},
                    {"name": "Belt", "category": "Accessories", "cost": 5, "price": 15, "supplier": "Accessory Makers"},
                    {"name": "Cap", "category": "Accessories", "cost": 3, "price": 12, "supplier": "Headwear Co"},
                    {"name": "Socks Pack", "category": "Clothing", "cost": 2, "price": 8, "supplier": "Sock Factory"},
                    {"name": "Scarf", "category": "Accessories", "cost": 4, "price": 14, "supplier": "Accessory Makers"},
                    {"name": "Sunglasses", "category": "Accessories", "cost": 6, "price": 20, "supplier": "Vision Wear"},
                ]

            # Create products
            created_products = []
            for i, product_data in enumerate(products_data):
                product = Product(
                    owner_id=user.id,
                    name=product_data["name"],
                    category=product_data["category"],
                    cost_price=product_data["cost"],
                    selling_price=product_data["price"],
                    quantity=random.randint(20, 100),
                    supplier=product_data["supplier"],
                    sku=f"SKU-{user.id}-{i+1:04d}",
                    description=f"High quality {product_data['name'].lower()}",
                )
                db.add(product)
                db.flush()
                created_products.append(product)

            # Create customers
            customer_names = [
                "Thabo Molefe", "Lerato Nkosi", "Sipho Zulu", "Nomsa Khumalo", "Jabu Mthembu",
                "Zinhle Ndlovu", "Themba Sithole", "Ayanda Cele", "Sibusiso Nkosi", "Nomvula Dlamini",
                "Bongani Nkosi", "Thandiwe Mkhize", "Sifiso Buthelezi", "Zanele Nkosi", "Mthokozisi Mthembu",
                "Nokuthula Zulu", "Sandile Nkosi", "Phumzile Mthembu", "Thulani Nkosi", "Ntombifuthi Dlamini"
            ]

            created_customers = []
            for name in customer_names:
                customer = Customer(
                    owner_id=user.id,
                    name=name,
                    email=f"{name.lower().replace(' ', '.')}@gmail.com",
                    phone=f"27{random.randint(60, 89)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
                )
                db.add(customer)
                db.flush()
                created_customers.append(customer)

            # Create locations (Limpopo, South Africa regions)
            locations_data = [
                {"name": "Polokwane Central", "lat": -23.8962, "lon": 29.4486, "region": "Polokwane"},
                {"name": "Thohoyandou Mall", "lat": -22.9456, "lon": 30.4848, "region": "Thohoyandou"},
                {"name": "Tzaneen Market", "lat": -23.8332, "lon": 30.1596, "region": "Tzaneen"},
                {"name": "Phalaborwa Gateway", "lat": -23.9420, "lon": 31.1411, "region": "Phalaborwa"},
                {"name": "Mokopane Plaza", "lat": -24.1833, "lon": 29.0167, "region": "Mokopane"},
                {"name": "Louis Trichardt Centre", "lat": -23.0439, "lon": 29.9032, "region": "Louis Trichardt"},
                {"name": "Musina Border Post", "lat": -22.3486, "lon": 30.0417, "region": "Musina"},
                {"name": "Lephalale Mall", "lat": -23.6667, "lon": 27.7500, "region": "Lephalale"},
                {"name": "Giyani Shopping Centre", "lat": -23.2833, "lon": 30.7167, "region": "Giyani"},
                {"name": "Lebowakgomo Plaza", "lat": -24.2000, "lon": 29.5000, "region": "Lebowakgomo"},
                {"name": "Modjadjiskloof Market", "lat": -23.6833, "lon": 30.1333, "region": "Modjadjiskloof"},
                {"name": "Burgersfort Centre", "lat": -24.6833, "lon": 30.3333, "region": "Burgersfort"},
                {"name": "Steelpoort Mall", "lat": -24.7333, "lon": 30.2000, "region": "Steelpoort"},
                {"name": "Hoedspruit Gateway", "lat": -24.3500, "lon": 30.9667, "region": "Hoedspruit"},
                {"name": "Graskop Plaza", "lat": -24.9333, "lon": 30.8333, "region": "Graskop"},
            ]

            created_locations = []
            for location_data in locations_data:
                location = Location(
                    owner_id=user.id,
                    name=location_data["name"],
                    latitude=location_data["lat"],
                    longitude=location_data["lon"],
                    region=location_data["region"],
                    description=f"Sales location in {location_data['region']}, Limpopo"
                )
                db.add(location)
                db.flush()
                created_locations.append(location)

            db.commit()

            # Generate historical sales data (365 days)
            today = date.today()

            for days_back in range(365, 0, -1):
                sale_date = today - timedelta(days=days_back)

                # Generate 3-12 sales per day with higher sales on weekends
                day_of_week = sale_date.weekday()
                num_sales = 12 if day_of_week >= 4 else random.randint(5, 10)

                for _ in range(num_sales):
                    # Random time during business hours
                    hour = random.randint(9, 20)
                    minute = random.randint(0, 59)
                    sale_datetime = datetime.combine(sale_date, datetime.min.time()).replace(hour=hour, minute=minute)

                    # Create sale
                    customer = random.choice(created_customers)
                    location = random.choice(created_locations)

                    num_items = random.randint(1, 4)
                    selected_products = random.sample(created_products, min(num_items, len(created_products)))

                    total_amount = 0
                    total_cost = 0
                    sale_items_list = []

                    for product in selected_products:
                        quantity = random.randint(1, 3)
                        unit_price = product.selling_price
                        cost_price = product.cost_price
                        subtotal = quantity * unit_price

                        total_amount += subtotal
                        total_cost += quantity * cost_price

                        sale_items_list.append({
                            "product": product,
                            "quantity": quantity,
                            "unit_price": unit_price,
                            "cost_price": cost_price,
                            "subtotal": subtotal
                        })

                    profit = total_amount - total_cost

                    sale = Sale(
                        owner_id=user.id,
                        customer_id=customer.id,
                        location_id=location.id,
                        total_amount=total_amount,
                        total_cost=total_cost,
                        profit=profit,
                        payment_method=random.choice(["cash", "card", "mobile"]),
                        notes=None,
                        created_at=sale_datetime
                    )

                    db.add(sale)
                    db.flush()

                    # Add sale items
                    for item in sale_items_list:
                        sales_item = SalesItem(
                            sale_id=sale.id,
                            product_id=item["product"].id,
                            quantity=item["quantity"],
                            unit_price=item["unit_price"],
                            cost_price=item["cost_price"],
                            subtotal=item["subtotal"]
                        )
                        db.add(sales_item)

                    # Update customer stats
                    customer.total_purchases += total_amount
                    customer.visit_count += 1

                    # Update location stats
                    location.total_sales += total_amount

                db.commit()

            # Generate analytics records
            for days_back in range(365, 0, -1):
                current_date = today - timedelta(days=days_back)

                # Calculate daily metrics
                daily_sales = db.query(Sale).filter(
                    (Sale.owner_id == user.id) &
                    (Sale.created_at >= datetime.combine(current_date, datetime.min.time())) &
                    (Sale.created_at < datetime.combine(current_date + timedelta(days=1), datetime.min.time()))
                ).all()

                if daily_sales:
                    total_sales = sum(s.total_amount for s in daily_sales)
                    total_profit = sum(s.profit for s in daily_sales)

                    analytics = Analytics(
                        owner_id=user.id,
                        date=current_date,
                        total_sales=total_sales,
                        total_profit=total_profit,
                        total_revenue=total_sales,
                        transaction_count=len(daily_sales),
                        average_transaction=total_sales / len(daily_sales),
                        period_type="daily"
                    )
                    db.add(analytics)

            db.commit()

            print(f"✓ Demo data seeded successfully for {user.username}!")
            print(f"✓ Created {len(created_products)} products")
            print(f"✓ Created {len(created_customers)} customers")
            print(f"✓ Created {len(created_locations)} locations")
            print(f"✓ Generated 365 days of sales history")

    except Exception as e:
        db.rollback()
        print(f"Error seeding demo data: {e}")
        raise
    finally:
        db.close()