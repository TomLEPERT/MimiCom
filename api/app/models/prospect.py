from datetime import date
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator, model_validator

# Helpers utilitaires pour normaliser et valider les données
from app.utils.normalizers import normalize_str, normalize_phone, validate_phone


# -------------------------------------------------------------------
# Enum : types de prospects autorisés
# -------------------------------------------------------------------
# Cette enum définit une liste fermée de valeurs possibles.
# Si une autre valeur est envoyée par le client → erreur 422 automatique.
class ProspectType(str, Enum):
    CSCS = "CSCS"
    BAR_A_JEUX = "Bar à jeux"
    INFLUENCEUR = "Influenceur"
    MJC = "MJC"
    MEDIATHEQUE = "Médiathèque"
    ARTISAN = "Artisan"
    EDITEUR = "Éditeur"
    ASSO_JDR = "Asso JDR"
    BOUTIQUE_SPECIALISEE = "Boutique spécialisée"
    LUDOTHEQUE = "Ludothèque"


# -------------------------------------------------------------------
# Modèle de base Prospect
# -------------------------------------------------------------------
# Cette classe contient tous les champs communs.
# Elle est utilisée comme base pour :
# - ProspectCreate (création)
# - ProspectUpdate (mise à jour)
# - ProspectOut (sortie API)
class ProspectBase(BaseModel):

    # Configuration Pydantic :
    # - extra="forbid" → interdit les champs inconnus dans le payload
    model_config = ConfigDict(extra="forbid")

    # -------------------------
    # Identité du prospect
    # -------------------------
    nom_structure: Optional[str] = Field(default=None, max_length=200)
    nom_contact: Optional[str] = Field(default=None, max_length=200)

    # Email :
    # - EmailStr valide automatiquement le format email
    email: Optional[EmailStr] = None

    # Téléphone :
    # - format nettoyé + validé via des validateurs custom plus bas
    telephone: Optional[str] = Field(default=None, max_length=30)

    # Type de prospect :
    # - doit appartenir à l'enum ProspectType
    type_prospect: Optional[ProspectType] = None

    # -------------------------
    # Localisation
    # -------------------------
    pays: Optional[str] = Field(default=None, max_length=100)
    region: Optional[str] = Field(default=None, max_length=100)
    departement: Optional[str] = Field(default=None, max_length=100)
    ville: Optional[str] = Field(default=None, max_length=120)
    adresse: Optional[str] = Field(default=None, max_length=300)

    # -------------------------
    # Données de taille / audience
    # -------------------------
    # Nombre d'adhérents (doit être >= 0)
    nb_aderents: Optional[int] = Field(default=None, ge=0)

    # Réseaux sociaux + followers
    facebook: Optional[str] = Field(default=None, max_length=300)
    facebook_followers: Optional[int] = Field(default=None, ge=0)

    x: Optional[str] = Field(default=None, max_length=300)
    x_followers: Optional[int] = Field(default=None, ge=0)

    instagram: Optional[str] = Field(default=None, max_length=300)
    instagram_followers: Optional[int] = Field(default=None, ge=0)

    tictok: Optional[str] = Field(default=None, max_length=300)
    tictok_followers: Optional[int] = Field(default=None, ge=0)

    youtube: Optional[str] = Field(default=None, max_length=300)
    youtube_followers: Optional[int] = Field(default=None, ge=0)

    # -------------------------
    # Site web
    # -------------------------
    sit_web: Optional[str] = Field(default=None, max_length=300)

    # -------------------------
    # Statut de contact
    # -------------------------
    # Booléen avec valeur par défaut = False
    accepte_contact: bool = False

    methode_contact: Optional[str] = Field(default=None, max_length=50)

    # Booléen avec valeur par défaut = False
    contacte: bool = False

    # Date au format ISO (YYYY-MM-DD)
    date_dernier_contact: Optional[date] = None

    # -------------------------
    # Commentaires libres
    # -------------------------
    commentaires: Optional[str] = None

    # ----------------------------------------------------------------
    # Normalisation des champs texte
    # ----------------------------------------------------------------
    # Ce validateur s'exécute AVANT la validation Pydantic.
    # Il :
    # - supprime les espaces en début / fin
    # - convertit les chaînes vides ("") en None
    @field_validator(
        "nom_structure",
        "nom_contact",
        "pays",
        "region",
        "departement",
        "ville",
        "adresse",
        "facebook",
        "x",
        "instagram",
        "tictok",
        "youtube",
        "sit_web",
        "methode_contact",
        "commentaires",
        mode="before",
    )
    @classmethod
    def strip_strings(cls, v: Any) -> Any:
        """
        Supprime les espaces inutiles et convertit les chaînes vides en None.
        """
        return normalize_str(v)

    # ----------------------------------------------------------------
    # Normalisation du téléphone
    # ----------------------------------------------------------------
    # Ce validateur s'exécute AVANT la validation du format.
    # Il :
    # - trim
    # - collapse les espaces multiples
    @field_validator("telephone", mode="before")
    @classmethod
    def normalize_telephone(cls, v: Any) -> Any:
        """
        Nettoie le format du téléphone avant validation.
        """
        return normalize_phone(v)

    # ----------------------------------------------------------------
    # Validation du téléphone
    # ----------------------------------------------------------------
    # Ce validateur s'exécute APRÈS la normalisation.
    # Il vérifie que le téléphone respecte le regex défini.
    # Si invalide → erreur 422 automatique.
    @field_validator("telephone")
    @classmethod
    def check_phone(cls, v: Optional[str]) -> Optional[str]:
        """
        Vérifie que le téléphone respecte le format attendu.
        """
        return validate_phone(v)
    
# -------------------------------------------------------------------
# Modèle utilisé pour la CRÉATION d'un prospect (POST /prospects)
# -------------------------------------------------------------------
class ProspectCreate(ProspectBase):
    # Champs obligatoires
    # min_length=1 garantit qu'on ne peut pas envoyer une chaîne vide.
    nom_structure: str = Field(..., min_length=1, max_length=200)
    type_prospect: ProspectType = Field(...)

    # Sécurité : même si le client essaie d'envoyer prospect_id,
    # on l'ignore complètement, le backend le générera.
    prospect_id: Optional[str] = Field(default=None, exclude=True)

    # ----------------------------------------------------------------
    # Validation métier transversale (au moins email OU téléphone)
    # ----------------------------------------------------------------
    @model_validator(mode="after")
    def check_at_least_one_contact(self):
        """
        Vérifie qu'au moins un des deux champs email ou téléphone
        est renseigné à la création.
        """
        if not self.email and not self.telephone:
            raise ValueError(
                "Vous devez renseigner au moins un moyen de contact : email ou téléphone."
            )

        return self


# -------------------------------------------------------------------
# Modèle utilisé pour la MISE À JOUR d'un prospect (PATCH /prospects/{id})
# -------------------------------------------------------------------
class ProspectUpdate(ProspectBase):

    # Sécurité : si le client envoie prospect_id dans le payload,
    # on l'ignore complètement.
    prospect_id: Optional[str] = Field(default=None, exclude=True)
    
# -------------------------------------------------------------------
# Modèle utilisé en SORTIE API
# -------------------------------------------------------------------
class ProspectOut(ProspectBase):

    # Identifiant unique du prospect
    prospect_id: str
