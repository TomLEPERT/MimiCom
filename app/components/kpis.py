import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import squarify


# -----------------------------
# PIE TYPE PROSPECT
# -----------------------------
def pie_prospect(kpis: dict):
    type_counts = kpis["type_prospect_dist"]["values"]
    labels = kpis["type_prospect_dist"]["labels"]

    fig, ax = plt.subplots()
    ax.pie(type_counts, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)


# -----------------------------
# HISTO ADHERENTS
# -----------------------------
def histo_adhérents(kpis: dict):
    adherents_counts = kpis["adherents_distribution"]

    fig, ax = plt.subplots()
    sns.histplot(adherents_counts, bins=10, kde=False, ax=ax)
    st.pyplot(fig)


# -----------------------------
# HISTO FOLLOWERS
# -----------------------------
def histo_followers(kpis: dict):
    followers_counts = kpis["followers_distribution"]

    fig, ax = plt.subplots()
    sns.histplot(followers_counts, bins=10, kde=False, ax=ax)
    st.pyplot(fig)


# -----------------------------
# TREEMAP
# -----------------------------
def treemap_followers(kpis: dict):
    followers_counts = kpis["followers_distribution"]
    labels = [f"{i}" for i in followers_counts]

    fig, ax = plt.subplots()
    squarify.plot(sizes=followers_counts, label=labels, ax=ax)
    ax.axis('off')
    st.pyplot(fig)


# -----------------------------
# BAR STATUTS
# -----------------------------
def bar_statuts(kpis: dict):
    statut_counts = kpis["statut_dist"]["values"]
    labels = kpis["statut_dist"]["labels"]

    fig, ax = plt.subplots()
    sns.barplot(x=labels, y=statut_counts, ax=ax)
    st.pyplot(fig)


# -----------------------------
# WEBSITE PIE
# -----------------------------
def website_pie_chart(kpis: dict):
    with_web = kpis["website_with"]
    without_web = kpis["website_without"]

    fig, ax = plt.subplots()
    ax.pie([with_web, without_web], labels=['Avec', 'Sans'], autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)


# -----------------------------
# GAUGES
# -----------------------------
def gauge_accepte_com(kpis: dict):
    st.progress(kpis["acceptance_percentage"])


def gauge_non_contactés(kpis: dict):
    st.progress(kpis["non_contactes_percentage"])


def gauge_tel_manquants(kpis: dict):
    st.progress(kpis["tel_manquants_percentage"])


def gauge_mail_manquants(kpis: dict):
    st.progress(kpis["mail_manquants_percentage"])