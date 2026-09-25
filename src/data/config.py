# Reproducibility
RANDOM_SEED = 42

# Dataset size
NUM_CUSTOMERS = 1000
NUM_LEADS = 2000

# Simulation period
START_DATE = "2026-01-01"
END_DATE = "2026-04-30"

# Customer plans
PLANS = [
    "Free",
    "Starter",
    "Business",
]

# Countries
COUNTRIES = [
    "India",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
    "Singapore",
]

# Industries
INDUSTRIES = [
    "SaaS",
    "FinTech",
    "E-commerce",
    "Healthcare",
    "Education",
    "Marketing",
    "IT Services",
    "Professional Services",
]

# Acquisition channels
ACQUISITION_CHANNELS = [
    "Organic",
    "Paid Ads",
    "Referral",
    "Partner",
    "Sales",
]

# Product events
EVENT_TYPES = [
    "login",
    "feature_used",
    "report_created",
    "integration_connected",
    "integration_failed",
    "team_member_invited",
    "dashboard_viewed",
]

# Product features
FEATURES = [
    "dashboard",
    "reports",
    "integrations",
    "team_management",
    "analytics",
]

# Customer distribution weights
COUNTRY_WEIGHTS = {
    "India": 40,
    "United States": 25,
    "United Kingdom": 10,
    "Canada": 8,
    "Australia": 7,
    "Germany": 6,
    "Singapore": 4,
}

INDUSTRY_WEIGHTS = {
    "SaaS": 20,
    "FinTech": 15,
    "E-commerce": 15,
    "Healthcare": 10,
    "Education": 10,
    "Marketing": 10,
    "IT Services": 12,
    "Professional Services": 8,
}

ACQUISITION_CHANNEL_WEIGHTS = {
    "Organic": 30,
    "Paid Ads": 20,
    "Referral": 25,
    "Partner": 10,
    "Sales": 15,
}

# Baseline monthly activity event ranges by plan
PLAN_ACTIVITY_RANGES = {
    "Free": (20, 60),
    "Starter": (50, 120),
    "Business": (100, 250),
}

# Relative frequency of product events
EVENT_WEIGHTS = {
    "login": 30,
    "feature_used": 25,
    "report_created": 10,
    "integration_connected": 8,
    "integration_failed": 2,
    "team_member_invited": 5,
    "dashboard_viewed": 20,
}

# Monthly activity multipliers for customers affected by the
# simulated integration problem
AFFECTED_ACTIVITY_MULTIPLIERS = {
    1: 1.00,  # January
    2: 0.95,  # February
    3: 0.75,  # March
    4: 0.65,  # April
}

# Base probability of being affected by the simulated integration problem
AFFECTED_BASE_PROBABILITY = 0.20