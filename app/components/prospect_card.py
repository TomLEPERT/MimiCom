from typing import Any, Dict, Optional
import streamlit as st


def _format_link(url: Optional[str]) -> str:
    """
    Retourne un lien cliquable si possible, sinon un tiret.
    """
    if not url:
        return "—"
    return url


def render_prospect_card(prospect: Dict[str, Any], *, key: str = "card") -> Optional[str]:
    """
    Affiche une fiche prospect complète.

    Retourne une action :
    - "back" : revenir à la liste
    - "edit" : ouvrir l'édition inline
    - None   : rien
    """

    st.subheader("Fiche prospect")

    # ------------------------------------------------------------
    # Header : titre + actions
    # ------------------------------------------------------------
    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        st.write(f"### {prospect.get('nom_structure') or '—'}")
        # Nom du contact + ID technique
        nom_contact = prospect.get("nom_contact") or "—"
        st.caption(f"Contact : {nom_contact}  |  ID : {prospect.get('prospect_id')}")

    with c2:
        if st.button("Modifier", key=f"{key}_edit", width="stretch"):
            return "edit"

    with c3:
        if st.button("Retour", key=f"{key}_back", width="stretch"):
            return "back"

    st.divider()

    # ------------------------------------------------------------
    # Informations principales
    # ------------------------------------------------------------
    st.write("#### Informations")
    st.write(f"- **Type** : {prospect.get('type_prospect') or '—'}")
    st.write(f"- **Ville** : {prospect.get('ville') or '—'}")
    st.write(f"- **Région** : {prospect.get('region') or '—'}")
    st.write(f"- **Département** : {prospect.get('departement') or '—'}")
    st.write(f"- **Pays** : {prospect.get('pays') or '—'}")
    st.write(f"- **Adresse** : {prospect.get('adresse') or '—'}")

    # ------------------------------------------------------------
    # Contact
    # ------------------------------------------------------------
    st.write("#### Contact")
    st.write(f"- **Email** : {prospect.get('email') or '—'}")
    st.write(f"- **Téléphone** : {prospect.get('telephone') or '—'}")
    st.write(f"- **Site web** : {_format_link(prospect.get('sit_web'))}")

    # ------------------------------------------------------------
    # Réseaux sociaux + followers
    # ------------------------------------------------------------
    st.write("#### Réseaux sociaux")

    # On prépare une petite table lisible (réseau / lien / followers)
    rows = [
        ("Facebook", prospect.get("facebook"), prospect.get("facebook_followers")),
        ("X (Twitter)", prospect.get("x"), prospect.get("x_followers")),
        ("Instagram", prospect.get("instagram"), prospect.get("instagram_followers")),
        ("TikTok", prospect.get("tictok"), prospect.get("tictok_followers")),
        ("YouTube", prospect.get("youtube"), prospect.get("youtube_followers")),
    ]

    # On n'affiche pas des lignes vides : mais on laisse "—" si tout est vide
    any_social = any((link or followers) for _, link, followers in rows)

    if not any_social:
        st.write("—")
    else:
        for label, link, followers in rows:
            followers_txt = "—" if followers is None else str(followers)
            st.write(f"- **{label}** : {_format_link(link)}  |  **Followers** : {followers_txt}")

        followers_values = [
            v for v in [
                prospect.get("facebook_followers"),
                prospect.get("x_followers"),
                prospect.get("instagram_followers"),
                prospect.get("tictok_followers"),
                prospect.get("youtube_followers"),
            ]
            if isinstance(v, int)
        ]
        if followers_values:
            st.caption(f"Portée max (réseau le plus fort) : {max(followers_values)}")

    # ------------------------------------------------------------
    # Statut
    # ------------------------------------------------------------
    st.write("#### Statut")
    st.write(f"- **Accepte contact** : {prospect.get('accepte_contact')}")
    st.write(f"- **Contacté** : {prospect.get('contacte')}")
    st.write(f"- **Dernier contact** : {prospect.get('date_dernier_contact') or '—'}")
    st.write(f"- **Méthode** : {prospect.get('methode_contact') or '—'}")

    # ------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------
    st.write("#### Notes")
    st.write(prospect.get("commentaires") or "—")

    return None
