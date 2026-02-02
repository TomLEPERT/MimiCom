import random
import uuid
from typing import Optional, Dict
import pandas as pd
from faker import Faker

fake = Faker("fr_FR")

NB_ROWS = 5000

# ------------------------------------------------------------
# ENUMS BACK / FRONT (ALIGNÉS)
# ------------------------------------------------------------
TYPE_PROSPECT_OPTIONS = [
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

METHODE_CONTACT_OPTIONS = [
    "Email", "Téléphone", "Facebook", "Instagram", "X", "TikTok", "Autre"
]

PAYS_OPTIONS = ["France", "Belgique", "Suisse"]

STATUT_OPTIONS = ["Prospect", "Contacté", "Intéressé"]

# ------------------------------------------------------------
# DÉPARTEMENT → RÉGION
# ------------------------------------------------------------
DEPARTEMENTS = {
        "01 - Ain",
    "02 - Aisne",
    "03 - Allier",
    "04 - Alpes-de-Haute-Provence",
    "05 - Hautes-Alpes",
    "06 - Alpes-Maritimes",
    "07 - Ardèche",
    "08 - Ardennes",
    "09 - Ariège",
    "10 - Aube",
    "11 - Aude",
    "12 - Aveyron",
    "13 - Bouches-du-Rhône",
    "14 - Calvados",
    "15 - Cantal",
    "16 - Charente",
    "17 - Charente-Maritime",
    "18 - Cher",
    "19 - Corrèze",
    "21 - Côte-d'Or",
    "22 - Côtes-d'Armor",
    "23 - Creuse",
    "24 - Dordogne",
    "25 - Doubs",
    "26 - Drôme",
    "27 - Eure",
    "28 - Eure-et-Loir",
    "29 - Finistère",
    "2A - Corse-du-Sud",
    "2B - Haute-Corse",
    "30 - Gard",
    "31 - Haute-Garonne",
    "32 - Gers",
    "33 - Gironde",
    "34 - Hérault",
    "35 - Ille-et-Vilaine",
    "36 - Indre",
    "37 - Indre-et-Loire",
    "38 - Isère",
    "39 - Jura",
    "40 - Landes",
    "41 - Loir-et-Cher",
    "42 - Loire",
    "43 - Haute-Loire",
    "44 - Loire-Atlantique",
    "45 - Loiret",
    "46 - Lot",
    "47 - Lot-et-Garonne",
    "48 - Lozère",
    "49 - Maine-et-Loire",
    "50 - Manche",
    "51 - Marne",
    "52 - Haute-Marne",
    "53 - Mayenne",
    "54 - Meurthe-et-Moselle",
    "55 - Meuse",
    "56 - Morbihan",
    "57 - Moselle",
    "58 - Nièvre",
    "59 - Nord",
    "60 - Oise",
    "61 - Orne",
    "62 - Pas-de-Calais",
    "63 - Puy-de-Dôme",
    "64 - Pyrénées-Atlantiques",
    "65 - Hautes-Pyrénées",
    "66 - Pyrénées-Orientales",
    "67 - Bas-Rhin",
    "68 - Haut-Rhin",
    "69 - Rhône",
    "70 - Haute-Saône",
    "71 - Saône-et-Loire",
    "72 - Sarthe",
    "73 - Savoie",
    "74 - Haute-Savoie",
    "75 - Paris",
    "76 - Seine-Maritime",
    "77 - Seine-et-Marne",
    "78 - Yvelines",
    "79 - Deux-Sèvres",
    "80 - Somme",
    "81 - Tarn",
    "82 - Tarn-et-Garonne",
    "83 - Var",
    "84 - Vaucluse",
    "85 - Vendée",
    "86 - Vienne",
    "87 - Haute-Vienne",
    "88 - Vosges",
    "89 - Yonne",
    "90 - Territoire de Belfort",
    "91 - Essonne",
    "92 - Hauts-de-Seine",
    "93 - Seine-Saint-Denis",
    "94 - Val-de-Marne",
    "95 - Val-d'Oise",

    # DOM
    "971 - Guadeloupe",
    "972 - Martinique",
    "973 - Guyane",
    "974 - La Réunion",
    "976 - Mayotte",
}

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def maybe(value, p=0.7):
    return value if random.random() < p else None

def phone_fr():
    return fake.msisdn()[:10]

def followers(mini, maxi):
    return random.randint(mini, maxi)

def social_block(prob, f_min, f_max):
    if random.random() < prob:
        return fake.url(), followers(f_min, f_max)
    return None, None

# ------------------------------------------------------------
# GÉNÉRATION
# ------------------------------------------------------------
rows = []

for _ in range(NB_ROWS):
    prospect_type = random.choice(TYPE_PROSPECT_OPTIONS)

    departement = random.choice(list(DEPARTEMENTS.keys()))
    region = DEPARTEMENTS[departement]

    email = maybe(fake.email(), 0.85)
    telephone = maybe(phone_fr(), 0.85)

    # RÈGLE MÉTIER : au moins un contact
    if not email and not telephone:
        if random.random() < 0.5:
            email = fake.email()
        else:
            telephone = phone_fr()

    facebook, facebook_followers = social_block(0.7, 100, 5000)
    instagram, instagram_followers = social_block(0.6, 300, 8000)
    x, x_followers = social_block(0.4, 100, 4000)
    youtube, youtube_followers = social_block(0.3, 200, 15000)
    tictok, tictok_followers = social_block(0.35, 500, 20000)

    methode_contact = random.choice(
        [m for m in METHODE_CONTACT_OPTIONS if m.lower() in (email or "").lower()]
        or METHODE_CONTACT_OPTIONS
    )

    row = {
        "nom_structure": f"{prospect_type} {fake.company()}",
        "nom_contact": fake.name(),
        "email": email,
        "telephone": telephone,
        "type_prospect": prospect_type,

        "pays": random.choice(PAYS_OPTIONS),
        "region": region,
        "departement": departement,
        "ville": fake.city(),
        "adresse": fake.street_address(),

        "nb_aderents": random.randint(20, 600) if prospect_type in [
            "Asso JDR", "MJC", "CSCS", "Ludothèque", "Médiathèque"
        ] else None,

        "facebook": facebook,
        "facebook_followers": facebook_followers,
        "instagram": instagram,
        "instagram_followers": instagram_followers,
        "x": x,
        "x_followers": x_followers,
        "youtube": youtube,
        "youtube_followers": youtube_followers,
        "tictok": tictok,
        "tictok_followers": tictok_followers,

        "sit_web": maybe(fake.url(), 0.8),

        "accepte_contact": random.choice([True, False]),
        "methode_contact": methode_contact,
        "contacte": random.choice([True, False]),
        "date_dernier_contact": maybe(fake.date_between("-2y", "today").isoformat(), 0.5),

        "commentaires": maybe(fake.sentence(), 0.3),
    }

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv(
    "fake_prospects_import_ready.csv",
    index=False,
    encoding="utf-8",
)

print("Dataset généré :", len(df), "lignes")