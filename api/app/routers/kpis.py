import re
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query
from collections import Counter

from ..db.prospects import get_prospects_collection
from ..models.kpis import KPIsResponse, KPISummary, KPIDistribution, FollowersByNetwork

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/kpis", tags=["kpis"])


# Helper function to build MongoDB filters
def _build_mongodb_filters(
    nom: Optional[str] = None,
    type_prospect: Optional[str] = None,
    region: Optional[str] = None,
    departement: Optional[str] = None,
    statut: Optional[str] = None,
    accepte_contact: Optional[bool] = None,
    email: Optional[bool] = None,
    telephone: Optional[bool] = None,
    sit_web: Optional[bool] = None,
    min_nb_aderents: Optional[int] = None,
    max_nb_aderents: Optional[int] = None,
    min_followers_total: Optional[int] = None,
    max_followers_total: Optional[int] = None,
) -> Dict[str, Any]:
    """Build MongoDB filter from query parameters."""
    match: Dict[str, Any] = {}

    if nom:
        pattern = re.escape(nom.strip())
        match["nom_structure"] = {"$regex": pattern, "$options": "i"}

    if type_prospect is not None:
        match["type_prospect"] = type_prospect

    if region is not None:
        match["region"] = region

    if departement is not None:
        match["departement"] = departement

    if statut is not None:
        match["statut"] = statut

    if accepte_contact is not None:
        match["accepte_contact"] = accepte_contact

    def _present(field: str) -> Dict[str, Any]:
        return {field: {"$exists": True, "$type": "string", "$ne": ""}}

    def _missing(field: str) -> Dict[str, Any]:
        return {"$or": [
            {field: {"$exists": False}},
            {field: None},
            {field: ""},
        ]}

    if email is True:
        match.update(_present("email"))
    elif email is False:
        match["$and"] = match.get("$and", [])
        match["$and"].append(_missing("email"))

    if telephone is True:
        match.update(_present("telephone"))
    elif telephone is False:
        match["$and"] = match.get("$and", [])
        match["$and"].append(_missing("telephone"))

    if sit_web is True:
        match.update(_present("sit_web"))
    elif sit_web is False:
        match["$and"] = match.get("$and", [])
        match["$and"].append(_missing("sit_web"))

    if min_nb_aderents is not None or max_nb_aderents is not None:
        match["nb_aderents"] = {}
        if min_nb_aderents is not None:
            match["nb_aderents"]["$gte"] = min_nb_aderents
        if max_nb_aderents is not None:
            match["nb_aderents"]["$lte"] = max_nb_aderents

    return match


def _calculate_histogram_bins(data: List[float], bins: int = 10) -> List[int]:
    # On calcule les bins de l'histo
    if not data:
        return []
    
    min_val = min(data)
    max_val = max(data)
    
    if min_val == max_val:
        return [len(data)]
    
    
    bin_width = (max_val - min_val) / bins
    bin_counts = [0] * bins
    
    for val in data:
        if val == max_val:
            bin_idx = bins - 1
        else:
            bin_idx = int((val - min_val) / bin_width)
            bin_idx = min(bin_idx, bins - 1)
        
        bin_counts[bin_idx] += 1
    
    return bin_counts


@router.get("/prospects", response_model=KPIsResponse)
async def get_prospects_kpis(
    # Search filters
    nom: Optional[str] = Query(default=None),
    type_prospect: Optional[str] = Query(default=None),
    region: Optional[str] = Query(default=None),
    departement: Optional[str] = Query(default=None),
    statut: Optional[str] = Query(default=None),
    accepte_contact: Optional[bool] = Query(default=None),
    email: Optional[bool] = Query(default=None),
    telephone: Optional[bool] = Query(default=None),
    sit_web: Optional[bool] = Query(default=None),
    min_nb_aderents: Optional[int] = Query(default=None, ge=0),
    max_nb_aderents: Optional[int] = Query(default=None, ge=0),
    min_followers_total: Optional[int] = Query(default=None, ge=0),
    max_followers_total: Optional[int] = Query(default=None, ge=0),
):

    # Calcule les KPIs pour les prospects en fonction des filtres de recherche
    try:
        col = get_prospects_collection()

        # Build filters
        match = _build_mongodb_filters(
            nom=nom,
            type_prospect=type_prospect,
            region=region,
            departement=departement,
            statut=statut,
            accepte_contact=accepte_contact,
            email=email,
            telephone=telephone,
            sit_web=sit_web,
            min_nb_aderents=min_nb_aderents,
            max_nb_aderents=max_nb_aderents,
            min_followers_total=min_followers_total,
            max_followers_total=max_followers_total,
        )

        # Pipeline pour récupérer les prospects matchant les critères
        pipeline: List[Dict[str, Any]] = [
            {
                "$addFields": {
                    "followers_total": {
                        "$max": [
                            {"$ifNull": ["$facebook_followers", 0]},
                            {"$ifNull": ["$x_followers", 0]},
                            {"$ifNull": ["$instagram_followers", 0]},
                            {"$ifNull": ["$youtube_followers", 0]},
                            {"$ifNull": ["$tictok_followers", 0]},
                        ]
                    }
                }
            }
        ]

        if min_followers_total is not None or max_followers_total is not None:
            match["followers_total"] = {}

        if min_followers_total is not None:
            match["followers_total"]["$gte"] = min_followers_total

        if max_followers_total is not None:
            match["followers_total"]["$lte"] = max_followers_total

        # on ajoute le match à la pipeline
        pipeline.append({"$match": match})

        # On récup les prospects correspondant aux criètres
        cursor = col.aggregate(pipeline)

        prospects = []
        async for doc in cursor:
            prospects.append(doc)


        total_count = len(prospects)

        # ========== SUM CALCULS ==========
        total_adherents = sum(p.get("nb_aderents", 0) or 0 for p in prospects)
        
        # total followers
        total_followers = sum(p.get("followers_total", 0) for p in prospects)
        
        accepte_contact_count = sum(1 for p in prospects if p.get("accepte_contact") is True)
        non_contactes_count = sum(1 for p in prospects if p.get("contacte") is False or p.get("contacte") is None)
        tel_manquants_count = sum(1 for p in prospects if not p.get("telephone"))
        mail_manquants_count = sum(1 for p in prospects if not p.get("email"))

        summary = KPISummary(
            total_prospects=total_count,
            total_adherents=total_adherents,
            total_followers=total_followers,
            total_accepte_contact=accepte_contact_count,
            total_non_contactes=non_contactes_count,
            total_tel_manquants=tel_manquants_count,
            total_mail_manquants=mail_manquants_count,
        )

        # ========== TYPE PROSPECT DISTRIBUTION ==========
        type_prospect_counter = Counter(p.get("type_prospect") for p in prospects if p.get("type_prospect"))
        type_prospect_labels = [t for t, _ in type_prospect_counter.most_common()]
        type_prospect_values = [type_prospect_counter[t] for t in type_prospect_labels]
        type_prospect_total = sum(type_prospect_values)
        type_prospect_percentages = [
            (v / type_prospect_total * 100) if type_prospect_total > 0 else 0
            for v in type_prospect_values
        ]

        type_prospect_dist = KPIDistribution(
            labels=type_prospect_labels,
            values=type_prospect_values,
            percentages=type_prospect_percentages,
        )

        # ========== STATUT DISTRIBUTION ==========
        statut_counter = Counter(p.get("statut") for p in prospects if p.get("statut"))
        statut_labels = [s for s, _ in statut_counter.most_common()]
        statut_values = [statut_counter[s] for s in statut_labels]
        statut_total = sum(statut_values)
        statut_percentages = [
            (v / statut_total * 100) if statut_total > 0 else 0
            for v in statut_values
        ]

        statut_dist = KPIDistribution(
            labels=statut_labels,
            values=statut_values,
            percentages=statut_percentages,
        )

        # ========== ADHERENTS DISTRIBUTION (histogram bins) ==========
        adherents_list = [p.get("nb_aderents", 0) or 0 for p in prospects]
        adherents_distribution = _calculate_histogram_bins(adherents_list, bins=10)

        # ========== FOLLOWERS DISTRIBUTION (histogram bins) ==========
        followers_list = [p.get("followers_total", 0) for p in prospects]
        followers_distribution = _calculate_histogram_bins(followers_list, bins=10)

        # ========== WEBSITE DATA ==========
        website_with = sum(1 for p in prospects if p.get("sit_web") and str(p.get("sit_web")).strip() != "")
        website_without = total_count - website_with

        # ========== FOLLOWERS BY NETWORK ==========
        facebook_total = sum(p.get("facebook_followers", 0) or 0 for p in prospects)
        twitter_total = sum(p.get("x_followers", 0) or 0 for p in prospects)
        instagram_total = sum(p.get("instagram_followers", 0) or 0 for p in prospects)
        youtube_total = sum(p.get("youtube_followers", 0) or 0 for p in prospects)
        tiktok_total = sum(p.get("tictok_followers", 0) or 0 for p in prospects)

        followers_by_network = FollowersByNetwork(
            facebook=facebook_total,
            twitter=twitter_total,
            instagram=instagram_total,
            youtube=youtube_total,
            tiktok=tiktok_total,
        )

        # ========== PERCENTAGES FOR GAUGES ==========
        acceptance_percentage = (accepte_contact_count / total_count) if total_count > 0 else 0
        non_contactes_percentage = (non_contactes_count / total_count) if total_count > 0 else 0
        tel_manquants_percentage = (tel_manquants_count / total_count) if total_count > 0 else 0
        mail_manquants_percentage = (mail_manquants_count / total_count) if total_count > 0 else 0

    # ========== RETURN ALL KPIs ==========
        return KPIsResponse(
            summary=summary,
            type_prospect_dist=type_prospect_dist,
            statut_dist=statut_dist,
            adherents_distribution=adherents_distribution,
            followers_distribution=followers_distribution,
            website_with=website_with,
            website_without=website_without,
            followers_by_network=followers_by_network,
            acceptance_percentage=acceptance_percentage,
            non_contactes_percentage=non_contactes_percentage,
            tel_manquants_percentage=tel_manquants_percentage,
            mail_manquants_percentage=mail_manquants_percentage,
        )
    except Exception as e:
        logger.error(f"Error calculating KPIs: {str(e)}", exc_info=True)
        raise
