from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

ETA_MODEL_PATH = MODEL_DIR / "estimated_delivery_time_model.pkl"
LATE_MODEL_PATH = MODEL_DIR / "late_delivery_model_no_eta.pkl"

app = FastAPI(title="Food Delivery Predictor")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

eta_model = joblib.load(ETA_MODEL_PATH)
late_model = joblib.load(LATE_MODEL_PATH)

CITIES = ["City_A", "City_B", "City_C", "City_D"]

AREAS_BY_CITY = {
    "City_A": [
        "City_A_Area_1", "City_A_Area_2", "City_A_Area_3", "City_A_Area_4", "City_A_Area_5",
        "City_A_Area_6", "City_A_Area_7", "City_A_Area_8", "City_A_Area_9", "City_A_Area_10",
    ],
    "City_B": [
        "City_B_Area_1", "City_B_Area_2", "City_B_Area_3", "City_B_Area_4", "City_B_Area_5",
        "City_B_Area_6", "City_B_Area_7", "City_B_Area_8", "City_B_Area_9", "City_B_Area_10",
    ],
    "City_C": [
        "City_C_Area_1", "City_C_Area_2", "City_C_Area_3", "City_C_Area_4", "City_C_Area_5",
        "City_C_Area_6", "City_C_Area_7", "City_C_Area_8", "City_C_Area_9", "City_C_Area_10",
    ],
    "City_D": [
        "City_D_Area_1", "City_D_Area_2", "City_D_Area_3", "City_D_Area_4", "City_D_Area_5",
        "City_D_Area_6", "City_D_Area_7", "City_D_Area_8", "City_D_Area_9", "City_D_Area_10",
    ],
}

DAY_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
CUSTOMER_TYPES = ["New", "Premium", "Regular"]
RESTAURANT_TYPES = ["Cafe", "Casual Dining", "Fast Food", "Fine Dining"]
PRIMARY_CATEGORIES = ["Asian", "Burger", "Dessert", "Healthy", "Local", "Pizza"]
PAYMENT_METHODS = ["Cash", "Credit Card", "Digital Wallet"]
WEATHER = ["Clear", "Cloudy", "Rain", "Storm"]
TRAFFIC = ["High", "Low", "Medium"]

FEATURES = [
    "order_hour",
    "day_of_week",
    "is_weekend",
    "city",
    "delivery_area",
    "customer_age",
    "customer_type",
    "restaurant_type",
    "restaurant_primary_category",
    "restaurant_rating",
    "items_count",
    "subtotal",
    "discount_percent",
    "tax_amount",
    "service_fee",
    "delivery_fee",
    "order_total",
    "payment_method",
    "tip_amount",
    "distance_km",
    "weather",
    "traffic_level",
    "delivery_partner_experience_months",
    "delivery_partner_rating",
    "restaurant_preparation_time_minutes",
    "order_year",
    "order_month",
    "order_day",
    "order_weekofyear",
]


def must_be(field_name: str, value: str, allowed_values: list[str]) -> str:
    if value not in allowed_values:
        raise HTTPException(status_code=400, detail=f"Invalid value for {field_name}")
    return value


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": None,
            "cities": CITIES,
            "areas_by_city": AREAS_BY_CITY,
            "day_of_week_list": DAY_OF_WEEK,
            "customer_types": CUSTOMER_TYPES,
            "restaurant_types": RESTAURANT_TYPES,
            "primary_categories": PRIMARY_CATEGORIES,
            "payment_methods": PAYMENT_METHODS,
            "weather_list": WEATHER,
            "traffic_list": TRAFFIC,
        },
    )


@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    order_hour: int = Form(...),
    day_of_week: str = Form(...),
    is_weekend: int = Form(...),
    city: str = Form(...),
    delivery_area: str = Form(...),
    customer_age: int = Form(...),
    customer_type: str = Form(...),
    restaurant_type: str = Form(...),
    restaurant_primary_category: str = Form(...),
    restaurant_rating: float = Form(...),
    items_count: int = Form(...),
    subtotal: float = Form(...),
    discount_percent: float = Form(...),
    tax_amount: float = Form(...),
    service_fee: float = Form(...),
    delivery_fee: float = Form(...),
    order_total: float = Form(...),
    payment_method: str = Form(...),
    tip_amount: float = Form(...),
    distance_km: float = Form(...),
    weather: str = Form(...),
    traffic_level: str = Form(...),
    delivery_partner_experience_months: int = Form(...),
    delivery_partner_rating: float = Form(...),
    restaurant_preparation_time_minutes: int = Form(...),
    order_year: int = Form(...),
    order_month: int = Form(...),
    order_day: int = Form(...),
    order_weekofyear: int = Form(...),
):
    day_of_week = must_be("day_of_week", day_of_week, DAY_OF_WEEK)
    city = must_be("city", city, CITIES)
    delivery_area = must_be("delivery_area", delivery_area, AREAS_BY_CITY[city])
    customer_type = must_be("customer_type", customer_type, CUSTOMER_TYPES)
    restaurant_type = must_be("restaurant_type", restaurant_type, RESTAURANT_TYPES)
    restaurant_primary_category = must_be(
        "restaurant_primary_category", restaurant_primary_category, PRIMARY_CATEGORIES
    )
    payment_method = must_be("payment_method", payment_method, PAYMENT_METHODS)
    weather = must_be("weather", weather, WEATHER)
    traffic_level = must_be("traffic_level", traffic_level, TRAFFIC)

    row = pd.DataFrame([{
        "order_hour": order_hour,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "city": city,
        "delivery_area": delivery_area,
        "customer_age": customer_age,
        "customer_type": customer_type,
        "restaurant_type": restaurant_type,
        "restaurant_primary_category": restaurant_primary_category,
        "restaurant_rating": restaurant_rating,
        "items_count": items_count,
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "tax_amount": tax_amount,
        "service_fee": service_fee,
        "delivery_fee": delivery_fee,
        "order_total": order_total,
        "payment_method": payment_method,
        "tip_amount": tip_amount,
        "distance_km": distance_km,
        "weather": weather,
        "traffic_level": traffic_level,
        "delivery_partner_experience_months": delivery_partner_experience_months,
        "delivery_partner_rating": delivery_partner_rating,
        "restaurant_preparation_time_minutes": restaurant_preparation_time_minutes,
        "order_year": order_year,
        "order_month": order_month,
        "order_day": order_day,
        "order_weekofyear": order_weekofyear,
    }])

    eta_pred = float(eta_model.predict(row)[0])
    late_prob = float(late_model.predict_proba(row)[0, 1])
    late_pred = "Late" if late_prob >= 0.5 else "Not Late"

    result = {
        "eta": round(eta_pred, 2),
        "late_prob": round(late_prob, 4),
        "late_pred": late_pred,
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": result,
            "eta": result["eta"],
            "late_prob": result["late_prob"],
            "late_pred": result["late_pred"],
            "cities": CITIES,
            "areas_by_city": AREAS_BY_CITY,
            "day_of_week_list": DAY_OF_WEEK,
            "customer_types": CUSTOMER_TYPES,
            "restaurant_types": RESTAURANT_TYPES,
            "primary_categories": PRIMARY_CATEGORIES,
            "payment_methods": PAYMENT_METHODS,
            "weather_list": WEATHER,
            "traffic_list": TRAFFIC,
        },
    )