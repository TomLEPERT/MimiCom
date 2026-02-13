import streamlit as st

from components.login import render_login

from views.Visualisation_BDD import visualisation_bdd
from views.Ajouter_Prospect import ajouter_prospect
from views.Imports import imports as imports_page
from views.Kpis_Prospects import kpis_prospects


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Mimicom",
    layout="centered"
)


# -------------------------------------------------
# Session state init
# -------------------------------------------------
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("page", "Base prospects")  # DEFAULT LANDING PAGE


# -------------------------------------------------
# Authentication
# -------------------------------------------------
if not st.session_state["authenticated"]:
    render_login()
    st.stop()


# -------------------------------------------------
# Sidebar navigation (MANUAL ROUTER)
# -------------------------------------------------
with st.sidebar:
    st.write(f"Connecté en tant que **{st.session_state['username']}**")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Base prospects", "KPIs"],
        index=["Base prospects", "KPIs"].index(st.session_state["page"])
    )

    st.session_state["page"] = page


# -------------------------------------------------
# Logout
# -------------------------------------------------
st.divider()
def logout():
    st.session_state.clear()
    st.rerun()


# -------------------------------------------------
# Router
# -------------------------------------------------
if st.session_state["page"] == "Base prospects":
    visualisation_bdd()

elif st.session_state["page"] == "KPIs":
    kpis_prospects()
    
elif st.session_state["page"] == "Ajouter":
    ajouter_prospect()

elif st.session_state["page"] == "Imports":
    imports_page()
