import streamlit as st

from supabase import Client, create_client

# ── TEMP DEBUG (remove after fixing) ──────────────────────────
_url = st.secrets.get('SUPABASE_URL', 'MISSING')
_key = st.secrets.get('SUPABASE_KEY', 'MISSING')
st.write("DEBUG SUPABASE_URL:", repr(_url))
st.write("DEBUG SUPABASE_KEY length:", len(_key) if _key != 'MISSING' else 'MISSING')
# ───────────────────────────────────────────────────────────────

supabase: Client = create_client(_url, _key)
