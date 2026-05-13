from __future__ import annotations

"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Any


# ==================== User Schemas ====================
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    business_name: str
    business_type: Optional[str] = None
    location: Optional['LocationCreate'] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    business_name: str
    business_type: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# ==================== Product Schemas ====================
class ProductCreate(BaseModel):
    name: str
    category: str
    cost_price: float
    selling_price: float
    quantity: int = 0
    supplier: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    quantity: Optional[int] = None
    supplier: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    cost_price: float
    selling_price: float
    quantity: int
    supplier: Optional[str]
    sku: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Sale Schemas ====================
class SalesItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    location_id: Optional[int] = None
    items: List[SalesItemCreate]
    payment_method: str = "cash"
    notes: Optional[str] = None


class SalesItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    cost_price: float
    subtotal: float

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    customer_id: Optional[int]
    location_id: Optional[int]
    total_amount: float
    total_cost: float
    profit: float
    payment_method: str
    notes: Optional[str]
    items: List[SalesItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Customer Schemas ====================
class CustomerCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    total_purchases: float
    visit_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Location Schemas ====================
class LocationCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    formatted_address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    formatted_address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None


class LocationResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    formatted_address: Optional[str]
    city: Optional[str]
    province_state: Optional[str]
    region: Optional[str]
    total_sales: float
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Analytics Schemas ====================
class AnalyticsResponse(BaseModel):
    id: int
    date: str
    total_sales: float
    total_profit: float
    total_revenue: float
    transaction_count: int
    average_transaction: float
    period_type: str

    class Config:
        from_attributes = True


class DashboardMetrics(BaseModel):
    total_sales: float
    total_profit: float
    total_revenue: float
    profit_margin: float
    avg_transaction_value: float
    total_products: int
    low_stock_products: int
    top_products: List[dict]
    worst_products: List[dict]
    period: str


# ==================== Prediction Schemas ====================
class PredictionResponse(BaseModel):
    id: int
    prediction_type: str
    predicted_value: float
    confidence_score: float
    time_period: Optional[str]
    additional_data: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Insight Schemas ====================
class BusinessInsightResponse(BaseModel):
    id: int
    insight_type: str
    title: str
    description: str
    recommendation: Optional[str]
    impact_potential: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Error Schemas ====================
class ErrorResponse(BaseModel):
    error: str
    message: str


class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


UserRegister.update_forward_refs()
