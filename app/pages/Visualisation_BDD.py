import streamlit as st

from services.prospects_api import list_prospects, get_prospect, delete_prospect, search_prospects
from components.prospects_table import render_prospects_table
from components.prospect_card import render_prospect_card
from components.prospect_inline_edit import render_prospect_inline_edit
from components.prospects_filters import render_prospects_filters


# ------------------------------------------------------------
# Config page
# ------------------------------------------------------------
st.set_page_config(page_title="BDD Prospects", layout="wide")
st.title("Base de données prospects")

# Bouton
st.page_link("pages/Ajouter_Prospect.py", label="Ajouter un prospect")


# ------------------------------------------------------------
# Session state : modes + sélection
# ------------------------------------------------------------
# mode = "list" | "view"
if "bdd_mode" not in st.session_state:
    st.session_state.bdd_mode = "list"

# Prospect actuellement consulté (prospect_id)
if "bdd_selected_id" not in st.session_state:
    st.session_state.bdd_selected_id = None

# Prospect actuellement en édition inline (prospect_id)
if "bdd_edit_id" not in st.session_state:
    st.session_state.bdd_edit_id = None

# Confirmation suppression
if "bdd_confirm_delete_id" not in st.session_state:
    st.session_state.bdd_confirm_delete_id = None


def go_list():
    """Revenir en mode liste."""
    st.session_state.bdd_mode = "list"
    st.session_state.bdd_selected_id = None
    st.session_state.bdd_edit_id = None
    st.session_state.bdd_confirm_delete_id = None


def go_view(prospect_id: str):
    """Aller en mode view."""
    st.session_state.bdd_mode = "view"
    st.session_state.bdd_selected_id = prospect_id
    st.session_state.bdd_edit_id = None
    st.session_state.bdd_confirm_delete_id = None


def start_edit(prospect_id: str):
    """Activer l'édition inline (sans changer de page)."""
    st.session_state.bdd_edit_id = prospect_id
    st.session_state.bdd_confirm_delete_id = None


def stop_edit():
    """Stopper l'édition inline."""
    st.session_state.bdd_edit_id = None

# ------------------------------------------------------------
# FILTRES (nom + email + telephone)
# ------------------------------------------------------------
filters = render_prospects_filters(
    key="bdd",
    fields=["nom", "email", "telephone"],
    show_sort=True,
)

# ------------------------------------------------------------
# Chargement de la liste (GET ou SEARCH selon filtres)
# ------------------------------------------------------------
if filters:
    data, err = search_prospects(**filters)
else:
    data, err = list_prospects()

if err:
    st.error(err.get("message", "Erreur chargement prospects"))
    st.stop()

prospects = data or []

# ------------------------------------------------------------
# MODE VIEW : on cache le tableau, on affiche la fiche
# ------------------------------------------------------------
if st.session_state.bdd_mode == "view":
    pid = st.session_state.bdd_selected_id
    if not pid:
        go_list()
        st.rerun()

    # On récupère la fiche complète côté API
    prospect, perr = get_prospect(pid)
    if perr:
        st.error(perr.get("message", "Impossible de charger le prospect."))
        if st.button("Retour à la liste"):
            go_list()
            st.rerun()
        st.stop()

    # Fiche
    action = render_prospect_card(prospect, key="bdd_card")

    if action == "back":
        go_list()
        st.rerun()

    if action == "edit":
        start_edit(pid)
        st.rerun()

    # Edition inline sous la card (si activée)
    if st.session_state.bdd_edit_id == pid:
        st.divider()
        edit_action = render_prospect_inline_edit(prospect, key="bdd_card_edit")

        # Si saved -> on reste sur la fiche mais on recharge (rerun)
        if edit_action == "saved":
            stop_edit()
            st.rerun()

        if edit_action == "cancel":
            stop_edit()
            st.rerun()

    st.stop()


# ------------------------------------------------------------
# MODE LISTE : tableau + actions + édition inline sous le tableau
# ------------------------------------------------------------
selected, action = render_prospects_table(
    prospects,
    title="Tous les prospects",
    key="bdd_all",
)

# Si l'utilisateur clique une action
if selected and action:
    pid = selected.get("prospect_id")

    if action == "view":
        go_view(pid)
        st.rerun()

    elif action == "edit":
        # Edition inline dans la page (sous le tableau)
        start_edit(pid)
        st.rerun()

    elif action == "delete":
        st.session_state.bdd_confirm_delete_id = pid
        st.rerun()


# ------------------------------------------------------------
# Confirmation suppression
# ------------------------------------------------------------
if st.session_state.bdd_confirm_delete_id:
    pid = st.session_state.bdd_confirm_delete_id

    st.divider()
    st.warning(f"Confirmer suppression du prospect `{pid}` ?")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Oui supprimer", key="bdd_delete_yes"):
            _, derr = delete_prospect(pid)
            if derr:
                st.error(derr.get("message", "Erreur suppression"))
            else:
                st.success("Prospect supprimé")
            st.session_state.bdd_confirm_delete_id = None
            # On coupe aussi l'éventuelle édition en cours
            if st.session_state.bdd_edit_id == pid:
                stop_edit()
            st.rerun()

    with c2:
        if st.button("Annuler", key="bdd_delete_no"):
            st.session_state.bdd_confirm_delete_id = None
            st.rerun()


# ------------------------------------------------------------
# Edition inline SOUS le tableau (si activée)
# ------------------------------------------------------------
if st.session_state.bdd_edit_id:
    pid = st.session_state.bdd_edit_id

    st.divider()
    st.info(f"Édition inline : `{pid}`")

    # On récupère la version complète du prospect avant d'éditer
    prospect, perr = get_prospect(pid)
    if perr:
        st.error(perr.get("message", "Impossible de charger le prospect pour édition."))
        if st.button("Fermer l'édition", key="bdd_close_edit_on_error"):
            stop_edit()
            st.rerun()
        st.stop()

    edit_action = render_prospect_inline_edit(prospect, key="bdd_table_edit")

    if edit_action == "saved":
        stop_edit()
        st.rerun()

    if edit_action == "cancel":
        stop_edit()
        st.rerun()
