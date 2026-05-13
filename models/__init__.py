"""
Database models for the business management system
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """User model for authentication and business ownership"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    business_name = Column(String, nullable=False)
    business_type = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    products = relationship("Product", back_populates="owner")
    sales = relationship("Sale", back_populates="owner")
    customers = relationship("Customer", back_populates="owner")
    locations = relationship("BusinessLocation", back_populates="owner")
    analytics = relationship("Analytics", back_populates="owner")
    predictions = relationship("Prediction", back_populates="owner")
    insights = relationship("BusinessInsight", back_populates="owner")
    sales_analytics = relationship("SalesAnalytics", back_populates="owner")
    product_trends = relationship("ProductTrend", back_populates="owner")
    area_statistics = relationship("AreaStatistic", back_populates="owner")
    ai_insights = relationship("AIInsight", back_populates="owner")


class Product(Base):
    """Product model for inventory management"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    supplier = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    sku = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="products")
    sales_items = relationship("SalesItem", back_populates="product")


class Sale(Base):
    """Sale transaction model"""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("business_locations.id"), nullable=True)
    total_amount = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)
    payment_method = Column(String, default="cash")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    location = relationship("BusinessLocation", back_populates="sales")
    items = relationship("SalesItem", back_populates="sale")


class SalesItem(Base):
    """Individual items in a sale transaction"""
    __tablename__ = "sales_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relationships
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sales_items")


class Customer(Base):
    """Customer model for tracking buying patterns"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    total_purchases = Column(Float, default=0)
    visit_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="customers")
    sales = relationship("Sale", back_populates="customer")


class BusinessLocation(Base):
    """Business-specific geographic location and address metadata"""
    __tablename__ = "business_locations"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    formatted_address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    province_state = Column(String, nullable=True)
    region = Column(String, nullable=True)
    total_sales = Column(Float, default=0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="locations")
    sales = relationship("Sale", back_populates="location")


Location = BusinessLocation


class Analytics(Base):
    """Pre-calculated analytics data"""
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    total_sales = Column(Float, default=0)
    total_profit = Column(Float, default=0)
    total_revenue = Column(Float, default=0)
    transaction_count = Column(Integer, default=0)
    average_transaction = Column(Float, default=0)
    top_product_id = Column(Integer, nullable=True)
    worst_product_id = Column(Integer, nullable=True)
    period_type = Column(String, nullable=False)  # 'daily', 'weekly', 'monthly'
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="analytics")


class Prediction(Base):
    """ML predictions for business insights"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prediction_type = Column(String, nullable=False)  # 'sales', 'demand', 'profit', 'growth'
    target_id = Column(Integer, nullable=True)  # product_id if product-specific
    predicted_value = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    time_period = Column(String, nullable=True)  # 'next_week', 'next_month', 'next_quarter'
    additional_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="predictions")


class BusinessInsight(Base):
    """AI-generated business insights"""
    __tablename__ = "business_insights"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    insight_type = Column(String, nullable=False)  # 'pricing', 'inventory', 'sales', 'growth'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=True)
    impact_potential = Column(String, nullable=True)  # 'high', 'medium', 'low'
    additional_data = Column(JSON, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="insights")


class AIInsight(Base):
    """Public AI insight summary data"""
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    confidence_score = Column(Float, default=0.0)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="ai_insights")


class SalesAnalytics(Base):
    """Sales analytics records for area and business performance"""
    __tablename__ = "sales_analytics"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("business_locations.id"), nullable=True)
    date = Column(Date, nullable=False)
    total_sales = Column(Float, default=0)
    total_profit = Column(Float, default=0)
    transaction_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="sales_analytics")


class ProductTrend(Base):
    """Product and category trend metadata"""
    __tablename__ = "product_trends"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, nullable=True)
    category = Column(String, nullable=True)
    trend_score = Column(Float, default=0)
    demand_index = Column(Float, default=0)
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="product_trends")


class AreaStatistic(Base):
    """Geographic area statistics for map analytics"""
    __tablename__ = "area_statistics"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("business_locations.id"), nullable=True)
    area_name = Column(String, nullable=False)
    sales_density = Column(Float, default=0)
    demand_score = Column(Float, default=0)
    popularity_score = Column(Float, default=0)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="area_statistics")
