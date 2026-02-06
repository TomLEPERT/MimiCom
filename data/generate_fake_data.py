# data/generate_fake_prospects_50k.py
import os
import random
from typing import Optional, Dict, Union, List

import pandas as pd
from faker import Faker

fake = Faker("fr_FR")

# ===============================
# CONFIG
# ===============================
NB_ROWS = 5000

# % de lignes AVEC email/tel qui deviennent des doublons CSV
DUP_EMAIL_RATE = 0.07   # 7%
DUP_TEL_RATE = 0.06     # 6%

# Présence des champs (pour rester réaliste)
EMAIL_PRESENT_RATE = 0.95
TEL_PRESENT_RATE = 0.90

OUT_PATH = "data/fake_prospects_dataset_5k.csv"

TYPES_ENUM = [
    "CSCS",
    "Bar à jeux",
    "Influenceur",
    "MJC",
    "Médiathèque",
    "Artisan",
    "Éditeur",
    "Asso JDR",
    "Boutique spécialisée",
    "Ludothèque",
]

# Département → (Région, Villes)
DEPARTEMENTS = {
    "16": ("Nouvelle-Aquitaine", ["Angoulême", "Cognac", "Confolens", "Barbezieux", "Blanzac", "Beigne", "Brossac"]),
    "17": ("Nouvelle-Aquitaine", ["La Rochelle", "Rochefort", "St Jean d'Angely", "Saint", "Jonzac"]),
    "79": ("Nouvelle-Aquitaine", ["Niort", "Bressuire", "Parthenay"]),
    "86": ("Nouvelle-Aquitaine", ["Poitiers", "Montmorillon", "Châtellerault"]),
    "19": ("Nouvelle-Aquitaine", ["Brive-la-Gaillarde", "Tulle", "Ussel"]),
    "23": ("Nouvelle-Aquitaine", ["Guéret", "Aubusson", "La Souterraine"]),
    "87": ("Nouvelle-Aquitaine", ["Limoges", "Saint-Junien", "Bellac"]),
    "24": ("Nouvelle-Aquitaine", ["Périgueux", "Bergerac", "Sarlat-la-Canéda"]),
    "47": ("Nouvelle-Aquitaine", ["Agen", "Villeneuve-sur-Lot", "Marmande"]),
    "33": ("Nouvelle-Aquitaine", ["Bordeaux", "Mérignac", "Libourne"]),
    "40": ("Nouvelle-Aquitaine", ["Mont-de-Marsan", "Dax", "Capbreton"]),
    "64": ("Nouvelle-Aquitaine", ["Pau", "Bayonne", "Biarritz"]),
    "09": ("Occitanie", ["Foix", "Pamiers", "Saint-Girons"]),
    "11": ("Occitanie", ["Carcassonne", "Narbonne", "Castelnaudary"]),
    "12": ("Occitanie", ["Rodez", "Millau", "Villefranche-de-Rouergue"]),
    "30": ("Occitanie", ["Nîmes", "Alès", "Bagnols-sur-Cèze"]),
    "31": ("Occitanie", ["Toulouse", "Muret", "Saint-Gaudens"]),
    "32": ("Occitanie", ["Auch", "Condom", "Mirande"]),
    "34": ("Occitanie", ["Montpellier", "Béziers", "Sète"]),
    "46": ("Occitanie", ["Cahors", "Figeac", "Gourdon"]),
    "48": ("Occitanie", ["Mende", "Florac", "Langogne"]),
    "65": ("Occitanie", ["Tarbes", "Lourdes", "Bagnères-de-Bigorre"]),
    "66": ("Occitanie", ["Perpignan", "Céret", "Prades"]),
    "81": ("Occitanie", ["Albi", "Castres", "Gaillac"]),
    "82": ("Occitanie", ["Montauban", "Moissac", "Castelsarrasin"]),
    "44": ("Pays de la Loire", ["Nantes", "Saint-Nazaire", "Rezé"]),
    "49": ("Pays de la Loire", ["Angers", "Cholet", "Saumur"]),
    "53": ("Pays de la Loire", ["Laval", "Mayenne", "Château-Gontier"]),
    "72": ("Pays de la Loire", ["Le Mans", "La Flèche", "Sablé-sur-Sarthe"]),
    "85": ("Pays de la Loire", ["La Roche-sur-Yon", "Les Sables-d’Olonne", "Fontenay-le-Comte"]),
    "18": ("Centre-Val de Loire", ["Bourges", "Vierzon", "Saint-Amand-Montrond"]),
    "28": ("Centre-Val de Loire", ["Chartres", "Dreux", "Châteaudun"]),
    "36": ("Centre-Val de Loire", ["Châteauroux", "Issoudun", "Le Blanc"]),
    "37": ("Centre-Val de Loire", ["Tours", "Loches", "Chinon"]),
    "41": ("Centre-Val de Loire", ["Blois", "Vendôme", "Romorantin-Lanthenay"]),
    "45": ("Centre-Val de Loire", ["Orléans", "Montargis", "Gien"]),
    "01": ("Auvergne-Rhône-Alpes", ["Bourg-en-Bresse", "Oyonnax", "Bellegarde-sur-Valserine"]),
    "03": ("Auvergne-Rhône-Alpes", ["Moulins", "Vichy", "Montluçon"]),
    "07": ("Auvergne-Rhône-Alpes", ["Privas", "Annonay", "Aubenas"]),
    "15": ("Auvergne-Rhône-Alpes", ["Aurillac", "Saint-Flour", "Mauriac"]),
    "26": ("Auvergne-Rhône-Alpes", ["Valence", "Montélimar", "Romans-sur-Isère"]),
    "38": ("Auvergne-Rhône-Alpes", ["Grenoble", "Vienne", "Bourgoin-Jallieu"]),
    "42": ("Auvergne-Rhône-Alpes", ["Saint-Étienne", "Roanne", "Montbrison"]),
    "43": ("Auvergne-Rhône-Alpes", ["Le Puy-en-Velay", "Yssingeaux", "Brioude"]),
    "63": ("Auvergne-Rhône-Alpes", ["Clermont-Ferrand", "Riom", "Issoire"]),
    "69": ("Auvergne-Rhône-Alpes", ["Lyon", "Villefranche-sur-Saône", "Vénissieux"]),
    "73": ("Auvergne-Rhône-Alpes", ["Chambéry", "Albertville", "Aix-les-Bains"]),
    "74": ("Auvergne-Rhône-Alpes", ["Annecy", "Thonon-les-Bains", "Cluses"]),
    "04": ("Provence-Alpes-Côte d'Azur", ["Digne-les-Bains", "Manosque", "Sisteron"]),
    "05": ("Provence-Alpes-Côte d'Azur", ["Gap", "Briançon", "Embrun"]),
    "06": ("Provence-Alpes-Côte d'Azur", ["Nice", "Cannes", "Antibes"]),
    "13": ("Provence-Alpes-Côte d'Azur", ["Marseille", "Aix-en-Provence", "Arles"]),
    "83": ("Provence-Alpes-Côte d'Azur", ["Toulon", "Draguignan", "Hyères"]),
    "84": ("Provence-Alpes-Côte d'Azur", ["Avignon", "Carpentras", "Orange"]),
    "2A": ("Corse", ["Ajaccio", "Sartène", "Porto-Vecchio"]),
    "2B": ("Corse", ["Bastia", "Corte", "Calvi"]),
    "21": ("Bourgogne-Franche-Comté", ["Dijon", "Beaune", "Montbard"]),
    "25": ("Bourgogne-Franche-Comté", ["Besançon", "Montbéliard", "Pontarlier"]),
    "39": ("Bourgogne-Franche-Comté", ["Lons-le-Saunier", "Dole", "Saint-Claude"]),
    "58": ("Bourgogne-Franche-Comté", ["Nevers", "Cosne-Cours-sur-Loire", "Clamecy"]),
    "70": ("Bourgogne-Franche-Comté", ["Vesoul", "Lure", "Héricourt"]),
    "71": ("Bourgogne-Franche-Comté", ["Chalon-sur-Saône", "Mâcon", "Autun"]),
    "89": ("Bourgogne-Franche-Comté", ["Auxerre", "Sens", "Avallon"]),
    "90": ("Bourgogne-Franche-Comté", ["Belfort", "Danjoutin", "Valdoie"]),
    "22": ("Bretagne", ["Saint-Brieuc", "Lannion", "Dinan"]),
    "29": ("Bretagne", ["Brest", "Quimper", "Morlaix"]),
    "35": ("Bretagne", ["Rennes", "Saint-Malo", "Fougères"]),
    "56": ("Bretagne", ["Vannes", "Lorient", "Pontivy"]),
    "08": ("Grand Est", ["Charleville-Mézières", "Sedan", "Rethel"]),
    "10": ("Grand Est", ["Troyes", "Bar-sur-Aube", "Nogent-sur-Seine"]),
    "51": ("Grand Est", ["Reims", "Châlons-en-Champagne", "Épernay"]),
    "52": ("Grand Est", ["Chaumont", "Saint-Dizier", "Langres"]),
    "54": ("Grand Est", ["Nancy", "Lunéville", "Toul"]),
    "55": ("Grand Est", ["Bar-le-Duc", "Verdun", "Commercy"]),
    "57": ("Grand Est", ["Metz", "Thionville", "Forbach"]),
    "67": ("Grand Est", ["Strasbourg", "Haguenau", "Sélestat"]),
    "68": ("Grand Est", ["Mulhouse", "Colmar", "Saint-Louis"]),
    "88": ("Grand Est", ["Épinal", "Saint-Dié-des-Vosges", "Gérardmer"]),
    "02": ("Hauts-de-France", ["Saint-Quentin", "Laon", "Soissons"]),
    "59": ("Hauts-de-France", ["Lille", "Valenciennes", "Roubaix"]),
    "60": ("Hauts-de-France", ["Beauvais", "Compiègne", "Senlis"]),
    "62": ("Hauts-de-France", ["Arras", "Calais", "Boulogne-sur-Mer"]),
    "80": ("Hauts-de-France", ["Amiens", "Abbeville", "Péronne"]),
    "75": ("Île-de-France", ["Paris"]),
    "77": ("Île-de-France", ["Melun", "Meaux", "Fontainebleau"]),
    "78": ("Île-de-France", ["Versailles", "Saint-Germain-en-Laye", "Mantes-la-Jolie"]),
    "91": ("Île-de-France", ["Évry-Courcouronnes", "Massy", "Palaiseau"]),
    "92": ("Île-de-France", ["Nanterre", "Boulogne-Billancourt", "Levallois-Perret"]),
    "93": ("Île-de-France", ["Saint-Denis", "Montreuil", "Aubervilliers"]),
    "94": ("Île-de-France", ["Créteil", "Vitry-sur-Seine", "Ivry-sur-Seine"]),
    "95": ("Île-de-France", ["Cergy", "Argenteuil", "Sarcelles"]),
    "14": ("Normandie", ["Caen", "Lisieux", "Bayeux"]),
    "27": ("Normandie", ["Évreux", "Vernon", "Louviers"]),
    "50": ("Normandie", ["Cherbourg-en-Cotentin", "Saint-Lô", "Avranches"]),
    "61": ("Normandie", ["Alençon", "Flers", "Argentan"]),
    "76": ("Normandie", ["Rouen", "Le Havre", "Dieppe"]),
}

# ===============================
# Utils
# ===============================
def maybe(value, proba: float = 0.7):
    return value if random.random() < proba else None

def random_followers(mini: int, maxi: int) -> int:
    return random.randint(mini, maxi)

def fake_fr_mobile() -> str:
    # évite les formats faker “chelous”
    return "0" + random.choice(["6", "7"]) + "".join(str(random.randint(0, 9)) for _ in range(8))

def social_block(url_proba: float, min_followers: int, max_followers: int):
    """
    Garantit la cohérence:
    - si pas d’URL => followers None
    - si URL => followers int
    """
    url = maybe(fake.url(), url_proba)
    followers = random_followers(min_followers, max_followers) if url else None
    return url, followers

def pick_or_new(pool: List[str], make_new_fn, dup_rate: float) -> str:
    """
    Avec probabilité dup_rate, renvoie une valeur existante (doublon).
    Sinon, génère une nouvelle valeur et l’ajoute au pool.
    """
    if pool and random.random() < dup_rate:
        return random.choice(pool)
    v = make_new_fn()
    pool.append(v)
    return v

# ===============================
# Génération
# ===============================
os.makedirs(os.path.dirname(OUT_PATH) or ".", exist_ok=True)

rows: List[Dict[str, Optional[Union[str, int, bool]]]] = []

# Pools pour créer des doublons CSV
email_pool: List[str] = []
tel_pool: List[str] = []

for _ in range(NB_ROWS):
    dep = random.choice(list(DEPARTEMENTS.keys()))
    region, villes = DEPARTEMENTS[dep]
    ville = random.choice(villes)

    type_prospect = random.choice(TYPES_ENUM)

    # -------------------------------
    # Contacts (cohérents + doublons contrôlés)
    # -------------------------------
    if random.random() < EMAIL_PRESENT_RATE:
        email = pick_or_new(email_pool, lambda: fake.email(), DUP_EMAIL_RATE)
    else:
        email = None

    if random.random() < TEL_PRESENT_RATE:
        telephone = pick_or_new(tel_pool, fake_fr_mobile, DUP_TEL_RATE)
    else:
        telephone = None

    # garantie au moins un des deux (sinon ProspectCreate invalide)
    if not email and not telephone:
        email = pick_or_new(email_pool, lambda: fake.email(), DUP_EMAIL_RATE)

    # -------------------------------
    # Réseaux (cohérents)
    # -------------------------------
    facebook, facebook_followers = social_block(0.70, 100, 10_000)
    x, x_followers = social_block(0.50, 50, 15_000)
    instagram, instagram_followers = social_block(0.70, 100, 30_000)
    youtube, youtube_followers = social_block(0.40, 100, 50_000)
    tictok, tictok_followers = social_block(0.40, 100, 80_000)

    row: Dict[str, Optional[Union[str, int, bool]]] = {
        # champs API attendus
        "nom_structure": f"{type_prospect} {fake.word().capitalize()}",
        "nom_contact": maybe(fake.name(), 0.60),

        "email": email,
        "telephone": telephone,
        "type_prospect": type_prospect,

        "pays": "France",
        "region": region,
        "departement": dep,
        "ville": ville,
        "adresse": maybe(fake.street_address(), 0.80),

        "nb_aderents": maybe(random.randint(20, 500), 0.40),

        "facebook": facebook,
        "facebook_followers": facebook_followers,

        "x": x,
        "x_followers": x_followers,

        "instagram": instagram,
        "instagram_followers": instagram_followers,

        "youtube": youtube,
        "youtube_followers": youtube_followers,

        "tictok": tictok,
        "tictok_followers": tictok_followers,

        "sit_web": maybe(fake.url(), 0.80),

        "accepte_contact": random.choice([True, False]),
        "methode_contact": maybe(random.choice(["email", "telephone", "instagram", "facebook"]), 0.60),

        "contacte": random.choice([True, False]),
        "date_dernier_contact": maybe(str(fake.date_between(start_date="-2y", end_date="today")), 0.50),

        "commentaires": maybe(fake.sentence(), 0.30),
    }

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUT_PATH, index=False, encoding="utf-8")

print("Dataset généré :", len(df), "lignes")
print(f"Export : {OUT_PATH}")
print(f"Emails pool: {len(email_pool)} | Tels pool: {len(tel_pool)}")
print(f"Paramètres: email_present={EMAIL_PRESENT_RATE}, tel_present={TEL_PRESENT_RATE}, dup_email={DUP_EMAIL_RATE}, dup_tel={DUP_TEL_RATE}")
