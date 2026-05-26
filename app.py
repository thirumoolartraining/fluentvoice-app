import re
import math
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

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  box-sizing: border-box;
}

/* ── App background ── */
.stApp { background: #EEF2FF !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #0D1B3E 0%, #1B2B5E 55%, #1F3070 100%) !important;
  border-right: 1px solid rgba(201,168,76,0.2) !important;
}
[data-testid="stSidebar"] > div:first-child::before {
  content: '';
  display: block;
  height: 3px;
  background: linear-gradient(90deg, #C9A84C 0%, #F0D080 50%, #C9A84C 100%);
  border-radius: 0 0 2px 2px;
  margin-bottom: 4px;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
  color: rgba(255,255,255,0.9) !important;
}
[data-testid="stSidebar"] .stTextInput label {
  color: #C9A84C !important;
  font-weight: 600 !important;
  font-size: .78rem !important;
  text-transform: uppercase !important;
  letter-spacing: .6px !important;
}
[data-testid="stSidebar"] input {
  color: #1A1A2E !important;
  background: rgba(255,255,255,0.97) !important;
  border: 1.5px solid rgba(201,168,76,0.35) !important;
  border-radius: 10px !important;
  font-size: .95rem !important;
}
[data-testid="stSidebar"] input:focus {
  border-color: #C9A84C !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.15) !important;
}

/* Role toggle */
[data-testid="stSidebar"] [data-testid="stColumn"] button[data-testid="baseButton-secondary"] {
  background: rgba(255,255,255,0.08) !important;
  color: rgba(255,255,255,0.65) !important;
  border: 1.5px solid rgba(255,255,255,0.15) !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: .88rem !important;
  padding: 0.5rem 0 !important;
  transition: all .2s !important;
}
[data-testid="stSidebar"] [data-testid="stColumn"] button[data-testid="baseButton-secondary"]:hover {
  background: rgba(255,255,255,0.14) !important;
  color: #fff !important;
  opacity: 1 !important;
}
[data-testid="stSidebar"] [data-testid="stColumn"] button[data-testid="baseButton-primary"] {
  background: linear-gradient(135deg, #C9A84C 0%, #E8C96A 100%) !important;
  color: #1B2B5E !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  font-size: .88rem !important;
  padding: 0.5rem 0 !important;
  box-shadow: 0 4px 14px rgba(201,168,76,0.45) !important;
  opacity: 1 !important;
}
[data-testid="stSidebar"] [data-testid="stColumn"] button:hover { opacity: 1 !important; }

/* Sidebar action buttons (Continue / Sign out) */
[data-testid="stSidebar"] .stButton > button:not([data-testid="baseButton-primary"]):not([data-testid="baseButton-secondary"]) {
  background: linear-gradient(135deg, #C9A84C, #E8C96A) !important;
  color: #1B2B5E !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  width: 100% !important;
  padding: 0.55rem 1rem !important;
  box-shadow: 0 4px 14px rgba(201,168,76,0.35) !important;
  transition: all .2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover { opacity: .9 !important; }

/* ── Main content headings ── */
[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3 {
  color: #1B2B5E !important;
  font-weight: 700 !important;
  letter-spacing: -.3px;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
  background: rgba(255,255,255,0.75) !important;
  border-radius: 14px !important;
  padding: 5px !important;
  border: 1px solid rgba(27,43,94,0.08) !important;
  gap: 4px !important;
}
[data-testid="stTabs"] button[role="tab"] {
  border-radius: 10px !important;
  font-weight: 600 !important;
  color: #6B7280 !important;
  padding: 9px 22px !important;
  font-size: .9rem !important;
  transition: all .2s !important;
  border: none !important;
  border-bottom: none !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  background: white !important;
  color: #1B2B5E !important;
  box-shadow: 0 2px 10px rgba(27,43,94,0.12) !important;
  border-bottom: none !important;
}
/* Hide BaseUI's default red/orange tab highlight bar */
[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] {
  display: none !important;
  height: 0 !important;
  background: transparent !important;
}

/* ── Main buttons ── */
[data-testid="stMainBlockContainer"] .stButton > button {
  background: linear-gradient(135deg, #1B2B5E 0%, #2D44A0 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-size: .95rem !important;
  padding: 0.65rem 2.2rem !important;
  box-shadow: 0 4px 18px rgba(27,43,94,0.28) !important;
  transition: all .2s !important;
  letter-spacing: .2px;
}
[data-testid="stMainBlockContainer"] .stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(27,43,94,0.38) !important;
  opacity: 1 !important;
}
[data-testid="stMainBlockContainer"] .stButton > button:disabled {
  background: #D1D5DB !important;
  color: #9CA3AF !important;
  box-shadow: none !important;
  transform: none !important;
}

/* Save Notes button — secondary gold */
button[kind="secondary"],
[data-testid="stMainBlockContainer"] .stButton > button[data-testid="baseButton-secondary"] {
  background: linear-gradient(135deg, #C9A84C, #E8C96A) !important;
  color: #1B2B5E !important;
  box-shadow: 0 4px 14px rgba(201,168,76,0.3) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: white !important;
  border: 2px dashed rgba(201,168,76,0.6) !important;
  border-radius: 16px !important;
  transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: #C9A84C !important; }

/* File uploader browse button — needs 3-attribute specificity to beat the main button rule */
[data-testid="stMainBlockContainer"] [data-testid="stFileUploader"] button,
[data-testid="stMainBlockContainer"] [data-testid="stFileUploader"] .stButton > button,
[data-testid="stMainBlockContainer"] [data-testid="stFileUploadDropzone"] button {
  background: white !important;
  color: #374151 !important;
  border: 1.5px solid #D4D9EE !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: .82rem !important;
  padding: 0.38rem 1.1rem !important;
  box-shadow: none !important;
  transform: none !important;
  width: auto !important;
  min-width: 0 !important;
  letter-spacing: 0 !important;
  line-height: 1.4 !important;
}
[data-testid="stMainBlockContainer"] [data-testid="stFileUploader"] button:hover,
[data-testid="stMainBlockContainer"] [data-testid="stFileUploader"] .stButton > button:hover,
[data-testid="stMainBlockContainer"] [data-testid="stFileUploadDropzone"] button:hover {
  background: #F0F4FF !important;
  border-color: #1B2B5E !important;
  transform: none !important;
  box-shadow: none !important;
  opacity: 1 !important;
}

/* ── Audio input ── */
[data-testid="stAudioInput"] {
  background: white !important;
  border: 2px solid rgba(27,43,94,0.1) !important;
  border-radius: 16px !important;
  padding: 8px !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
  background: white !important;
  border: 1px solid rgba(27,43,94,0.07) !important;
  border-radius: 18px !important;
  margin-bottom: 14px !important;
  overflow: hidden !important;
  box-shadow: 0 2px 12px rgba(27,43,94,0.06) !important;
  transition: box-shadow .2s !important;
}
[data-testid="stExpander"]:hover { box-shadow: 0 4px 20px rgba(27,43,94,0.1) !important; }
[data-testid="stExpander"] summary {
  padding: 18px 22px !important;
  font-weight: 700 !important;
  color: #1B2B5E !important;
  font-size: .97rem !important;
  background: white !important;
}
[data-testid="stExpander"] > div > div { padding: 0 22px 18px !important; }

/* ── Main inputs / textarea ── */
[data-testid="stMainBlockContainer"] input,
[data-testid="stMainBlockContainer"] textarea {
  color: #1A1A2E !important;
  border-radius: 10px !important;
  border: 1.5px solid #D4D9EE !important;
  font-size: .93rem !important;
}
[data-testid="stMainBlockContainer"] input:focus,
[data-testid="stMainBlockContainer"] textarea:focus {
  border-color: #1B2B5E !important;
  box-shadow: 0 0 0 3px rgba(27,43,94,0.1) !important;
}
[data-testid="stMainBlockContainer"] label {
  color: #374151 !important;
  font-weight: 600 !important;
  font-size: .85rem !important;
  text-transform: uppercase !important;
  letter-spacing: .4px !important;
}

/* ── Alert / info ── */
[data-testid="stAlert"] { border-radius: 12px !important; font-weight: 500 !important; }

/* ── Divider ── */
hr { border-color: rgba(27,43,94,0.08) !important; margin: 24px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(27,43,94,0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(27,43,94,0.35); }
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
    "block":        "#FFE4E4",
    "word_rep":     "#FFF8CC",
    "sound_rep":    "#FFE8D0",
    "prolongation": "#EDE9FF",
    "interjection": "#F3F4F6",
    "pause":        "#E0F0FF",
}
PILL_TEXT_COLORS = {
    "block":        "#991B1B",
    "word_rep":     "#78350F",
    "sound_rep":    "#7C2D12",
    "prolongation": "#4C1D95",
    "interjection": "#374151",
    "pause":        "#1E40AF",
}
PILL_BORDER = {
    "block":        "#FCA5A5",
    "word_rep":     "#FCD34D",
    "sound_rep":    "#FDBA74",
    "prolongation": "#C4B5FD",
    "interjection": "#D1D5DB",
    "pause":        "#93C5FD",
}

# ── HTML component helpers ────────────────────────────────────────────────────

def _md_bold(text: str) -> str:
    """Convert **bold** markdown to HTML <strong>."""
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)


def fluency_gauge_html(score: float) -> str:
    r = 42
    circ = 2 * math.pi * r
    pct  = max(0.0, min(score / 100.0, 1.0))
    offset = circ * (1 - pct)
    if score >= 70:
        ring_color, grade, grade_color = "#10B981", "Good", "#10B981"
    elif score >= 40:
        ring_color, grade, grade_color = "#F59E0B", "Fair", "#F59E0B"
    else:
        ring_color, grade, grade_color = "#EF4444", "Low", "#EF4444"
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px">
      <svg width="160" height="160" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="#E8EDF5" stroke-width="10"/>
        <circle cx="50" cy="50" r="{r}" fill="none" stroke="{ring_color}" stroke-width="10"
          stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"
          stroke-linecap="round" transform="rotate(-90 50 50)"/>
        <text x="50" y="43" text-anchor="middle" font-size="24" font-weight="800"
          fill="#1B2B5E" font-family="Inter,sans-serif">{score:.0f}</text>
        <text x="50" y="56" text-anchor="middle" font-size="9" fill="#9CA3AF"
          font-family="Inter,sans-serif">out of 100</text>
        <text x="50" y="70" text-anchor="middle" font-size="11" font-weight="700"
          fill="{grade_color}" font-family="Inter,sans-serif">{grade}</text>
      </svg>
      <span style="font-size:.72rem;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:.8px">Fluency Score</span>
    </div>"""


def severity_banner_html(severity: str) -> str:
    cfg = {
        "mild":     ("#ECFDF5", "#10B981", "#065F46", "✅", "Mild Stuttering",     "Typical disfluency — within manageable range."),
        "moderate": ("#FFFBEB", "#F59E0B", "#78350F", "⚠️","Moderate Stuttering", "Noticeable disruptions — therapy is recommended."),
        "severe":   ("#FFF5F5", "#EF4444", "#7F1D1D", "🔴","Severe Stuttering",   "Significant impact on communication — seek specialist care."),
    }
    bg, border, text, icon, label, sub = cfg.get(
        severity.lower(),
        ("#F0F4FF", "#1B2B5E", "#1B2B5E", "📊", severity.title(), "Fluency analysis complete.")
    )
    return f"""
    <div style="background:{bg};border:1.5px solid {border};
      border-radius:16px;padding:18px 22px;margin:18px 0 6px;
      display:flex;align-items:center;gap:16px;
      box-shadow:0 2px 12px {border}22">
      <span style="font-size:2.2rem;line-height:1">{icon}</span>
      <div>
        <div style="font-size:1.05rem;font-weight:800;color:{text};letter-spacing:-.2px">{label}</div>
        <div style="font-size:.83rem;color:{text};opacity:.75;margin-top:3px">{sub}</div>
      </div>
    </div>"""


def metric_cards_html(score: float, rate: float, disf_count: int, pause_count: int) -> str:
    rate_val = f"{rate:.0f}" if rate <= 300 else "N/A"
    cards = [
        ("🎯", f"{score:.1f}", "Fluency Score",  "#1B2B5E", f"Fluency score is {score:.1f} out of 100"),
        ("💬", rate_val,       "Speech Rate",  "#6366F1", f"Speech rate is {rate_val} words per minute"),
        ("⚡", str(disf_count),"Disfluencies", "#F59E0B", f"Detected {disf_count} disfluency events"),
        ("⏸", str(pause_count),"Pauses",       "#EC4899", f"Detected {pause_count} pause events"),
    ]
    inner = ""
    for icon, val, label, color, aria_label in cards:
        inner += f"""
        <div role="region" aria-label="{aria_label}" style="background:white;border-radius:18px;padding:20px 16px;text-align:center;
          box-shadow:0 2px 12px rgba(27,43,94,0.06);border:1.5px solid #E8EDF5;transition:all .2s">
          <div style="font-size:1.6rem;margin-bottom:8px" aria-hidden="true">{icon}</div>
          <div style="font-size:2rem;font-weight:900;color:{color};line-height:1;letter-spacing:-1px">{val}</div>
          <div style="font-size:.7rem;font-weight:700;color:#6B7280;text-transform:uppercase;
            letter-spacing:.6px;margin-top:12px">{label}</div>
        </div>"""
    return f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0">{inner}</div>'


def insight_card_html(text: str) -> str:
    border_map = {
        "🐢": "#6366F1", "✅": "#10B981", "⚡": "#F59E0B", "🚀": "#EF4444",
        "👍": "#10B981", "⚠️": "#F59E0B", "🔔": "#EF4444",
        "🔴": "#EF4444", "🟡": "#F59E0B", "🟠": "#F97316",
        "🟣": "#8B5CF6", "⏸": "#6366F1",
    }
    color = next((c for k, c in border_map.items() if text.startswith(k)), "#1B2B5E")
    return f"""
    <div style="background:white;border-radius:12px;padding:14px 18px;margin-bottom:10px;
      border-left:4px solid {color};box-shadow:0 2px 8px rgba(27,43,94,0.05);
      font-size:.91rem;color:#374151;line-height:1.6">{_md_bold(text)}</div>"""


def patient_avatar_html(name: str) -> str:
    initials = "".join(w[0].upper() for w in name.split()[:2]) if name else "?"
    palette  = ["#6366F1","#8B5CF6","#EC4899","#EF4444","#F59E0B","#10B981","#3B82F6","#0891B2"]
    color    = palette[hash(name) % len(palette)] if name else "#6366F1"
    return (f'<div style="width:46px;height:46px;border-radius:14px;background:{color};'
            f'display:flex;align-items:center;justify-content:center;color:white;'
            f'font-weight:800;font-size:1rem;flex-shrink:0;letter-spacing:.5px">{initials}</div>')


def page_header_html(title: str, subtitle: str) -> str:
    return f"""
    <div style="background:linear-gradient(135deg,#1B2B5E 0%,#2D44A0 100%);border-radius:22px;
      padding:30px 36px;margin-bottom:28px;position:relative;overflow:hidden">
      <div style="position:absolute;top:-30px;right:-30px;width:150px;height:150px;
        border-radius:50%;background:rgba(201,168,76,0.12)"></div>
      <div style="position:absolute;bottom:-40px;right:80px;width:100px;height:100px;
        border-radius:50%;background:rgba(201,168,76,0.07)"></div>
      <div style="position:relative">
        <h1 style="color:white;font-size:1.75rem;font-weight:800;margin:0 0 6px;letter-spacing:-.4px">{title}</h1>
        <p style="color:rgba(255,255,255,0.65);margin:0;font-size:.92rem;font-weight:400">{subtitle}</p>
      </div>
    </div>"""


# ── Core helpers ──────────────────────────────────────────────────────────────

def call_api(audio_bytes: bytes, filename: str) -> dict:
    """Call the FluentVoice API with proper error handling."""
    if not audio_bytes or len(audio_bytes) == 0:
        raise ValueError("Audio file is empty. Please record or upload audio.")

    try:
        resp = requests.post(
            API_URL,
            files={"audio": (filename, audio_bytes)},
            data={"condition_on_previous_text": "false", "no_speech_threshold": "0.6"},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Cannot reach the API. Please check your internet connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError("The API took too long to respond. Please try a shorter audio clip.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            raise ValueError("Audio format not supported. Please try MP3, WAV, or OGG.")
        elif e.response.status_code == 429:
            raise RuntimeError("API rate limit exceeded. Please wait a moment and try again.")
        elif e.response.status_code >= 500:
            raise RuntimeError("The API is temporarily unavailable. Please try again in a moment.")
        else:
            raise RuntimeError(f"API error: {e.response.status_code}")
    except ValueError as e:
        raise ValueError(f"Invalid API response: {str(e)}")


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
    """Analyze audio and save session with error recovery."""
    if not patient_name or not patient_name.strip():
        st.error("⚠️ Please enter your name before analyzing.")
        return

    with st.spinner("Analyzing audio — this may take 15–30 seconds…"):
        try:
            result = call_api(audio_bytes, filename)
            st.session_state.last_result = result
            save_session(patient_name, filename, audio_bytes, result)
            st.success("✅ Analysis complete! Your results are ready below.")
        except ValueError as e:
            st.error(f"⚠️ {str(e)}")
        except (TimeoutError, ConnectionError, RuntimeError) as e:
            st.error(f"📡 {str(e)}")
        except Exception as e:
            st.error(f"🔧 Unexpected error. Please try again or contact support: {str(e)}")


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
    disf_rate  = (len(disf) / word_count * 100) if word_count else 0
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
        insights.append(f"{icon} Dominant disfluency: **{dominant.replace('_',' ').title()}** ({counts[dominant]} occurrences).")
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

    # ── Severity banner ────────────────────────────────────────────────────────
    st.markdown(severity_banner_html(severity), unsafe_allow_html=True)

    # ── Score gauge + metric cards ─────────────────────────────────────────────
    col_gauge, col_metrics = st.columns([1, 3], gap="medium")
    with col_gauge:
        st.markdown(
            f'<div style="background:white;border-radius:18px;padding:18px;'
            f'box-shadow:0 4px 20px rgba(27,43,94,0.07);border:1.5px solid #E8EDF5;'
            f'display:flex;justify-content:center">{fluency_gauge_html(score)}</div>',
            unsafe_allow_html=True,
        )
    with col_metrics:
        st.markdown(metric_cards_html(score, rate, len(disfluencies), pause_count), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Transcript ─────────────────────────────────────────────────────────────
    with st.expander("📝 Transcript", expanded=True):
        if transcript:
            st.markdown(
                f'<div style="font-size:.95rem;line-height:1.85;color:#374151;'
                f'padding:4px 0">{transcript}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.info("No transcript available.")

    # ── Disfluency timeline ────────────────────────────────────────────────────
    with st.expander("📊 Disfluency Timeline", expanded=True):
        events = timeline if timeline else disfluencies
        if events:
            pills = ""
            for ev in events:
                t    = ev.get("event") or ev.get("type", "unknown")
                ts   = ev.get("time") or ev.get("start") or ev.get("timestamp", "")
                word = ev.get("word", "")
                icon = DISFLUENCY_ICONS.get(t, "❓")
                bg   = PILL_COLORS.get(t, "#F3F4F6")
                fg   = PILL_TEXT_COLORS.get(t, "#374151")
                bd   = PILL_BORDER.get(t, "#D1D5DB")
                lbl  = f"{icon} {t.replace('_',' ')}"
                if word: lbl += f' "{word}"'
                if ts != "": lbl += f" @{ts}"
                pills += (f'<span style="display:inline-flex;align-items:center;'
                          f'background:{bg};color:{fg};border:1px solid {bd};'
                          f'border-radius:20px;padding:5px 12px;font-size:.82rem;'
                          f'font-weight:600;margin:3px 4px 3px 0;gap:2px">{lbl}</span>')
            st.markdown(
                f'<div style="display:flex;flex-wrap:wrap;padding:4px 0">{pills}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.success("No disfluency events detected in this sample.")

    # ── Insights ───────────────────────────────────────────────────────────────
    with st.expander("💡 Automated Insights", expanded=True):
        for ins in generate_insights(result):
            st.markdown(insight_card_html(ins), unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:12px 0 8px;text-align:center">'
        '<span style="font-size:1.7rem">🎙️</span>'
        '<div style="font-size:1.2rem;font-weight:800;color:white;letter-spacing:-.3px;margin-top:4px">FluentVoice</div>'
        '<div style="font-size:.72rem;color:rgba(201,168,76,0.9);font-weight:600;letter-spacing:1px;text-transform:uppercase">Speech Analytics</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr style="border-color:rgba(255,255,255,0.1);margin:8px 0 16px">', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.markdown('<div style="font-size:.72rem;font-weight:700;color:#C9A84C;text-transform:uppercase;letter-spacing:.6px;margin-bottom:6px">Your Name</div>', unsafe_allow_html=True)
        name_input = st.text_input("Your Name", placeholder="e.g. Jane Doe", label_visibility="collapsed",
                                    max_chars=100, help="Enter your first and last name (max 100 characters)")

        st.markdown('<div style="font-size:.72rem;font-weight:700;color:#C9A84C;text-transform:uppercase;letter-spacing:.6px;margin:14px 0 8px">I am a</div>', unsafe_allow_html=True)
        col_p, col_t = st.columns(2, gap="small")
        with col_p:
            if st.button("👤 Patient", key="toggle_patient", use_container_width=True,
                         type="primary" if st.session_state._role_choice == "Patient" else "secondary",
                         help="I am a patient seeking analysis"):
                st.session_state._role_choice = "Patient"
                st.rerun()
        with col_t:
            if st.button("🩺 Therapist", key="toggle_therapist", use_container_width=True,
                         type="primary" if st.session_state._role_choice == "Therapist" else "secondary",
                         help="I am a speech therapist"):
                st.session_state._role_choice = "Therapist"
                st.rerun()

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Continue →", use_container_width=True, help="Proceed to the main application"):
            cleaned_name = name_input.strip()
            if not cleaned_name:
                st.error("⚠️ Please enter your name to continue.")
            elif len(cleaned_name) < 2:
                st.error("⚠️ Please enter at least 2 characters.")
            else:
                st.session_state.name      = cleaned_name
                st.session_state.role      = st.session_state._role_choice
                st.session_state.logged_in = True
                st.rerun()
    else:
        name    = st.session_state.name
        role    = st.session_state.role
        initials = "".join(w[0].upper() for w in name.split()[:2])
        count   = len(st.session_state.all_sessions)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:12px;padding:8px 0 14px">'
            f'<div style="width:48px;height:48px;border-radius:14px;flex-shrink:0;'
            f'background:linear-gradient(135deg,#C9A84C,#E8C96A);display:flex;align-items:center;'
            f'justify-content:center;font-weight:800;font-size:1.1rem;color:#1B2B5E">{initials}</div>'
            f'<div><div style="font-weight:700;color:white;font-size:.97rem">{name}</div>'
            f'<div style="font-size:.78rem;color:rgba(201,168,76,0.9);font-weight:600">{role}</div>'
            f'{"<div style=\"font-size:.72rem;color:rgba(255,255,255,0.5);margin-top:2px\">" + str(count) + " session" + ("s" if count!=1 else "") + "</div>" if count else ""}'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        if st.button("Sign out", use_container_width=True):
            for k in ("logged_in","name","role","last_result","selected_session_idx"):
                st.session_state[k] = False if k == "logged_in" else (None if k in ("last_result","selected_session_idx") else "")
            st.rerun()

# ── Landing ───────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown(
        """
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
          min-height:70vh;text-align:center;padding:40px 20px">
          <div style="background:linear-gradient(135deg,#1B2B5E,#2D44A0);width:90px;height:90px;
            border-radius:26px;display:flex;align-items:center;justify-content:center;
            font-size:2.8rem;margin-bottom:28px;
            box-shadow:0 20px 60px rgba(27,43,94,0.35)">🎙️</div>
          <h1 style="font-size:3rem;font-weight:900;color:#1B2B5E;letter-spacing:-1px;margin:0 0 16px">
            FluentVoice</h1>
          <p style="font-size:1.15rem;color:#6B7280;max-width:480px;line-height:1.7;margin:0 0 40px">
            AI-powered stuttering &amp; fluency analysis.<br>
            Upload or record a voice sample and get instant clinical insights.
          </p>
          <div style="display:flex;gap:28px;flex-wrap:wrap;justify-content:center">
            <div style="background:white;border-radius:16px;padding:20px 24px;min-width:160px;
              box-shadow:0 4px 20px rgba(27,43,94,0.08);border:1px solid #E8EDF5;text-align:center">
              <div style="font-size:1.8rem">📊</div>
              <div style="font-weight:700;color:#1B2B5E;margin-top:8px">Clinical Report</div>
              <div style="font-size:.82rem;color:#9CA3AF;margin-top:4px">Detailed analysis</div>
            </div>
            <div style="background:white;border-radius:16px;padding:20px 24px;min-width:160px;
              box-shadow:0 4px 20px rgba(27,43,94,0.08);border:1px solid #E8EDF5;text-align:center">
              <div style="font-size:1.8rem">🎯</div>
              <div style="font-weight:700;color:#1B2B5E;margin-top:8px">Fluency Score</div>
              <div style="font-size:.82rem;color:#9CA3AF;margin-top:4px">0 – 100 scale</div>
            </div>
            <div style="background:white;border-radius:16px;padding:20px 24px;min-width:160px;
              box-shadow:0 4px 20px rgba(27,43,94,0.08);border:1px solid #E8EDF5;text-align:center">
              <div style="font-size:1.8rem">🩺</div>
              <div style="font-weight:700;color:#1B2B5E;margin-top:8px">Therapist View</div>
              <div style="font-size:.82rem;color:#9CA3AF;margin-top:4px">Session management</div>
            </div>
          </div>
          <p style="margin-top:48px;color:#9CA3AF;font-size:.88rem">👈 Sign in from the sidebar to begin</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# PATIENT VIEW
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.role == "Patient":
    st.markdown(page_header_html(
        f"Welcome back, {st.session_state.name} 👋",
        "Upload or record a voice sample to get your fluency analysis."
    ), unsafe_allow_html=True)

    tab_upload, tab_record = st.tabs(["📁  Upload Audio", "🎙️  Record Audio"])

    with tab_upload:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        audio_file   = st.file_uploader("Choose a WAV, MP3, or M4A file", type=["wav","mp3","m4a"],
                                        label_visibility="collapsed",
                                        help="Supported formats: WAV, MP3, M4A. Max size: 200MB")
        upload_bytes = None
        upload_name  = None
        if audio_file is not None:
            upload_bytes = audio_file.read()
            upload_name  = audio_file.name
            if not upload_bytes:
                st.error("⚠️ The uploaded file is empty. Please try another file.")
                upload_bytes = None
            else:
                st.audio(upload_bytes, format=audio_file.type)
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("🔍  Analyze Speech", disabled=(upload_bytes is None), key="analyze_upload",
                    help="Analyze the uploaded audio file for fluency metrics"):
            analyze_and_save(upload_bytes, upload_name, st.session_state.name)

    with tab_record:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<p style="color:#6B7280;font-size:.9rem;margin-bottom:12px">'
            'Press the microphone button to start recording. Press again to stop.</p>',
            unsafe_allow_html=True,
        )
        audio_input    = st.audio_input("Record your voice", key="native_recorder",
                                       label_visibility="collapsed",
                                       help="Click the microphone to start recording")
        recorded_bytes = None
        if audio_input is not None:
            recorded_bytes = audio_input.read()
            if not recorded_bytes:
                st.error("⚠️ Recording is empty. Please try again.")
                recorded_bytes = None
            else:
                st.success("✅ Recording captured — ready to analyze.")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("🔍  Analyze Speech", disabled=(recorded_bytes is None), key="analyze_record",
                    help="Analyze the recorded audio for fluency metrics"):
            analyze_and_save(recorded_bytes, "recording.wav", st.session_state.name)

    if st.session_state.last_result:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<hr style="border-color:rgba(27,43,94,0.1)">', unsafe_allow_html=True)
        render_analysis(st.session_state.last_result)


# ═══════════════════════════════════════════════════════════════════════════════
# THERAPIST VIEW
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(page_header_html(
        f"Therapist Dashboard",
        f"Reviewing sessions for {st.session_state.name} · {len(st.session_state.all_sessions)} total"
    ), unsafe_allow_html=True)

    sessions = st.session_state.all_sessions

    if not sessions:
        st.markdown(
            """
            <div style="text-align:center;padding:80px 20px;background:white;border-radius:22px;
              border:1.5px solid #E8EDF5;box-shadow:0 4px 20px rgba(27,43,94,0.06)">
              <div style="font-size:3.5rem;margin-bottom:16px">🩺</div>
              <div style="font-size:1.2rem;font-weight:700;color:#1B2B5E;margin-bottom:8px">No Sessions Yet</div>
              <div style="color:#9CA3AF;font-size:.9rem">Ask a patient to analyze a sample first.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    col_list, col_report = st.columns([1, 2], gap="large")

    # ── Left: session list ────────────────────────────────────────────────────
    with col_list:
        st.markdown(
            f'<div style="font-size:.72rem;font-weight:700;color:#6B7280;text-transform:uppercase;'
            f'letter-spacing:.7px;margin-bottom:12px">{len(sessions)} Session{"s" if len(sessions)!=1 else ""}</div>',
            unsafe_allow_html=True,
        )

        for i in range(len(sessions) - 1, -1, -1):
            sess   = sessions[i]
            score  = sess["report"].get("fluency_score", 0)
            sev    = sess["report"].get("severity", "?").title()
            is_sel = st.session_state.selected_session_idx == i

            sev_colors = {
                "Mild":     ("#D1FAE5","#065F46"),
                "Moderate": ("#FEF3C7","#78350F"),
                "Severe":   ("#FEE2E2","#7F1D1D"),
            }
            sc_bg, sc_fg = sev_colors.get(sev, ("#E8EDF5","#1B2B5E"))
            card_border  = "#1B2B5E" if is_sel else "#E8EDF5"
            card_bg      = "#F0F4FF" if is_sel else "white"
            card_shadow  = "0 4px 16px rgba(27,43,94,0.12)" if is_sel else "0 2px 8px rgba(27,43,94,0.05)"

            st.markdown(
                f'<div style="background:{card_bg};border:1.5px solid {card_border};border-radius:16px;'
                f'padding:14px 16px;margin-bottom:4px;box-shadow:{card_shadow};transition:all .2s">'
                f'<div style="display:flex;align-items:center;gap:10px">'
                f'{patient_avatar_html(sess["patient_name"])}'
                f'<div style="flex:1;min-width:0">'
                f'<div style="font-weight:700;color:#1B2B5E;font-size:.92rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{sess["patient_name"]}</div>'
                f'<div style="font-size:.75rem;color:#9CA3AF;margin-top:1px">{sess["timestamp"]}</div>'
                f'</div>'
                f'<div style="text-align:right;flex-shrink:0">'
                f'<div style="font-size:1rem;font-weight:800;color:#1B2B5E">{score:.0f}</div>'
                f'<div style="background:{sc_bg};color:{sc_fg};font-size:.68rem;font-weight:700;'
                f'padding:2px 8px;border-radius:20px;margin-top:2px">{sev}</div>'
                f'</div></div></div>',
                unsafe_allow_html=True,
            )
            if st.button(
                "✓ Selected" if is_sel else "View Report →",
                key=f"view_{i}",
                use_container_width=True,
            ):
                st.session_state.selected_session_idx = i
                st.rerun()
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Right: full report ────────────────────────────────────────────────────
    with col_report:
        idx = st.session_state.selected_session_idx

        if idx is None or not (0 <= idx < len(sessions)):
            st.markdown(
                """
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                  min-height:420px;background:white;border-radius:22px;border:1.5px dashed #D4D9EE;
                  text-align:center;padding:40px">
                  <div style="font-size:3rem;margin-bottom:16px;opacity:.4">📋</div>
                  <div style="font-size:1.05rem;font-weight:600;color:#9CA3AF">Select a session to view the full report</div>
                  <div style="font-size:.85rem;color:#C4C9D8;margin-top:8px">Click "View Report →" on any session</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            sess = sessions[idx]
            # Header
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:16px">'
                f'{patient_avatar_html(sess["patient_name"])}'
                f'<div><div style="font-size:1.15rem;font-weight:800;color:#1B2B5E">{sess["patient_name"]}</div>'
                f'<div style="font-size:.82rem;color:#9CA3AF">{sess["timestamp"]} · {sess["filename"]}</div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.audio(sess["audio_bytes"], format="audio/wav")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            render_analysis(sess["report"])

            # Notes
            st.markdown(
                '<div style="background:white;border-radius:18px;border:1.5px solid #E8EDF5;'
                'padding:22px 24px;margin-top:8px;box-shadow:0 2px 12px rgba(27,43,94,0.06)">'
                '<div style="font-size:.72rem;font-weight:700;color:#6B7280;text-transform:uppercase;'
                'letter-spacing:.7px;margin-bottom:12px">📝 Manual Review Notes</div>',
                unsafe_allow_html=True,
            )
            notes = st.text_area(
                "Notes",
                value=sess.get("notes",""),
                height=130,
                placeholder="e.g. Patient shows improvement in block frequency. Recommend breathing exercises...",
                key=f"notes_{idx}",
                label_visibility="collapsed",
            )
            if st.button("💾  Save Notes", key=f"save_notes_{idx}"):
                st.session_state.all_sessions[idx]["notes"] = notes
                st.success("Notes saved!")
            st.markdown('</div>', unsafe_allow_html=True)
