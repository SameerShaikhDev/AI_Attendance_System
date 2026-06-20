import streamlit as st

from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(voice: bytes) -> list | None:
    """
    Audio bytes se speaker embedding nikalo.
    Returns: 256-d list (resemblyzer), ya None agar error ho
    """
    try:
        encoder = load_voice_encoder()
        wav = preprocess_wav(io.BytesIO(voice))
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f"Voice embedding error: {e}")
        return None


def identify_speaker(
    new_embedding: list,
    candidate_dict: dict,
    threshold: float = 0.65,
) -> tuple[str | None, float]:
    """
    Ek embedding ko stored embeddings se match karo.

    Args:
        new_embedding  : query embedding (list ya np.array)
        candidate_dict : {student_id: stored_embedding}
        threshold      : cosine similarity cutoff

    Returns:
        (student_id, best_score) ya (None, best_score)
    """
    if new_embedding is None or not candidate_dict:
        return None, 0.0

    query = np.array(new_embedding)
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidate_dict.items():
        if stored_embedding is not None:
            score = float(np.dot(query, np.array(stored_embedding)))
            if score > best_score:
                best_score = score
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_teacher_audio(
    audio: bytes,
    candidate_dict: dict,
    threshold: float = 0.65,
) -> dict:
    """
    Teacher ki recording mein se alag alag students ki awaaz pehchano.
    Audio ko segments mein split karta hai, har segment match karta hai.

    Args:
        audio          : raw audio bytes
        candidate_dict : {student_id: stored_embedding}
        threshold      : cosine similarity cutoff

    Returns:
        {student_id: best_score} — jinki awaaz mili
    """
    try:
        encoder = load_voice_encoder()

        audio_array, sr = librosa.load(io.BytesIO(audio), sr=16000)
        segments = librosa.effects.split(audio_array, top_db=30)

        # ── naam fix: 'detected_speakers' — 'identify_student' se conflict tha ──
        detected_speakers: dict = {}

        for start, end in segments:
            # 0.5 second se chote segments skip karo (noise/silence)
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio_array[start:end]

            # resemblyzer numpy array directly accept karta hai
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding.tolist(), candidate_dict, threshold)

            if sid is not None:
                if sid not in detected_speakers or score > detected_speakers[sid]:
                    detected_speakers[sid] = score

        return detected_speakers

    except Exception as e:
        st.error(f"Teacher audio processing error: {e}")
        return {}