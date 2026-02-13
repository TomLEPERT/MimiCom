import time
import streamlit as st

from services.imports_api import (
    preview_import_csv,
    start_commit_async,
    get_import_progress,
    get_import_result,
)
from components.import_summary import render_import_summary
from components.import_preview import render_invalid_rows, render_duplicates


def imports():
    st.set_page_config(page_title="Import CSV", layout="wide")
    st.title("Import CSV")

    if "preview" not in st.session_state:
        st.session_state.preview = None

    # stock des overrides: {row_number(int): strategy(str)}
    if "overrides" not in st.session_state:
        st.session_state.overrides = {}

    uploaded = st.file_uploader("Choisis un CSV", type=["csv"])


    # -----------------------------
    # CSS: barre sticky pour éviter de scroller 9000 lignes
    # -----------------------------
    st.markdown(
        """
    <style>
    .merge-bar {
        position: sticky;
        top: 0;
        background: white;
        padding: 1rem;
        z-index: 999;
        border-bottom: 1px solid #eee;
        border-radius: 0.5rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # PREVIEW
    # -----------------------------
    if st.button("Preview", type="primary", disabled=uploaded is None):
        data, err = preview_import_csv(
            filename=uploaded.name,
            file_bytes=uploaded.getvalue(),
        )
        if err:
            st.error(err["message"])
            if err.get("detail"):
                st.write(err["detail"])
        else:
            st.session_state.preview = data
            st.session_state.overrides = {}  # reset overrides à chaque preview

    preview = st.session_state.preview

    # -----------------------------
    # UI PREVIEW + MERGE
    # -----------------------------
    if preview:
        render_import_summary(preview["summary"])

        if preview.get("message"):
            st.info(preview["message"])

        # -----------------------------
        # MERGE BAR (TOUJOURS EN HAUT)
        # -----------------------------
        st.markdown('<div class="merge-bar">', unsafe_allow_html=True)

        # On garde la stratégie en session_state pour que la page ne la perde pas au rerun
        if "merge_strategy_default" not in st.session_state:
            st.session_state.merge_strategy_default = "ignore_duplicates"

        c1, c2 = st.columns([3, 1])

        with c1:
            st.session_state.merge_strategy_default = st.radio(
                "Stratégie de merge (par défaut)",
                ["ignore_duplicates", "replace_existing", "force_add"],
                horizontal=True,
                index=["ignore_duplicates", "replace_existing", "force_add"].index(st.session_state.merge_strategy_default),
            )

        with c2:
            merge_clicked = st.button(
                "Merge",
                type="primary",
                disabled=(preview["status"] == "INVALID_CSV"),
                width="stretch",
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # OVERRIDES seulement doublons DB
        # -----------------------------
        # IMPORTANT : si tu as 0 doublons DB, on n'affiche rien.
        # (dans ton cas actuel tu as surtout des doublons CSV)
        seen = set()
        dups_db = []
        for d in preview.get("duplicates", []):
            if d.get("source") != "db":
                continue
            rn = int(d["row_number"])
            if rn in seen:
                continue
            seen.add(rn)
            dups_db.append(d)

        if dups_db:
            st.subheader("Overrides (uniquement doublons DB)")
            st.caption("Choisis une stratégie par ligne (sinon = stratégie par défaut).")

            # Option pratique: reset overrides
            if st.button("Réinitialiser les overrides"):
                st.session_state.overrides = {}

            strategy_default = st.session_state.merge_strategy_default

            # (option UX) si beaucoup de doublons DB, on les met en expander
            with st.expander(f"Configurer les overrides DB ({len(dups_db)} ligne(s))", expanded=False):
                for d in dups_db:
                    row_number = int(d["row_number"])
                    match_on = d.get("match_on")
                    existing_id = d.get("existing_prospect_id")

                    label = f"Ligne {row_number} — match {match_on} — existing {existing_id}"

                    # valeur initiale: override si présent sinon stratégie globale
                    current = st.session_state.overrides.get(row_number, strategy_default)

                    choice = st.selectbox(
                        label,
                        ["ignore_duplicates", "replace_existing", "force_add"],
                        index=["ignore_duplicates", "replace_existing", "force_add"].index(current),
                        key=f"override_{row_number}",
                    )

                    # On ne stocke que si différent du global
                    if choice != strategy_default:
                        st.session_state.overrides[row_number] = choice
                    else:
                        st.session_state.overrides.pop(row_number, None)

            st.info(f"Overrides actifs: {len(st.session_state.overrides)}")

        st.divider()

        # -----------------------------
        # AFFICHAGE DES ERREURS / DOUBLONS
        # -----------------------------
        # (UX) si tu as 9000 doublons CSV, on cache le détail derrière un expander
        render_invalid_rows(preview.get("invalid", []))

        duplicates = preview.get("duplicates", []) or []
        if duplicates:
            with st.expander(f"Afficher le détail des doublons ({len(duplicates)})", expanded=False):
                render_duplicates(duplicates)
        else:
            st.success("Aucun doublon détecté")

        st.divider()

        # -----------------------------
        # MERGE ASYNC + PROGRESS
        # -----------------------------
        if merge_clicked:
            import_id = preview["import_id"]
            strategy = st.session_state.merge_strategy_default

            # convertir overrides en { "12": "force_add" } pour JSON
            overrides_payload = {str(k): v for k, v in st.session_state.overrides.items()}

            start_data, start_err = start_commit_async(
                import_id=import_id,
                merge_strategy=strategy,
                overrides=overrides_payload if overrides_payload else None,
            )

            if start_err:
                st.error(start_err["message"])
                if start_err.get("detail"):
                    st.write(start_err["detail"])
            else:
                st.info("Merge démarré…")

                bar = st.progress(0)
                status_box = st.empty()

                while True:
                    prog, prog_err = get_import_progress(import_id=import_id)
                    if prog_err:
                        st.error(prog_err["message"])
                        if prog_err.get("detail"):
                            st.write(prog_err["detail"])
                        break

                    percent = int(prog.get("percent", 0))
                    phase = prog.get("phase", "")
                    status = prog.get("status", "")
                    processed = prog.get("processed", 0)
                    total = prog.get("total", 0)

                    bar.progress(max(0, min(100, percent)))
                    status_box.write(f"**{status}** — {phase} — {processed}/{total}")

                    if status == "done":
                        res, res_err = get_import_result(import_id=import_id)
                        if res_err:
                            st.error(res_err["message"])
                            if res_err.get("detail"):
                                st.write(res_err["detail"])
                        else:
                            st.success("Merge terminé")
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Insérés", res.get("inserted", 0))
                            c2.metric("Mis à jour", res.get("updated", 0))
                            c3.metric("Ignorés", res.get("ignored", 0))

                            if res.get("overrides_count") is not None:
                                st.caption(f"Overrides appliqués: {res.get('overrides_count')}")

                            if res.get("errors"):
                                st.warning("Erreurs pendant le merge")
                                st.write(res["errors"])

                        # reset state
                        st.session_state.preview = None
                        st.session_state.overrides = {}
                        break

                    if status == "error":
                        st.error(f"Erreur merge: {prog.get('error', 'unknown')}")
                        break

                    time.sleep(0.5)
