import streamlit as st

from services.prospects_api import create_prospect
from utils.validators import is_valid_email, is_valid_phone
from utils.constants import (
    TYPE_PROSPECT_OPTIONS,
    REGION_FRANCE_OPTIONS,
    DEPARTEMENT_OPTIONS,
    PAYS_OPTIONS,
    METHODE_CONTACT_OPTIONS,
)

# ------------------------------------------------------------
# Configuration page
# ------------------------------------------------------------
st.set_page_config(
    page_title="Ajouter un prospect",
    layout="centered",
)

st.title("Ajouter un prospect")

# ------------------------------------------------------------
# Session state (gestion doublon + reset)
# ------------------------------------------------------------
if "pending_payload" not in st.session_state:
    st.session_state.pending_payload = None

if "pending_conflict" not in st.session_state:
    st.session_state.pending_conflict = None


def reset_form():
    """
    Supprime toutes les clés du formulaire pour repartir à zéro.
    """
    for key in list(st.session_state.keys()):
        if key.startswith("form_"):
            del st.session_state[key]


# ------------------------------------------------------------
# Bouton retour BDD
# ------------------------------------------------------------
st.page_link("pages/Visualisation_BDD.py", label="⬅ Retour à la BDD")

st.divider()

# ------------------------------------------------------------
# FORMULAIRE
# ------------------------------------------------------------
with st.form("add_prospect_form", clear_on_submit=False):
    st.subheader("Informations principales")

    nom_structure = st.text_input(
        "Nom de la structure *",
        key="form_nom_structure",
    )

    type_prospect = st.selectbox(
        "Type de prospect *",
        TYPE_PROSPECT_OPTIONS,
        index=None,
        placeholder="Choisir un type",
        key="form_type_prospect",
    )

    ville = st.text_input(
        "Ville *",
        key="form_ville",
    )

    st.subheader("Contact")

    email = st.text_input(
        "Email",
        key="form_email",
    )

    telephone = st.text_input(
        "Téléphone",
        key="form_telephone",
    )

    st.subheader("Localisation")

    pays = st.selectbox(
        "Pays",
        PAYS_OPTIONS,
        index=PAYS_OPTIONS.index("France"),
        key="form_pays",
    )
    region = st.selectbox(
        "Région",
        REGION_FRANCE_OPTIONS,
        index=None,
        placeholder="Choisir une région",
        key="form_region",
    )
    departement = st.selectbox(
        "Département",
        DEPARTEMENT_OPTIONS,
        index=None,
        placeholder="Choisir un département",
        key="form_departement",
    )
    adresse = st.text_input("Adresse", key="form_adresse")

    st.subheader("Statut")

    accepte_contact = st.checkbox(
        "Accepte d’être contacté",
        key="form_accepte_contact",
    )

    methode_contact = st.selectbox(
        "Méthode de contact",
        METHODE_CONTACT_OPTIONS,
        index=None,
        placeholder="Choisir une méthode",
        key="form_methode_contact",
    )

    submitted = st.form_submit_button("Ajouter le prospect")

# ------------------------------------------------------------
# VALIDATION + ENVOI API
# ------------------------------------------------------------
if submitted:
    errors = []

    # Champs obligatoires
    if not nom_structure.strip():
        errors.append("Le nom de la structure est obligatoire.")
    if not type_prospect:
        errors.append("Le type de prospect est obligatoire.")
    if not ville.strip():
        errors.append("La ville est obligatoire.")

    # Au moins un moyen de contact
    if not email and not telephone:
        errors.append("Renseigne au moins un email ou un téléphone.")

    # Validation email
    if email and not is_valid_email(email):
        errors.append("Format email invalide.")

    # Validation téléphone
    if telephone and not is_valid_phone(telephone):
        errors.append("Format téléphone invalide.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        payload = {
            "nom_structure": nom_structure,
            "type_prospect": type_prospect,
            "ville": ville,
            "email": email or None,
            "telephone": telephone or None,
            "pays": pays or None,
            "region": region or None,
            "departement": departement or None,
            "adresse": adresse or None,
            "accepte_contact": accepte_contact,
            "methode_contact": methode_contact or None,
        }

        data, err = create_prospect(payload)

        if err:
            if err.get("type") == "conflict":
                st.session_state.pending_payload = payload
                st.session_state.pending_conflict = err.get("detail")
                st.warning("Doublon détecté.")
            else:
                st.error(err.get("message", "Erreur lors de la création."))
        else:
            st.success("Prospect ajouté avec succès")
            reset_form()
            st.rerun()

# ------------------------------------------------------------
# GESTION DOUBLON (forcer / annuler)
# ------------------------------------------------------------
if st.session_state.pending_conflict:
    st.divider()
    st.warning("Un prospect similaire existe déjà.")

    st.json(st.session_state.pending_conflict)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Annuler"):
            st.session_state.pending_payload = None
            st.session_state.pending_conflict = None
            st.rerun()

    with col2:
        if st.button("Forcer l’ajout"):
            payload = st.session_state.pending_payload
            data, err = create_prospect(payload, force=True)

            if err:
                st.error(err.get("message", "Impossible de forcer l’ajout."))
            else:
                st.success("Prospect ajouté (forcé)")
                st.session_state.pending_payload = None
                st.session_state.pending_conflict = None
                reset_form()
                st.rerun()