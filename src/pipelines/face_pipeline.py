import streamlit as st
import numpy as np
import cv2
from src.database.db import get_all_students

# ─────────────────────────────────────────────
# InsightFace load karo (buffalo_sc = light model, works well for classrooms)
# ─────────────────────────────────────────────
@st.cache_resource
def load_face_app():
    """
    InsightFace ArcFace model load .
    buffalo_sc  → detection + 512-d ArcFace embedding 
    det_size    → jitna bada, utna better detection (but slower).
                  640x640 classroom ke liye theek hai.
    """
    try:
        import insightface
        from insightface.app import FaceAnalysis

        app = FaceAnalysis(
            name="buffalo_sc",          # lightweight ArcFace model
            providers=["CPUExecutionProvider"],
        )
        app.prepare(ctx_id=0, det_size=(640, 640))
        return app
    except Exception as e:
        st.error(f"InsightFace load nahi hua: {e}")
        return None


def get_face_embeddings(image: np.ndarray) -> list[np.ndarray]:
    
    app = load_face_app()
    if app is None:
        return []

    # InsightFace BGR expect karta hai
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    faces = app.get(bgr)

    embeddings = []
    for face in faces:
        emb = face.normed_embedding  # already L2-normalized, shape (512,)
        embeddings.append(emb.astype(np.float32))

    return embeddings


# ─────────────────────────────────────────────
# DB se embeddings load + cosine similarity match
# ─────────────────────────────────────────────

def _build_student_map() -> dict[int, list[np.ndarray]]:
    """
    DB se saare students ka face_embedding load karo.
    Returns: {student_id: [emb1, emb2, ...]}
    """
    student_db = get_all_students()
    student_map: dict[int, list[np.ndarray]] = {}

    for student in (student_db or []):
        sid = student.get("student_id")
        emb = student.get("face_embedding")
        if sid is not None and emb is not None:
            arr = np.array(emb, dtype=np.float32)
            # normalize karo agar DB mein raw hai
            norm = np.linalg.norm(arr)
            if norm > 0:
                arr = arr / norm
            student_map.setdefault(int(sid), []).append(arr)

    return student_map


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Dono vectors already normalized hain → dot product = cosine similarity.
    Range: -1 to 1 (same person → close to 1).
    """
    return float(np.dot(a, b))


def _match_face(
    query_emb: np.ndarray,
    student_map: dict[int, list[np.ndarray]],
    threshold: float = 0.45,          # ArcFace cosine ke liye 0.45 solid hai
) -> tuple[int | None, float]:
    """
    query_emb ko saare stored embeddings se compare karo.
    Sabse zyada score wala student → match, agar threshold ke upar ho.

    Returns:
        (student_id, best_score) ya (None, best_score)
    """
    best_sid = None
    best_score = -1.0

    for sid, stored_embs in student_map.items():
        # ek student ke multiple registered embeddings mein se best lete hain
        score = max(_cosine_similarity(query_emb, s) for s in stored_embs)
        if score > best_score:
            best_score = score
            best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


# ─────────────────────────────────────────────
# Main predict function
# ─────────────────────────────────────────────

def predict_attendance(
    class_image: np.ndarray,
    threshold: float = 0.45,
) -> tuple[dict[int, float], list[int], int]:
    """
    Classroom photo deke attendance predict karo.

    Args:
        class_image : RGB numpy array
        threshold   : cosine similarity cutoff (0.45 recommended for ArcFace)

    Returns:
        (detected_students, all_students, total_faces_found)
        detected_students = {student_id: best_score}
        all_students      = sorted list of all registered student IDs
        total_faces_found = kitne faces image mein mile
    """
    student_map = _build_student_map()
    all_students = sorted(student_map.keys())

    embeddings = get_face_embeddings(class_image)
    total_faces = len(embeddings)

    print(f"DEBUG: Registered students = {len(all_students)}, IDs = {all_students}")
    print(f"DEBUG: Faces detected in image = {total_faces}")

    if not student_map:
        print("DEBUG: DB mein koi student nahi hai")
        return {}, all_students, total_faces

    detected_students: dict[int, float] = {}

    for emb in embeddings:
        sid, score = _match_face(emb, student_map, threshold)

        print(f"DEBUG: predicted_sid={sid}, cosine_score={score:.4f}, threshold={threshold}")

        if sid is not None:
            # Ek student multiple baar detect ho sakta hai → best score rakho
            if sid not in detected_students or score > detected_students[sid]:
                detected_students[sid] = score

    return detected_students, all_students, total_faces


# ─────────────────────────────────────────────
# Registration helper (naye student ka embedding save karna)
# ─────────────────────────────────────────────

def get_registration_embedding(image: np.ndarray) -> np.ndarray | None:
    """
    Registration ke time: image se pehla face ka embedding nikaalo.
    Ye embedding DB mein store karo.

    Returns:
        512-d normalized numpy array, ya None agar face nahi mila
    """
    embeddings = get_face_embeddings(image)

    if not embeddings:
        st.warning("Koi face detect nahi hua. Seedha camera mein dekho aur achhi light lo.")
        return None

    if len(embeddings) > 1:
        st.warning(f"{len(embeddings)} faces mile. Sirf apna face frame mein rakho.")
        return None

    return embeddings[0]