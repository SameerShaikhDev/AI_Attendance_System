import streamlit as st
import segno
import io


@st.dialog("Share Subject")
def share_subject(subject_name, subject_code):
    app_domain = 'http://localhost:8501'
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header(f"📚 {subject_name}")

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)
    out.seek(0)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔗 Copy Link")
        st.code(join_url, language='text')

        st.markdown("### 🔑 Join Code")
        st.code(subject_code, language='text')  # typo fix: subjec_code → subject_code

        st.info("WhatsApp pe share karo ya code bata do")

    with col2:
        st.markdown("### 📷 Scan to Join")  # fix: st,amrkdown → st.markdown
        st.image(out.getvalue(), use_container_width=True, caption="QR Code to Join")