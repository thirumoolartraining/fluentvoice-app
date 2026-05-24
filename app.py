import streamlit as st
import requests
from datetime import datetime


API_URL = "https://ramlakshman-fluentvoice-api.hf.space/analyze"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FluentVoice",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "**FluentVoice** — AI-powered stuttering & fluency analysis.",
    },
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  :root {
    --primary: #1B2B5E;
    --accent:  #C9A84C;
    --bg:      #F5F7FA;
    --card:    #FFFFFF;
    --text:    #1A1A2E;
  }

  .stApp { background-color: var(--bg); }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background-color: var(--primary) !important;
  }
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] li,
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
    color: #FFFFFF !important;
  }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stTextInput label {
    color: #C9A84C !important;
    font-weight: 600;
  }
  [data-testid="stSidebar"] input,
  [data-testid="stSidebar"] textarea {
    color: #1A1A2E !important;
    background-color: #FFFFFF !important;
  }
  [data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1A1A2E !important;
  }
  [data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #1A1A2E !important;
  }
  [data-testid="stSidebar"] [data-baseweb="menu"] * {
    color: #1A1A2E !important;
  }

  /* ── Headings (main content only) ── */
  .main h1, .main h2, .main h3,
  [data-testid="stMainBlockContainer"] h1,
  [data-testid="stMainBlockContainer"] h2,
  [data-testid="stMainBlockContainer"] h3 {
    color: var(--primary);
  }

  /* ── Metric cards ── */
  [data-testid="metric-container"] {
    background: var(--card);
    border: 1px solid #E0E4EF;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,.06);
  }
  [data-testid="metric-container"] label {
    color: var(--primary) !important;
    font-weight: 600;
  }

  /* ── Main area inputs ── */
  [data-testid="stMainBlockContainer"] input,
  [data-testid="stMainBlockContainer"] textarea {
    color: #1A1A2E !important;
  }
  [data-testid="stMainBlockContainer"] label {
    color: var(--primary) !important;
    font-weight: 500;
  }

  /* ── Buttons ── */
  .stButton > button {
    background-color: var(--accent);
    color: var(--primary);
    border: none;
    font-weight: 700;
    border-radius: 8px;
    padding: 0.5rem 1.6rem;
    transition: opacity .2s;
  }
  .stButton > button:hover { opacity: .85; }

  /* ── Severity badges ── */
  .badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: .5px;
  }
  .badge-mild     { background: #D4EDDA; color: #155724; }
  .badge-moderate { background: #FFF3CD; color: #856404; }
  .badge-severe   { background: #F8D7DA; color: #721C24; }

  /* ── Disfluency timeline pills ── */
  .pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: .82rem;
    font-weight: 600;
    margin: 2px 4px 2px 0;
  }

  /* ── Session card (therapist list) ── */
  .session-card {
    background: var(--card);
    border-left: 4px solid var(--accent);
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: .88rem;
    color: var(--text) !important;
  }
  .session-card * { color: var(--text) !important; }
  .session-card.selected {
    border-left-color: var(--primary);
    background: #EEF1FA;
  }

  /* ── Transcript ── */
  .transcript-box {
    background: var(--card);
    border: 1px solid #D0D5E8;
    border-radius: 8px;
    padding: 16px 20px;
    font-size: .95rem;
    line-height: 1.7;
    color: var(--text);
  }

  /* ── Insight items ── */
  .insight-item {
    background: #EEF1FA;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: .92rem;
    color: var(--text);
  }

  /* ── Role toggle buttons (inside columns in sidebar) ── */
  [data-testid="stSidebar"] [data-testid="stColumn"] button[data-testid="baseButton-secondary"] {
    background-color: rgba(255,255,255,0.10) !important;
    color: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.45rem 0;
    width: 100%;
  }
  [data-testid="stSidebar"] [data-testid="stColumn"] button[data-testid="baseButton-secondary"]:hover {
    background-color: rgba(255,255,255,0.18) !important;
    color: #fff !important;
    opacity: 1 !important;
  }
  [data-testid="stSidebar"] [data-testid="stColumn"] button[data-testid="baseButton-primary"] {
    background-color: #C9A84C !important;
    color: #1B2B5E !important;
    border: none !important;
    font-weight: 700;
    border-radius: 8px;
    padding: 0.45rem 0;
    width: 100%;
    opacity: 1 !important;
  }
  [data-testid="stSidebar"] [data-testid="stColumn"] button:hover {
    opacity: 1 !important;
  }

  /* ── Therapist session list ── */
  .therapist-list-btn > div > button {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1px solid #E0E4EF !important;
    border-left: 4px solid var(--accent) !important;
    border-radius: 6px !important;
    text-align: left !important;
    padding: 10px 14px !important;
    font-weight: normal !important;
    white-space: pre-wrap !important;
    line-height: 1.6 !important;
    width: 100% !important;
  }
  .therapist-list-btn > div > button:hover {
    background: #EEF1FA !important;
    opacity: 1 !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("logged_in", False),
    ("name", ""),
    ("role", "Patient"),
    ("_role_choice", "Patient"),
    ("all_sessions", []),
    ("last_result", None),
    ("selected_session_idx", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Constants ─────────────────────────────────────────────────────────────────
DISFLUENCY_ICONS = {
    "block":        "🔴",
    "word_rep":     "🟡",
    "sound_rep":    "🟠",
    "prolongation": "🟣",
    "interjection": "⚪",
    "pause":        "⏸",
}
PILL_COLORS = {
    "block":        "#FFDEDE",
    "word_rep":     "#FFF5CC",
    "sound_rep":    "#FFE8D0",
    "prolongation": "#F0E6FF",
    "interjection": "#F0F0F0",
    "pause":        "#E6F4FF",
}
PILL_TEXT_COLORS = {
    "block":        "#900",
    "word_rep":     "#765000",
    "sound_rep":    "#7A3800",
    "prolongation": "#5A0090",
    "interjection": "#555",
    "pause":        "#005A90",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def severity_badge(severity: str) -> str:
    cls = f"badge-{severity.lower()}" if severity.lower() in ("mild", "moderate", "severe") else "badge-mild"
    return f'<span class="badge {cls}">{severity.upper()}</span>'


def call_api(audio_bytes: bytes, filename: str) -> dict:
    resp = requests.post(
        API_URL,
        files={"audio": (filename, audio_bytes)},
        data={
            "condition_on_previous_text": "false",
            "no_speech_threshold": "0.6",
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def save_session(patient_name: str, filename: str, audio_bytes: bytes, report: dict):
    st.session_state.all_sessions.append({
        "patient_name": patient_name,
        "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M"),
        "filename":     filename,
        "audio_bytes":  audio_bytes,
        "report":       report,
        "notes":        "",
    })


def analyze_and_save(audio_bytes: bytes, filename: str, patient_name: str):
    with st.spinner("Analyzing audio — this may take 15–30 seconds…"):
        try:
            result = call_api(audio_bytes, filename)
            st.session_state.last_result = result
            save_session(patient_name, filename, audio_bytes, result)
            st.success("Analysis complete!")
        except requests.exceptions.Timeout:
            st.error("The API timed out. Please try a shorter audio clip.")
        except requests.exceptions.RequestException as e:
            st.error(f"API error: {e}")


def generate_insights(result: dict) -> list[str]:
    insights = []

    rate = result.get("speech_rate", 0)
    if rate > 300:
        insights.append("⚠️ Speech rate could not be calculated reliably for this sample.")
    elif rate < 100:
        insights.append(f"🐢 Speech rate is **{rate:.0f} wpm** — notably slow, which may indicate frequent pauses or blocks.")
    elif rate < 140:
        insights.append(f"✅ Speech rate is **{rate:.0f} wpm** — within the typical fluent range (100–160 wpm).")
    elif rate < 180:
        insights.append(f"⚡ Speech rate is **{rate:.0f} wpm** — slightly fast; breath support may be strained.")
    else:
        insights.append(f"🚀 Speech rate is **{rate:.0f} wpm** — very fast; intelligibility could be affected.")

    disf = result.get("disfluencies", [])
    transcript = result.get("transcript", "")
    word_count = len(transcript.split()) if transcript else 1
    disf_rate = (len(disf) / word_count * 100) if word_count else 0
    if disf_rate < 3:
        insights.append(f"👍 Disfluency rate is **{disf_rate:.1f}%** — typical conversational speech.")
    elif disf_rate < 10:
        insights.append(f"⚠️ Disfluency rate is **{disf_rate:.1f}%** — mild disruption to fluency.")
    else:
        insights.append(f"🔔 Disfluency rate is **{disf_rate:.1f}%** — frequent disruptions detected.")

    if disf:
        counts: dict[str, int] = {}
        for d in disf:
            t = d.get("event") or d.get("type", "unknown")
            counts[t] = counts.get(t, 0) + 1
        dominant = max(counts, key=lambda k: counts[k])
        icon = DISFLUENCY_ICONS.get(dominant, "❓")
        insights.append(f"{icon} Dominant disfluency: **{dominant.replace('_', ' ').title()}** ({counts[dominant]} occurrences).")

    pauses = result.get("pauses", 0)
    if isinstance(pauses, list):
        pauses = len(pauses)
    if pauses > 5:
        insights.append(f"⏸ **{pauses} notable pauses** detected — may reflect word-finding difficulty or blocking.")

    return insights


def render_analysis(result: dict, patient_name: str = ""):
    score        = result.get("fluency_score", 0)
    severity     = result.get("severity", "Unknown")
    rate         = result.get("speech_rate", 0)
    transcript   = result.get("transcript", "")
    disfluencies = result.get("disfluencies", [])
    pauses_raw   = result.get("pauses", 0)
    pause_count  = len(pauses_raw) if isinstance(pauses_raw, list) else pauses_raw
    timeline     = result.get("timeline", [])

    if patient_name:
        st.markdown(f"### Analysis — {patient_name}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fluency Score", f"{score:.1f} / 100")
    c2.metric("Speech Rate", f"{rate:.0f} wpm" if rate <= 300 else "Unable to calculate")
    c3.metric("Disfluencies", len(disfluencies))
    c4.metric("Pauses", pause_count)

    st.markdown(f"**Severity:** {severity_badge(severity)}", unsafe_allow_html=True)
    st.divider()

    with st.expander("📝 Transcript", expanded=True):
        if transcript:
            st.markdown(f'<div class="transcript-box">{transcript}</div>', unsafe_allow_html=True)
        else:
            st.info("No transcript available.")

    with st.expander("📊 Disfluency Timeline", expanded=True):
        events = timeline if timeline else disfluencies
        if events:
            pills_html = ""
            for ev in events:
                t    = ev.get("event") or ev.get("type", "unknown")
                ts   = ev.get("time") or ev.get("start") or ev.get("timestamp", "")
                word = ev.get("word", "")
                icon = DISFLUENCY_ICONS.get(t, "❓")
                bg   = PILL_COLORS.get(t, "#EEE")
                fg   = PILL_TEXT_COLORS.get(t, "#333")
                label = f"{icon} {t.replace('_', ' ')}"
                if word:
                    label += f' "{word}"'
                if ts != "":
                    label += f" @{ts}"
                pills_html += f'<span class="pill" style="background:{bg};color:{fg}">{label}</span>'
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.success("No disfluency events detected.")

    with st.expander("💡 Automated Insights", expanded=True):
        for ins in generate_insights(result):
            st.markdown(f'<div class="insight-item">{ins}</div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎙️ FluentVoice")
    st.markdown("---")

    if not st.session_state.logged_in:
        st.markdown("### Sign In")
        name_input = st.text_input("Your Name", placeholder="e.g. Jane Doe")

        st.markdown('<p style="margin:12px 0 6px;font-size:.85rem;color:#C9A84C;font-weight:600">I am a</p>', unsafe_allow_html=True)
        col_p, col_t = st.columns(2, gap="small")
        with col_p:
            if st.button(
                "👤 Patient",
                key="toggle_patient",
                use_container_width=True,
                type="primary" if st.session_state.get("_role_choice", "Patient") == "Patient" else "secondary",
            ):
                st.session_state._role_choice = "Patient"
                st.rerun()
        with col_t:
            if st.button(
                "🩺 Therapist",
                key="toggle_therapist",
                use_container_width=True,
                type="primary" if st.session_state.get("_role_choice", "Patient") == "Therapist" else "secondary",
            ):
                st.session_state._role_choice = "Therapist"
                st.rerun()

        role_input = st.session_state.get("_role_choice", "Patient")
        st.markdown("")
        if st.button("Continue →", use_container_width=True):
            if name_input.strip():
                st.session_state.name      = name_input.strip()
                st.session_state.role      = role_input
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Please enter your name.")
    else:
        st.markdown(f"**👤 {st.session_state.name}**")
        st.markdown(f"*{st.session_state.role}*")
        session_count = len(st.session_state.all_sessions)
        if session_count:
            st.markdown(f"*{session_count} session{'s' if session_count != 1 else ''} recorded*")
        if st.button("Sign out"):
            for k in ("logged_in", "name", "role", "last_result", "selected_session_idx"):
                st.session_state[k] = False if k == "logged_in" else (None if k in ("last_result", "selected_session_idx") else "")
            st.rerun()

# ── Landing (not logged in) ───────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown(
        """
        <div style="text-align:center;padding:60px 0 20px">
          <h1 style="font-size:2.8rem;color:#1B2B5E">🎙️ FluentVoice</h1>
          <p style="font-size:1.2rem;color:#555;max-width:540px;margin:0 auto">
            AI-powered stuttering &amp; fluency analysis.<br>
            Upload or record a voice sample and get instant clinical insights.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.columns([1, 2, 1])[1].info("👈 Sign in from the sidebar to get started.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# PATIENT VIEW
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.role == "Patient":
    st.markdown("# 🎙️ FluentVoice — Patient Dashboard")

    tab_upload, tab_record = st.tabs(["📁 Upload Audio", "🎙️ Record Audio"])

    # ── Tab 1: Upload ──────────────────────────────────────────────────────────
    with tab_upload:
        audio_file = st.file_uploader(
            "Choose a WAV, MP3, or M4A file",
            type=["wav", "mp3", "m4a"],
            label_visibility="collapsed",
        )
        upload_bytes = None
        upload_name  = None
        if audio_file is not None:
            upload_bytes = audio_file.read()
            upload_name  = audio_file.name
            st.audio(upload_bytes, format=audio_file.type)

        if st.button("🔍 Analyze Speech", disabled=(upload_bytes is None), key="analyze_upload"):
            analyze_and_save(upload_bytes, upload_name, st.session_state.name)

    # ── Tab 2: Record ──────────────────────────────────────────────────────────
    with tab_record:
        st.markdown("**Press the microphone button below to start recording. Press again to stop.**")

        audio_input = st.audio_input("Record your voice", key="native_recorder", label_visibility="collapsed")

        recorded_bytes = None
        if audio_input is not None:
            recorded_bytes = audio_input.read()
            st.success("✅ Recording captured — ready to analyze.")

        if st.button(
            "🔍 Analyze Speech",
            disabled=(recorded_bytes is None),
            key="analyze_record",
        ):
            analyze_and_save(recorded_bytes, "recording.wav", st.session_state.name)

    # ── Latest result ──────────────────────────────────────────────────────────
    if st.session_state.last_result:
        st.divider()
        render_analysis(st.session_state.last_result)


# ═══════════════════════════════════════════════════════════════════════════════
# THERAPIST VIEW
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("# 🎙️ FluentVoice — Therapist Dashboard")

    sessions = st.session_state.all_sessions

    if not sessions:
        st.info("No sessions recorded yet. Ask a patient to analyze a sample first.")
        st.stop()

    col_list, col_report = st.columns([1, 2], gap="large")

    # ── Left: session list ────────────────────────────────────────────────────
    with col_list:
        st.markdown("### 📋 Patient Sessions")
        st.caption(f"{len(sessions)} session{'s' if len(sessions) != 1 else ''} total")

        for i in range(len(sessions) - 1, -1, -1):   # newest first
            sess  = sessions[i]
            score = sess["report"].get("fluency_score", 0)
            sev   = sess["report"].get("severity", "?").title()
            is_sel = st.session_state.selected_session_idx == i

            badge_colors = {"Mild": "#D4EDDA", "Moderate": "#FFF3CD", "Severe": "#F8D7DA"}
            badge_text   = {"Mild": "#155724",  "Moderate": "#856404",  "Severe": "#721C24"}
            bc = badge_colors.get(sev, "#E0E4EF")
            bt = badge_text.get(sev, "#333")

            selected_style = "border-left: 4px solid #1B2B5E; background: #EEF1FA;" if is_sel else "border-left: 4px solid #C9A84C; background: #FFFFFF;"

            st.markdown(
                f'<div class="session-card {"selected" if is_sel else ""}" style="{selected_style}">'
                f'<b>{sess["patient_name"]}</b><br>'
                f'<span style="font-size:.8rem;color:#666">{sess["timestamp"]}</span><br>'
                f'<span style="font-size:.85rem">Score: <b>{score:.1f}</b> &nbsp;'
                f'<span style="background:{bc};color:{bt};padding:1px 8px;border-radius:10px;font-size:.78rem;font-weight:700">{sev}</span></span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            with st.container():
                st.markdown('<div class="therapist-list-btn">', unsafe_allow_html=True)
                if st.button(
                    "▶ View Report" if not is_sel else "✓ Selected",
                    key=f"view_{i}",
                    use_container_width=True,
                ):
                    st.session_state.selected_session_idx = i
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # ── Right: full report ────────────────────────────────────────────────────
    with col_report:
        idx = st.session_state.selected_session_idx

        if idx is None or not (0 <= idx < len(sessions)):
            st.markdown(
                """
                <div style="text-align:center;padding:80px 0;color:#888">
                  <div style="font-size:3rem">📋</div>
                  <div style="font-size:1.1rem;margin-top:12px">Select a session from the left to view the full report</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            sess = sessions[idx]
            st.markdown(f"### {sess['patient_name']} &nbsp; <span style='font-size:.9rem;color:#888;font-weight:400'>{sess['timestamp']}</span>", unsafe_allow_html=True)
            st.markdown(f"📄 *{sess['filename']}*")

            # Audio playback
            st.audio(sess["audio_bytes"], format="audio/wav")

            render_analysis(sess["report"])

            # ── Manual review notes ────────────────────────────────────────
            st.markdown("---")
            st.markdown("### 📝 Manual Review Notes")
            notes = st.text_area(
                "Add your clinical observations for this session",
                value=sess.get("notes", ""),
                height=140,
                placeholder="e.g. Patient shows improvement in block frequency. Recommend breathing exercises...",
                key=f"notes_{idx}",
            )
            if st.button("💾 Save Notes", key=f"save_notes_{idx}"):
                st.session_state.all_sessions[idx]["notes"] = notes
                st.success("Notes saved!")
