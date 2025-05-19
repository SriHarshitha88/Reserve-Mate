import streamlit as st
import time
from pathlib import Path
from agent import process_user_message_pseudo_stream
from tools import ALL_RESTAURANTS

# ─── App Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReserveMate",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load & Inject Custom CSS ────────────────────────────────────────────────
def local_css(filename: str):
    css_path = Path(__file__).parent / "assets" / filename
    if css_path.exists():
        css = css_path.read_text(encoding='utf-8')
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Missing CSS: {css_path}")

local_css("style.css")

# ─── Main Title ──────────────────────────────────────────────────────────────
st.markdown(
    "<h1>ReserveMate – A FoodieSpot Initiative 🍽️</h1>",
    unsafe_allow_html=True
)

# ─── Initialize Session State ────────────────────────────────────────────────
session = st.session_state
session.setdefault("messages", [])
session.setdefault("display_messages", [])
session.setdefault("bookings_db", {})
session.setdefault("booking_id_counter_ref", {"value": 1})

# ─── Sidebar: Reservations & Dev Tools ────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3448/3448620.png", width=100)
    st.markdown("## Current Reservations")
    st.markdown("---")

    bookings = session["bookings_db"]
    if not bookings:
        st.info("🌶️ No reservations made this session. Let's find a great spot!")
    else:
        for bid in sorted(bookings, reverse=True):
            d = bookings[bid]
            st.markdown(f"""
                <div class="booking-card">
                  <h4>Booking ID: {bid}</h4>
                  <p><strong>Restaurant:</strong> {d.get('restaurant_name','N/A')}</p>
                  <p><strong>Guest Name:</strong> {d.get('customer_name','N/A')}</p>
                  <p><strong>City:</strong> {d.get('city','N/A')} ({d.get('area','N/A')})</p>
                  <p><strong>Date & Time:</strong> {d.get('date','N/A')} at {d.get('time','N/A')}</p>
                  <p><strong>Guests:</strong> {d.get('num_guests','N/A')}</p>
                  <p><strong>Contact:</strong> {d.get('customer_contact','N/A')}</p>
                  <p><strong>Status:</strong> 
                     <span class="status-{d.get('status','unknown').lower()}">
                       {d.get('status','Unknown').capitalize()}
                     </span>
                  </p>
                </div>
                <hr/>
            """, unsafe_allow_html=True)

    st.markdown("## Developer Tools")
    st.caption(f"Next Booking ID: {session['booking_id_counter_ref']['value']:03d}")

    if st.button("🧹 Clear Chat & Bookings"):
        session.update({
            "messages": [],
            "display_messages": [],
            "bookings_db": {},
            "booking_id_counter_ref": {"value": 1}
        })
        st.rerun()

# ─── Critical Data Check ──────────────────────────────────────────────────────
if not ALL_RESTAURANTS:
    st.error("Failed to load restaurant data. Check restaurants.json.")
    st.stop()

# ─── Chat Display Area ────────────────────────────────────────────────────────
chat_container = st.container()
for msg in session["display_messages"]:
    with chat_container:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ─── Typewriter Effect for Streaming Responses ────────────────────────────────
def pseudo_stream(text: str, placeholder, delay: float = 0.02):
    buf = ""
    for ch in text:
        buf += ch
        placeholder.markdown(buf + "▌")
        time.sleep(delay)
    placeholder.markdown(buf)

# ─── Handle User Input ─────────────────────────────────────────────────────────
if prompt := st.chat_input("Namaste! How can I help with your reservation?"):
    session["display_messages"].append({"role": "user", "content": prompt})
    st.rerun()

# ─── Process & Stream Assistant Responses ─────────────────────────────────────
if session["display_messages"] and session["display_messages"][-1]["role"] == "user":
    user_text = session["display_messages"][-1]["content"]

    with chat_container:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("ReserveMate is thinking…"):
                reply = process_user_message_pseudo_stream(
                    user_text,
                    session["messages"],
                    session["bookings_db"],
                    session["booking_id_counter_ref"]
                )
            pseudo_stream(reply, placeholder)

    session["display_messages"].append({"role": "assistant", "content": reply})

    # If a booking was confirmed, rerun to update sidebar immediately
    if any(keyword in reply.lower() for keyword in ["confirm", "update", "successful"]):
        time.sleep(0.5)
        st.rerun()
