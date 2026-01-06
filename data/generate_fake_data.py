import random
import uuid
from typing import Optional, Dict, Union, cast
import pandas as pd
from faker import Faker

fake = Faker("fr_FR")

# ===============================
# CONFIGURATION
# ===============================
NB_ROWS = 5000

TYPES = [
    "Asso jdr",
    "CSCS",
    "MJC",
    "Ludothèque",
    "Editeur",
    "Influenceur",
    "Médiathèque",
    "Bar à jeux",
    "Boutique spécialisée",
    "Artisan"
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
    "76": ("Normandie", ["Rouen", "Le Havre", "Dieppe"])
}

# ===============================
# FONCTIONS UTILITAIRES
# ===============================

def maybe(value: str, proba: float = 0.7) -> Optional[str]:
    return value if random.random() < proba else None

def maybe_int(value: int, proba: float = 0.7) -> Optional[int]:
    return value if random.random() < proba else None

def random_followers(mini: int, maxi: int) -> int:
    return random.randint(mini, maxi)

def generate_socials(prospect_type: str) -> Dict[str, Optional[Union[str, int]]]:
    data: Dict[str, Optional[Union[str, int]]] = {
        "FB": None, "FB_nb_aderent": None,
        "Twitter": None, "Twitter_nb_aderent": None,
        "Insta": None, "Insta_nb_aderent": None,
        "Youtube": None, "Youtube_nb_aderent": None,
        "Tiktok": None, "Tiktok_nb_aderent": None,
    }

    # Structures (asso, médiathèque, MJC…)
    if prospect_type in ["Asso jdr", "MJC", "CSCS", "Ludothèque", "Médiathèque"]:
        if random.random() < 0.85:
            data["FB"] = fake.url()
            data["FB_nb_aderent"] = random_followers(100, 4000)

        if random.random() < 0.35:
            data["Twitter"] = fake.url()
            data["Twitter_nb_aderent"] = random_followers(50, 2000)

        if random.random() < 0.25:
            data["Insta"] = fake.url()
            data["Insta_nb_aderent"] = random_followers(100, 3000)

    # Commerces / bars / artisans
    if prospect_type in ["Bar à jeux", "Boutique spécialisée", "Artisan"]:
        if random.random() < 0.75:
            data["Insta"] = fake.url()
            data["Insta_nb_aderent"] = random_followers(300, 6000)

        if random.random() < 0.95:
            data["FB"] = fake.url()
            data["FB_nb_aderent"] = random_followers(200, 5000)

        if random.random() < 0.8:
            data["Twitter"] = fake.url()
            data["Twitter_nb_aderent"] = random_followers(100, 3000)

    # Éditeurs
    if prospect_type == "Editeur":
        if random.random() < 1:
            data["FB"] = fake.url()
            data["FB_nb_aderent"] = random_followers(500, 10000)

        if random.random() < 1:
            data["Twitter"] = fake.url()
            data["Twitter_nb_aderent"] = random_followers(500, 15000)

        if random.random() < 1:
            data["Insta"] = fake.url()
            data["Insta_nb_aderent"] = random_followers(800, 12000)

        if random.random() < 0.8:
            data["Youtube"] = fake.url()
            data["Youtube_nb_aderent"] = random_followers(300, 8000)

    # Influenceurs
    if prospect_type == "Influenceur":
        data["Insta"] = fake.url()
        data["Insta_nb_aderent"] = random_followers(2000, 30000)

        if random.random() < 1:
            data["Twitter"] = fake.url()
            data["Twitter_nb_aderent"] = random_followers(1000, 25000)

        if random.random() < 0.8:
            data["Youtube"] = fake.url()
            data["Youtube_nb_aderent"] = random_followers(2000, 50000)

        if random.random() < 0.85:
            data["Tiktok"] = fake.url()
            data["Tiktok_nb_aderent"] = random_followers(3000, 80000)

    return data

def generate_nb_adherent(prospect_type: str) -> Optional[int]:
    if prospect_type in ["Asso jdr", "MJC", "CSCS", "Ludothèque", "Médiathèque"]:
        return random.randint(20, 500)
    return None

# ===============================
# GÉNÉRATION DU DATASET
# ===============================

rows = []

for _ in range(NB_ROWS):
    dep = random.choice(list(DEPARTEMENTS.keys()))
    region, villes = DEPARTEMENTS[dep]
    ville = random.choice(villes)
    prospect_type = random.choice(TYPES)
    socials = generate_socials(prospect_type)

    # Champs typés
    email: Optional[str] = maybe(fake.email(), 0.95)
    tel: Optional[str] = maybe(fake.phone_number(), 0.9)
    web_site: Optional[str] = maybe(fake.url(), 0.9)
    commentaire: Optional[str] = maybe(fake.sentence(), 0.3)
    date_contact: Optional[str] = maybe(str(fake.date_between(start_date="-2y", end_date="today")), 0.5)
    fb_nb: Optional[int] = cast(Optional[int], socials["FB_nb_aderent"])
    twitter_nb: Optional[int] = cast(Optional[int], socials["Twitter_nb_aderent"])
    insta_nb: Optional[int] = cast(Optional[int], socials["Insta_nb_aderent"])
    youtube_nb: Optional[int] = cast(Optional[int], socials["Youtube_nb_aderent"])
    tiktok_nb: Optional[int] = cast(Optional[int], socials["Tiktok_nb_aderent"])
    nb_adherent: Optional[int] = generate_nb_adherent(prospect_type)

    row: Dict[str, Optional[Union[str, int]]] = {
        "ID": str(uuid.uuid4())[:8],
        "Nom": f"{prospect_type} {fake.word().capitalize()}",
        "Email": email,
        "Tel": tel,
        "Type": prospect_type,
        "Web_site": web_site,
        "FB": socials["FB"],
        "FB_nb_aderent": fb_nb,
        "Twitter": socials["Twitter"],
        "Twitter_nb_aderent": twitter_nb,
        "Insta": socials["Insta"],
        "Insta_nb_aderent": insta_nb,
        "Youtube": socials["Youtube"],
        "Youtube_nb_aderent": youtube_nb,
        "Tiktok": socials["Tiktok"],
        "Tiktok_nb_aderent": tiktok_nb,
        "nb_adherent": nb_adherent,
        "Date_contact": date_contact,
        "Adresse_postal": f"{fake.street_address()} {ville}",
        "Departement": dep,
        "Region": region,
        "Pays": "France",
        "Accepte_com": random.choice(["Oui", "Non"]),
        "Statut": random.choice(["Prospect", "Contacté", "Intéressé"]),
        "Commentaire": commentaire,
    }

    rows.append(row)

df = pd.DataFrame(rows)

# ===============================
# EXPORT CSV
# ===============================
df.to_csv("fake_festival_jdr_dataset.csv", index=False, encoding="utf-8")

print("Dataset généré :", len(df), "lignes")
