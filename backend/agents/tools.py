
# backend/agents/tools.py
from typing import TypedDict, List, Optional, Protocol
from datetime import date

# --- Data Schemas for Tool Outputs ---
# TODO: R2 to refine these schemas as the backend APIs are built.

class RequestStatus(TypedDict):
    status: str
    created_date: date
    closed_date: Optional[date]
    category: str
    ward: int
    lat: float
    lon: float

class Prediction(TypedDict):
    eta_date: date
    eta_days: float
    ci_low: float  # Confidence interval lower bound (days)
    ci_high: float # Confidence interval upper bound (days)
    confidence: float # A score from 0 to 1
    top_factors: List[str] # SHAP factors

class EquityResult(TypedDict):
    area_median: float
    city_median: float
    delta_days: float
    n: int # Sample size
    significance: bool # Is the difference statistically significant?

class Hotspot(TypedDict):
    center: dict[str, float] # e.g., {"lat": 41.8, "lon": -87.6}
    count: int
    trend_7d: float # e.g., 1.2 (20% increase)
    trend_30d: float

class RefreshMeta(TypedDict):
    data_last_updated: date
    model_version: str
    feature_version: str

# --- Tool Interface Definition ---
# Using a Protocol to define the set of tools the agents can use.
# This allows for easy mocking and testing.

class AgentTools(Protocol):
    """Defines the interface for all tools available to the CHI-311 agents."""

    def get_request_status(self, sr_number: str) -> RequestStatus:
        """Retrieves the current status and details of a service request."""
        ...

    def predict_eta(self, sr_number: str) -> Prediction:
        """Predicts the estimated time to resolution for a service request."""
        ...

    def area_equity(self, area_name: str, area_type: str = 'ward', category: Optional[str] = None) -> EquityResult:
        """Calculates the equity metrics for a given area (ward or community)."""
        ...

    def hotspots(self, category: str, days: int = 30) -> List[Hotspot]:
        """Identifies spatial hotspots for a given category over a time window."""
        ...

    def refresh_meta(self) -> RefreshMeta:
        """Gets metadata about data freshness and model versions."""
        ...

# TODO: R2 to implement a concrete class that calls the FastAPI endpoints.
# Example:
# class ApiAgentTools(AgentTools):
#     def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
#         self.client = httpx.Client(base_url=base_url)
#
#     def get_request_status(self, sr_number: str) -> RequestStatus:
#         response = self.client.get(f"/request/{sr_number}")
#         response.raise_for_status()
#         return response.json()
#     ...
