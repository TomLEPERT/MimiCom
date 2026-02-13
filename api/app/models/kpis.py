from typing import Dict, List, Optional
from pydantic import BaseModel


class KPISummary(BaseModel):
    total_prospects: int
    total_adherents: int
    total_followers: int
    total_accepte_contact: int
    total_non_contactes: int
    total_tel_manquants: int
    total_mail_manquants: int


class KPIDistribution(BaseModel):
    """Distribution data for prospects (pie, bar charts, etc)."""
    labels: List[str]
    values: List[int]
    percentages: Optional[List[float]] = None


class FollowersByNetwork(BaseModel):
    """Followers distribution by social network."""
    facebook: int
    twitter: int
    instagram: int
    youtube: int
    tiktok: int


class KPIsResponse(BaseModel):
    """Complete KPIs response for dashboard."""
    # Summary metrics
    summary: KPISummary
    
    # Distributions
    type_prospect_dist: KPIDistribution
    statut_dist: KPIDistribution
    adherents_distribution: Optional[List[int]] = None
    followers_distribution: Optional[List[int]] = None
    
    # Website data
    website_with: int
    website_without: int
    
    # Followers by network
    followers_by_network: FollowersByNetwork
    
    # Percentages for gauges
    acceptance_percentage: float
    non_contactes_percentage: float
    tel_manquants_percentage: float
    mail_manquants_percentage: float
