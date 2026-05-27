import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime
import random

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Patient Health Portal",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

  :root {
    --sage:    #4a7c6f;
    --sage-lt: #d4e8e2;
    --sand:    #f5f0e8;
    --clay:    #c17a4a;
    --slate:   #2c3e50;
    --mist:    #eef4f2;
    --text:    #1a2e28;
    --sub:     #5a7a72;
  }

  html, body, .stApp {
    background-color: var(--sand) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
  }

  [data-testid="stSidebar"] { background: var(--sage) !important; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stRadio label { color: white !important; }

  h1, h2, h3, h4 { font-family: 'DM Serif Display', serif !important; color: var(--slate) !important; }

  [data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1rem;
    border-left: 4px solid var(--sage);
    box-shadow: 0 2px 12px rgba(74,124,111,.10);
  }
  [data-testid="stMetricValue"] { color: var(--sage) !important; font-weight: 600; }
  [data-testid="stMetricLabel"] { color: var(--sub) !important; font-size: .85rem !important; }

  .card {
    background: white;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 16px rgba(74,124,111,.08);
    border-top: 3px solid var(--sage);
  }
  .card-clay { border-top-color: var(--clay); }
  .card-blue { border-top-color: #4a90d9; }

  .badge {
    display: inline-block;
    padding: .25rem .75rem;
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 600;
    margin: 2px;
  }
  .badge-green  { background: var(--sage-lt); color: var(--sage); }
  .badge-orange { background: #fde8d4; color: var(--clay); }
  .badge-blue   { background: #dce9f5; color: #2967a0; }
  .badge-red    { background: #fde4e4; color: #c0392b; }
  .badge-purple { background: #ede8f5; color: #6b3fa0; }

  .section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--sage);
    border-bottom: 2px solid var(--sage-lt);
    padding-bottom: .4rem;
    margin-bottom: 1.2rem;
  }

  .art-card {
    background: white;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(44,62,80,.10);
    height: 100%;
  }
  .art-canvas {
    width: 100%;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
  }
  .art-body { padding: 1rem 1.2rem 1.4rem; }
  .art-title { font-family: 'DM Serif Display', serif; font-size: 1.05rem; color: var(--slate); }
  .art-sub   { font-size: .8rem; color: var(--sub); margin-top: .15rem; }
  .art-desc  { font-size: .83rem; color: var(--text); margin-top: .5rem; line-height: 1.5; }

  .timeline-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 1rem;
  }
  .timeline-dot {
    width: 14px; height: 14px;
    border-radius: 50%;
    background: var(--sage);
    margin-top: 4px;
    flex-shrink: 0;
  }
  .timeline-dot.clay   { background: var(--clay); }
  .timeline-dot.blue   { background: #4a90d9; }
  .timeline-dot.purple { background: #6b3fa0; }

  .stTabs [role="tab"] { font-family: 'DM Sans', sans-serif !important; font-weight: 500; color: var(--sub) !important; }
  .stTabs [aria-selected="true"] { color: var(--sage) !important; border-bottom-color: var(--sage) !important; }

  .prog-wrap { margin-bottom: .8rem; }
  .prog-label { font-size: .82rem; color: var(--sub); display: flex; justify-content: space-between; margin-bottom: .25rem; }
  .prog-bar { height: 8px; background: var(--sage-lt); border-radius: 999px; overflow: hidden; }
  .prog-fill { height: 100%; background: var(--sage); border-radius: 999px; transition: width .6s; }
  .prog-fill.clay   { background: var(--clay); }
  .prog-fill.blue   { background: #4a90d9; }
  .prog-fill.purple { background: #6b3fa0; }

  hr { border: none; border-top: 1px solid var(--sage-lt); margin: 1.2rem 0; }
  .streamlit-expanderHeader { color: var(--sage) !important; font-weight: 600; }

  /* Visit note styles */
  .visit-chip {
    display: inline-block;
    padding: .18rem .6rem;
    border-radius: 6px;
    font-size: .72rem;
    font-weight: 700;
    margin-right: .3rem;
    letter-spacing: .04em;
    text-transform: uppercase;
  }
  .chip-routine   { background:#d4e8e2; color:#2d6a5e; }
  .chip-urgent    { background:#fde4e4; color:#b03030; }
  .chip-follow-up { background:#fde8d4; color:#a05020; }
  .chip-procedure { background:#dce9f5; color:#1e5a8e; }
  .chip-telehealth{ background:#ede8f5; color:#5a2e9a; }

  /* Quote block */
  .quote-block {
    border-left: 4px solid var(--sage);
    padding: .8rem 1.2rem;
    background: white;
    border-radius: 0 12px 12px 0;
    margin-bottom: 1rem;
    font-style: italic;
    color: var(--slate);
    font-size: .92rem;
    line-height: 1.6;
  }
  .quote-attr { font-style: normal; font-size: .78rem; color: var(--sub); margin-top: .4rem; font-weight: 600; }

  /* Footer */
  .footer-banner {
    background: linear-gradient(135deg, #2c3e50, #1a2e28);
    border-radius: 18px;
    padding: 1.4rem 2rem;
    color: white;
    font-size: .82rem;
    line-height: 1.7;
    margin-top: 2.5rem;
  }
  .footer-banner b { color: #a8d5c7; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🫀 Health Portal")
    st.markdown("---")

    patients = {
        "Sarah Chen, 42":   {"dob": "1982-04-15", "id": "P-2847", "blood": "A+",  "doctor": "Dr. Reyes",  "dept": "Cardiology"},
        "Marcus Webb, 67":  {"dob": "1957-09-03", "id": "P-1193", "blood": "O−",  "doctor": "Dr. Okafor", "dept": "Internal Medicine"},
        "Aisha Patel, 29":  {"dob": "1995-01-22", "id": "P-3561", "blood": "B+",  "doctor": "Dr. Lin",    "dept": "Endocrinology"},
        "David Torres, 54": {"dob": "1970-07-30", "id": "P-0984", "blood": "AB+", "doctor": "Dr. Nguyen", "dept": "Oncology"},
    }

    selected_patient = st.selectbox("Select Patient", list(patients.keys()))
    pt = patients[selected_patient]

    st.markdown("---")
    st.markdown(f"**Patient ID:** `{pt['id']}`")
    st.markdown(f"**Blood Type:** {pt['blood']}")
    st.markdown(f"**Physician:** {pt['doctor']}")
    st.markdown(f"**Department:** {pt['dept']}")
    st.markdown("---")

    view = st.radio("Navigate", [
        "📋 Overview",
        "💊 Treatment Plan",
        "🛡️ Preventative Health",
        "📁 History & Visits",
        "🎨 Healing Arts",
    ])
    st.markdown("---")
    st.markdown("<small style='opacity:.7'>Last updated: " + datetime.now().strftime("%b %d, %Y %H:%M") + "</small>", unsafe_allow_html=True)


name = selected_patient.split(",")[0]
age  = int(selected_patient.split(", ")[1])

# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"<h1 style='margin-bottom:0'>Welcome back, {name.split()[0]}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#5a7a72;font-size:1rem;margin-top:.2rem'>Patient ID {pt['id']} · {pt['dept']} · {pt['doctor']}</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
if view == "📋 Overview":

    st.markdown('<div class="section-title">Vitals at a Glance</div>', unsafe_allow_html=True)

    vitals_data = {
        "Sarah Chen, 42":   {"hr": 72,  "bp": "118/76", "temp": 98.4, "o2": 98, "bmi": 23.4, "weight": "138 lbs"},
        "Marcus Webb, 67":  {"hr": 81,  "bp": "142/88", "temp": 98.9, "o2": 95, "bmi": 27.1, "weight": "198 lbs"},
        "Aisha Patel, 29":  {"hr": 68,  "bp": "110/70", "temp": 98.2, "o2": 99, "bmi": 21.8, "weight": "126 lbs"},
        "David Torres, 54": {"hr": 76,  "bp": "130/82", "temp": 98.6, "o2": 96, "bmi": 25.3, "weight": "172 lbs"},
    }
    v = vitals_data[selected_patient]

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Heart Rate",     f"{v['hr']} bpm",  delta="−3 bpm")
    c2.metric("Blood Pressure", v['bp'],            delta="Stable")
    c3.metric("Temperature",    f"{v['temp']}°F",  delta="Normal")
    c4.metric("O₂ Saturation",  f"{v['o2']}%",     delta="+1%")
    c5.metric("BMI",            str(v['bmi']),      delta="Healthy")
    c6.metric("Weight",         v['weight'],        delta="−2 lbs")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.3, 1])

    with col_a:
        st.markdown('<div class="section-title">Patient Profile</div>', unsafe_allow_html=True)
        cond_map = {
            "Sarah Chen, 42":   ["Hypertension", "Anxiety", "Vitamin D Deficiency"],
            "Marcus Webb, 67":  ["Type 2 Diabetes", "Hypertension", "Osteoarthritis", "Hyperlipidemia"],
            "Aisha Patel, 29":  ["Hypothyroidism", "Iron-Deficiency Anemia"],
            "David Torres, 54": ["Stage II Lung Cancer", "Hypertension", "GERD"],
        }
        conds = cond_map[selected_patient]

        allergies_map = {
            "Sarah Chen, 42":   ["Penicillin", "Sulfa Drugs"],
            "Marcus Webb, 67":  ["Aspirin", "Latex"],
            "Aisha Patel, 29":  ["NSAIDs"],
            "David Torres, 54": ["Codeine", "Shellfish"],
        }
        allergies = allergies_map[selected_patient]

        st.markdown(f"""
        <div class="card">
          <table style="width:100%;border-collapse:collapse;font-size:.88rem">
            <tr><td style="color:#5a7a72;padding:.35rem 0;width:42%">Full Name</td><td><b>{name}</b></td></tr>
            <tr><td style="color:#5a7a72;padding:.35rem 0">Date of Birth</td><td>{pt['dob']}</td></tr>
            <tr><td style="color:#5a7a72;padding:.35rem 0">Age</td><td>{age} years</td></tr>
            <tr><td style="color:#5a7a72;padding:.35rem 0">Blood Type</td><td>{pt['blood']}</td></tr>
            <tr><td style="color:#5a7a72;padding:.35rem 0">Primary Physician</td><td>{pt['doctor']}</td></tr>
            <tr><td style="color:#5a7a72;padding:.35rem 0">Department</td><td>{pt['dept']}</td></tr>
          </table>
          <hr>
          <p style="font-size:.82rem;color:#5a7a72;margin-bottom:.4rem">Active Conditions</p>
          {''.join([f'<span class="badge badge-orange">{c}</span>' for c in conds])}
          <hr>
          <p style="font-size:.82rem;color:#5a7a72;margin-bottom:.4rem">Allergies</p>
          {''.join([f'<span class="badge badge-red">⚠ {a}</span>' for a in allergies])}
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-title">Recent Lab Results</div>', unsafe_allow_html=True)
        labs_map = {
            "Sarah Chen, 42":  [("Cholesterol", 195, 200, "mg/dL"), ("HbA1c", 5.4, 5.7, "%"), ("Vitamin D", 28, 30, "ng/mL"), ("Hemoglobin", 13.8, 12.0, "g/dL")],
            "Marcus Webb, 67": [("Fasting Glucose", 148, 100, "mg/dL"), ("HbA1c", 7.8, 6.5, "%"), ("LDL", 112, 100, "mg/dL"), ("eGFR", 68, 60, "mL/min")],
            "Aisha Patel, 29": [("TSH", 4.8, 4.5, "mIU/L"), ("Free T4", 0.9, 0.8, "ng/dL"), ("Ferritin", 11, 12, "ng/mL"), ("Hemoglobin", 10.2, 12.0, "g/dL")],
            "David Torres, 54":[("CA 19-9", 87, 37, "U/mL"), ("CEA", 6.2, 3.0, "ng/mL"), ("WBC", 11.4, 10.5, "K/μL"), ("Albumin", 3.7, 3.5, "g/dL")],
        }
        for lab, val, ref, unit in labs_map[selected_patient]:
            status = "🟢" if val <= ref else "🔴"
            pct = min(val / (ref * 1.5) * 100, 100) if ref > 0 else 50
            color = "clay" if val > ref else ""
            st.markdown(f"""
            <div class="prog-wrap">
              <div class="prog-label"><span>{status} {lab}</span><span>{val} <small>{unit}</small> (ref ≤{ref})</span></div>
              <div class="prog-bar"><div class="prog-fill {color}" style="width:{pct}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">6-Month Vital History</div>', unsafe_allow_html=True)
    months = ["Dec", "Jan", "Feb", "Mar", "Apr", "May"]
    base_hr  = v['hr']
    base_sys = int(v['bp'].split("/")[0])
    base_dia = int(v['bp'].split("/")[1])
    hr_vals  = [base_hr  + random.randint(-8, 8)  for _ in months]
    sys_vals = [base_sys + random.randint(-10, 10) for _ in months]
    dia_vals = [base_dia + random.randint(-6, 6)   for _ in months]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=hr_vals,  name="Heart Rate",   line=dict(color="#4a7c6f", width=2.5), mode="lines+markers"))
    fig.add_trace(go.Scatter(x=months, y=sys_vals, name="Systolic BP",  line=dict(color="#c17a4a", width=2.5), mode="lines+markers"))
    fig.add_trace(go.Scatter(x=months, y=dia_vals, name="Diastolic BP", line=dict(color="#4a90d9", width=2.5), mode="lines+markers", line_dash="dot"))
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="DM Sans", color="#2c3e50"),
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=0, r=0, t=10, b=0), height=260,
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#eef4f2"),
    )
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — TREATMENT PLAN
# ════════════════════════════════════════════════════════════════════════════════
elif view == "💊 Treatment Plan":

    st.markdown('<div class="section-title">Active Treatment Plan</div>', unsafe_allow_html=True)

    plans = {
        "Sarah Chen, 42": {
            "goals": [("Reduce systolic BP to < 120 mmHg", 78), ("Manage anxiety symptoms", 55), ("Increase Vitamin D to 40 ng/mL", 60)],
            "meds": [
                ("Lisinopril", "10 mg", "Once daily (morning)", "Hypertension", "green"),
                ("Sertraline", "50 mg", "Once daily (morning)", "Anxiety", "blue"),
                ("Vitamin D3", "2000 IU", "Once daily (with food)", "Deficiency", "orange"),
            ],
            "appointments": [
                ("Jun 10, 2025", "Follow-up: BP check", "Dr. Reyes", "clay"),
                ("Jul 15, 2025", "Lab work — lipid panel", "Dr. Reyes", ""),
                ("Aug 01, 2025", "Annual physical", "Dr. Reyes", ""),
            ],
            "notes": "Patient responding well to Lisinopril. Reassess Sertraline dosage at next visit. Encourage 30 min daily walks.",
        },
        "Marcus Webb, 67": {
            "goals": [("Lower HbA1c below 7.0%", 42), ("Control blood pressure < 130/80", 60), ("Reduce LDL to < 100 mg/dL", 55)],
            "meds": [
                ("Metformin", "1000 mg", "Twice daily (with meals)", "Type 2 Diabetes", "blue"),
                ("Amlodipine", "5 mg", "Once daily", "Hypertension", "green"),
                ("Atorvastatin", "40 mg", "Once daily (evening)", "Hyperlipidemia", "orange"),
                ("Celecoxib", "200 mg", "As needed", "Osteoarthritis", "orange"),
            ],
            "appointments": [
                ("Jun 5, 2025", "Diabetes management review", "Dr. Okafor", "clay"),
                ("Jun 28, 2025", "Podiatry check", "Dr. Okafor", ""),
                ("Sep 10, 2025", "3-month HbA1c retest", "Dr. Okafor", ""),
            ],
            "notes": "Diet counseling recommended. Monitor kidney function quarterly. Arthritis exercise program referral placed.",
        },
        "Aisha Patel, 29": {
            "goals": [("Normalize TSH to 0.5–4.0 mIU/L", 50), ("Raise ferritin above 20 ng/mL", 35), ("Resolve anemia symptoms", 48)],
            "meds": [
                ("Levothyroxine", "75 mcg", "Once daily (fasting)", "Hypothyroidism", "green"),
                ("Ferrous Sulfate", "325 mg", "Twice daily", "Iron Deficiency Anemia", "orange"),
                ("Folic Acid", "1 mg", "Once daily", "Anemia support", "blue"),
            ],
            "appointments": [
                ("Jun 18, 2025", "TSH follow-up labs", "Dr. Lin", "clay"),
                ("Jul 30, 2025", "Thyroid ultrasound", "Dr. Lin", ""),
            ],
            "notes": "Levothyroxine dose may need titration. Advise iron-rich diet. Re-check CBC in 8 weeks.",
        },
        "David Torres, 54": {
            "goals": [("Complete 4th chemo cycle", 75), ("Manage treatment side effects", 60), ("Monitor tumor markers monthly", 90)],
            "meds": [
                ("Carboplatin", "AUC 5", "IV every 3 weeks", "Stage II Lung Cancer", "red"),
                ("Pemetrexed", "500 mg/m²", "IV every 3 weeks", "Stage II Lung Cancer", "red"),
                ("Ondansetron", "8 mg", "Before/after chemo", "Anti-nausea", "orange"),
                ("Omeprazole", "20 mg", "Once daily", "GERD", "green"),
            ],
            "appointments": [
                ("Jun 3, 2025", "Cycle 4 Chemotherapy", "Dr. Nguyen", "clay"),
                ("Jun 17, 2025", "Oncology review + labs", "Dr. Nguyen", "clay"),
                ("Jul 8, 2025", "CT scan — tumor response", "Dr. Nguyen", ""),
            ],
            "notes": "Patient tolerating regimen. Watch for neuropathy. Nutritionist consult placed. Palliative care team involved.",
        },
    }

    plan = plans[selected_patient]
    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown("**🎯 Treatment Goals**")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for goal, pct in plan["goals"]:
            color = "clay" if pct < 50 else "blue" if pct < 70 else ""
            st.markdown(f"""
            <div class="prog-wrap">
              <div class="prog-label"><span>{goal}</span><span>{pct}%</span></div>
              <div class="prog-bar"><div class="prog-fill {color}" style="width:{pct}%"></div></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("**📝 Physician Notes**")
        st.markdown(f'<div class="card card-clay"><p style="font-size:.88rem;line-height:1.65;margin:0">{plan["notes"]}</p></div>', unsafe_allow_html=True)

    with col2:
        st.markdown("**💊 Current Medications**")
        for med, dose, freq, indication, color in plan["meds"]:
            badge_cls = f"badge-{color}" if color else "badge-green"
            st.markdown(f"""
            <div class="card" style="padding:1rem 1.2rem;margin-bottom:.6rem">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-weight:600;font-size:.95rem">{med}</span>
                <span class="badge {badge_cls}">{indication}</span>
              </div>
              <div style="font-size:.82rem;color:#5a7a72;margin-top:.4rem">
                💉 <b>{dose}</b> &nbsp;·&nbsp; ⏱ {freq}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**📅 Upcoming Appointments**")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for appt_date, appt_title, appt_dr, dot_color in plan["appointments"]:
        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-dot {dot_color}"></div>
          <div>
            <div style="font-weight:600;font-size:.9rem">{appt_title}</div>
            <div style="font-size:.8rem;color:#5a7a72">{appt_date} &nbsp;·&nbsp; {appt_dr}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — PREVENTATIVE HEALTH
# ════════════════════════════════════════════════════════════════════════════════
elif view == "🛡️ Preventative Health":

    st.markdown('<div class="section-title">Preventative Health Programme</div>', unsafe_allow_html=True)

    screenings = {
        "Sarah Chen, 42": [
            ("Mammogram", "Mar 2025", "Due: Mar 2026", "✅ Complete", "green"),
            ("Cervical Smear / Pap", "Jan 2025", "Due: Jan 2028", "✅ Complete", "green"),
            ("Cholesterol Panel", "Nov 2024", "Due: Nov 2025", "⚠️ Due Soon", "orange"),
            ("Colorectal Screening", "—", "Due at 45", "📌 Upcoming", "blue"),
            ("Skin Cancer Check", "May 2024", "Due: May 2025", "🔴 Overdue", "red"),
            ("Bone Density (DEXA)", "—", "Due at 50", "📌 Upcoming", "blue"),
        ],
        "Marcus Webb, 67": [
            ("Colonoscopy", "Feb 2023", "Due: Feb 2033", "✅ Complete", "green"),
            ("PSA / Prostate Screen", "Jan 2025", "Due: Jan 2026", "✅ Complete", "green"),
            ("Diabetic Eye Exam", "Apr 2025", "Due: Apr 2026", "✅ Complete", "green"),
            ("Foot Exam (Diabetic)", "Mar 2025", "Due: Jun 2025", "⚠️ Due Soon", "orange"),
            ("Abdominal Aortic Ultrasound", "—", "Recommended", "🔴 Not Done", "red"),
            ("Shingles Vaccine", "2019", "Booster recommended", "⚠️ Review", "orange"),
        ],
        "Aisha Patel, 29": [
            ("Cervical Smear / Pap", "Dec 2024", "Due: Dec 2027", "✅ Complete", "green"),
            ("Thyroid Antibody Panel", "Apr 2025", "Due: Apr 2026", "✅ Complete", "green"),
            ("STI Screening", "Jan 2025", "Due: Jan 2026", "✅ Complete", "green"),
            ("HPV Vaccine (series)", "Complete", "Completed 2018", "✅ Complete", "green"),
            ("Mental Health Screen (PHQ-9)", "Mar 2025", "Due: Sep 2025", "⚠️ Due Soon", "orange"),
            ("Skin Cancer Check", "—", "Annual recommended", "🔴 Not Done", "red"),
        ],
        "David Torres, 54": [
            ("Low-Dose CT Lung Screen", "May 2025", "Due: May 2026", "✅ Complete", "green"),
            ("Colonoscopy", "2022", "Due: 2032", "✅ Complete", "green"),
            ("PSA / Prostate Screen", "Apr 2025", "Due: Apr 2026", "✅ Complete", "green"),
            ("Flu Vaccine", "Oct 2024", "Due: Oct 2025", "⚠️ Due Soon", "orange"),
            ("Pneumococcal Vaccine", "—", "Recommended for smokers", "🔴 Not Done", "red"),
            ("Bone Density (DEXA)", "—", "Chemo risk — schedule now", "🔴 Priority", "red"),
        ],
    }

    lifestyle = {
        "Sarah Chen, 42":   [("Physical Activity", 4, 5, "4/5 days/week"), ("Sleep Quality", 6.5, 8, "Avg 6.5 hrs"), ("Stress Management", 55, 100, "Moderate"), ("Nutrition Score", 70, 100, "Good")],
        "Marcus Webb, 67":  [("Physical Activity", 2, 5, "2/5 days/week"), ("Sleep Quality", 7, 8, "Avg 7 hrs"), ("Blood Sugar Control", 62, 100, "Needs work"), ("Foot Care Adherence", 80, 100, "Good")],
        "Aisha Patel, 29":  [("Physical Activity", 5, 5, "5/5 days/week"), ("Sleep Quality", 7.5, 8, "Avg 7.5 hrs"), ("Medication Adherence", 92, 100, "Excellent"), ("Iron-Rich Diet", 50, 100, "Improving")],
        "David Torres, 54": [("Treatment Adherence", 95, 100, "Excellent"), ("Nutrition (Chemo)", 60, 100, "Moderate"), ("Rest & Recovery", 7, 8, "Avg 7 hrs"), ("Emotional Wellbeing", 50, 100, "Support needed")],
    }

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("**🔬 Screening Tracker**")
        rows = ""
        for item, last, next_due, status, color in screenings[selected_patient]:
            badge_cls = f"badge-{color}"
            rows += f"""
            <tr style="border-bottom:1px solid #eef4f2">
              <td style="padding:.6rem .5rem;font-size:.85rem;font-weight:500">{item}</td>
              <td style="padding:.6rem .5rem;font-size:.82rem;color:#5a7a72">{last}</td>
              <td style="padding:.6rem .5rem;font-size:.82rem;color:#5a7a72">{next_due}</td>
              <td style="padding:.6rem .5rem"><span class="badge {badge_cls}">{status}</span></td>
            </tr>"""
        st.markdown(f"""
        <div class="card">
          <table style="width:100%;border-collapse:collapse">
            <thead><tr style="background:#f5f0e8">
              <th style="text-align:left;padding:.5rem;font-size:.8rem;color:#5a7a72">Screening</th>
              <th style="text-align:left;padding:.5rem;font-size:.8rem;color:#5a7a72">Last Done</th>
              <th style="text-align:left;padding:.5rem;font-size:.8rem;color:#5a7a72">Next Due</th>
              <th style="text-align:left;padding:.5rem;font-size:.8rem;color:#5a7a72">Status</th>
            </tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("**🌿 Lifestyle Metrics**")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for label, val, max_val, display in lifestyle[selected_patient]:
            pct = min(val / max_val * 100, 100)
            color = "clay" if pct < 50 else "blue" if pct < 70 else ""
            st.markdown(f"""
            <div class="prog-wrap">
              <div class="prog-label"><span>{label}</span><span>{display}</span></div>
              <div class="prog-bar"><div class="prog-fill {color}" style="width:{pct}%"></div></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("**💉 Immunisation Record**")
        vaccines = {
            "Sarah Chen, 42":   [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Oct 2024", "green"), ("Tdap", "2020", "green"), ("Hepatitis B", "Complete", "green")],
            "Marcus Webb, 67":  [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Oct 2024", "green"), ("Pneumococcal", "2022", "green"), ("Shingles (Shingrix)", "2019", "orange")],
            "Aisha Patel, 29":  [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Oct 2024", "green"), ("HPV (Gardasil)", "2018", "green"), ("MMR", "Childhood", "green")],
            "David Torres, 54": [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Due Oct 2025", "orange"), ("Pneumococcal", "Not done", "red"), ("Hepatitis B", "Complete", "green")],
        }
        badges = "".join([f'<span class="badge badge-{c}">{vax} · {yr}</span>' for vax, yr, c in vaccines[selected_patient]])
        st.markdown(f'<div class="card">{badges}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🕸 Wellness Radar**")
    categories = ["Physical Activity", "Nutrition", "Sleep", "Mental Health", "Medication", "Preventative Care"]
    scores_map = {
        "Sarah Chen, 42":   [80, 70, 65, 55, 85, 72],
        "Marcus Webb, 67":  [40, 55, 70, 60, 78, 68],
        "Aisha Patel, 29":  [92, 55, 75, 70, 94, 80],
        "David Torres, 54": [45, 60, 72, 50, 95, 82],
    }
    scores = scores_map[selected_patient]
    fig2 = go.Figure(go.Scatterpolar(
        r=scores + [scores[0]], theta=categories + [categories[0]],
        fill='toself', fillcolor='rgba(74,124,111,0.18)',
        line=dict(color='#4a7c6f', width=2.5),
        marker=dict(size=7, color='#4a7c6f'),
    ))
    fig2.update_layout(
        polar=dict(bgcolor='white', radialaxis=dict(range=[0,100], showticklabels=False, gridcolor="#eef4f2"), angularaxis=dict(gridcolor="#eef4f2")),
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='DM Sans', color='#2c3e50'),
        margin=dict(l=30, r=30, t=20, b=20), height=300,
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — HISTORY & VISIT DOCUMENTATION
# ════════════════════════════════════════════════════════════════════════════════
elif view == "📁 History & Visits":

    st.markdown('<div class="section-title">Medical History & Visit Documentation</div>', unsafe_allow_html=True)

    # ── Medical history summary ───────────────────────────────────────────────
    history_map = {
        "Sarah Chen, 42": {
            "summary": "Sarah has a 6-year history of hypertension first diagnosed at age 36 during a routine physical. She was started on lifestyle modifications before pharmacological intervention was introduced in 2021. Anxiety disorder was diagnosed concurrently in 2022 following elevated GAD-7 scores over two consecutive visits. She has no history of hospitalisation, surgeries, or major cardiac events. Family history is notable for hypertension (mother) and type 2 diabetes (father). Non-smoker; occasional alcohol use.",
            "past_conditions": [("Essential Hypertension", "2019", "Active — managed"), ("Generalised Anxiety Disorder", "2022", "Active — managed"), ("Vitamin D Deficiency", "2023", "Active — supplementing"), ("Seasonal Allergic Rhinitis", "2015", "Inactive — resolved")],
            "surgeries": [("Appendectomy", "2008", "Uncomplicated"), ("Wisdom Tooth Extraction (×4)", "2003", "Uncomplicated")],
            "family_hx": ["Hypertension (mother)", "Type 2 Diabetes (father)", "Breast cancer (maternal aunt, age 58)"],
            "social_hx": "Non-smoker. Occasional alcohol (1–2 drinks/week). Works as a graphic designer (sedentary role). Married, two children. Reports moderate work-related stress.",
        },
        "Marcus Webb, 67": {
            "summary": "Marcus has a complex medical history spanning over 20 years. Type 2 diabetes was diagnosed at age 46 after routine bloodwork revealed fasting glucose of 182 mg/dL. Hypertension followed two years later. He underwent a coronary angiogram in 2018 that showed mild coronary artery disease — managed conservatively. Osteoarthritis of the bilateral knees was confirmed via imaging in 2020. He was hospitalised once in 2022 for a hypoglycaemic episode. Retired teacher. Widower.",
            "past_conditions": [("Type 2 Diabetes Mellitus", "2003", "Active — managed"), ("Essential Hypertension", "2005", "Active — managed"), ("Hyperlipidemia", "2010", "Active — managed"), ("Mild Coronary Artery Disease", "2018", "Stable — monitored"), ("Osteoarthritis (bilateral knees)", "2020", "Active — managed"), ("Hypoglycaemic Episode (hospitalised)", "2022", "Resolved")],
            "surgeries": [("Left Knee Arthroscopy", "2021", "Uncomplicated"), ("Cataract Surgery (right eye)", "2019", "Uncomplicated")],
            "family_hx": ["Type 2 Diabetes (mother, father)", "MI (brother, age 62)", "Colorectal cancer (father, age 71)"],
            "social_hx": "Former smoker — quit 2001 (20 pack-year history). No alcohol. Retired. Lives alone. Physically limited by knee pain. Active in church community.",
        },
        "Aisha Patel, 29": {
            "summary": "Aisha was diagnosed with Hashimoto's thyroiditis at age 25 after presenting with fatigue, weight gain, and cold intolerance. TSH was markedly elevated at 9.4 mIU/L at initial presentation. Iron-deficiency anaemia was identified concurrently, thought to be related to heavy menstrual cycles. She has no surgical history and no prior hospitalisations. Family history is significant for autoimmune conditions. She is currently enrolled in a graduate nutrition programme.",
            "past_conditions": [("Hashimoto's Thyroiditis / Hypothyroidism", "2020", "Active — managed"), ("Iron-Deficiency Anaemia", "2020", "Active — improving"), ("Iron-Deficiency Anaemia (initial)", "2020", "Active — treated"), ("Menorrhagia", "2019", "Under gynaecology review")],
            "surgeries": [],
            "family_hx": ["Hashimoto's thyroiditis (mother)", "Rheumatoid arthritis (maternal grandmother)", "Type 1 Diabetes (brother)"],
            "social_hx": "Non-smoker, no alcohol. Graduate student. Vegetarian diet — dietitian consult recommended. Exercises regularly (5×/week). Reports high academic stress.",
        },
        "David Torres, 54": {
            "summary": "David presented in January 2024 with a 3-month history of progressive dyspnoea, haemoptysis, and 12 lb unintentional weight loss. CT thorax revealed a 3.8 cm right upper lobe mass with mediastinal lymphadenopathy. Biopsy confirmed Stage IIB non-small cell lung carcinoma (adenocarcinoma). He is currently in active chemotherapy (cycle 3 of 6 completed). He has a 30 pack-year smoking history (quit upon diagnosis). GERD has been managed long-term. No prior malignancies. He has two adult children and is currently on medical leave from construction management.",
            "past_conditions": [("Stage IIB NSCLC (adenocarcinoma, RUL)", "Jan 2024", "Active — on treatment"), ("GERD / Oesophageal Reflux", "2015", "Active — managed"), ("Essential Hypertension", "2017", "Active — managed"), ("Occupational Asbestos Exposure", "1995–2010", "Historical — monitored")],
            "surgeries": [("Right Shoulder Rotator Cuff Repair", "2016", "Uncomplicated"), ("Inguinal Hernia Repair", "2009", "Uncomplicated")],
            "family_hx": ["Lung cancer (father, age 61)", "COPD (mother)", "Hypertension (both parents)"],
            "social_hx": "Former smoker — quit Jan 2024 (30 pack-year history). Occasional alcohol. Construction manager on medical leave. Divorced. Two adult children, supportive. Reports significant anxiety about prognosis.",
        },
    }

    h = history_map[selected_patient]

    col_h1, col_h2 = st.columns([1.3, 1])

    with col_h1:
        st.markdown("**📖 Clinical History Summary**")
        st.markdown(f'<div class="card"><p style="font-size:.88rem;line-height:1.75;margin:0">{h["summary"]}</p></div>', unsafe_allow_html=True)

        st.markdown("**🩺 Past Medical Conditions**")
        rows = ""
        for cond, year, status in h["past_conditions"]:
            color = "green" if "Active" not in status or "managed" in status.lower() else "orange"
            if "Resolved" in status or "Uncomplicated" in status: color = "green"
            if "Active" in status and "managed" not in status.lower(): color = "orange"
            rows += f"""
            <tr style="border-bottom:1px solid #eef4f2">
              <td style="padding:.55rem .5rem;font-size:.84rem;font-weight:500">{cond}</td>
              <td style="padding:.55rem .5rem;font-size:.82rem;color:#5a7a72">{year}</td>
              <td style="padding:.55rem .5rem"><span class="badge badge-{color}" style="font-size:.7rem">{status}</span></td>
            </tr>"""
        st.markdown(f"""
        <div class="card">
          <table style="width:100%;border-collapse:collapse">
            <thead><tr style="background:#f5f0e8">
              <th style="text-align:left;padding:.5rem;font-size:.78rem;color:#5a7a72">Condition</th>
              <th style="text-align:left;padding:.5rem;font-size:.78rem;color:#5a7a72">Diagnosed</th>
              <th style="text-align:left;padding:.5rem;font-size:.78rem;color:#5a7a72">Status</th>
            </tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with col_h2:
        st.markdown("**🔪 Surgical History**")
        if h["surgeries"]:
            surg_html = ""
            for surg, yr, outcome in h["surgeries"]:
                surg_html += f"""
                <div class="timeline-item">
                  <div class="timeline-dot blue"></div>
                  <div>
                    <div style="font-weight:600;font-size:.88rem">{surg}</div>
                    <div style="font-size:.78rem;color:#5a7a72">{yr} &nbsp;·&nbsp; <span style="color:#2d7a4a">{outcome}</span></div>
                  </div>
                </div>"""
            st.markdown(f'<div class="card">{surg_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><p style="font-size:.85rem;color:#5a7a72;margin:0">No surgical history on record.</p></div>', unsafe_allow_html=True)

        st.markdown("**👨‍👩‍👧 Family History**")
        fam_html = "".join([f'<span class="badge badge-purple">🧬 {f}</span>' for f in h["family_hx"]])
        st.markdown(f'<div class="card">{fam_html}</div>', unsafe_allow_html=True)

        st.markdown("**🏠 Social History**")
        st.markdown(f'<div class="card card-blue"><p style="font-size:.85rem;line-height:1.65;margin:0">{h["social_hx"]}</p></div>', unsafe_allow_html=True)

    # ── Visit Documentation ───────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Visit Documentation</div>', unsafe_allow_html=True)

    visit_notes = {
        "Sarah Chen, 42": [
            {
                "date": "May 14, 2025", "type": "Follow-Up", "chip": "chip-follow-up",
                "provider": "Dr. Reyes, MD — Cardiology",
                "cc": "Routine BP monitoring and medication review.",
                "subjective": "Patient reports improved energy levels since last visit. Denies chest pain, palpitations, or dyspnoea. Mild anxiety persisting — 'I've been better since reducing my work hours.' Sleep quality described as 'okay — around 6–7 hours a night.' Medication compliance confirmed.",
                "objective": "BP 118/76 mmHg (left arm, seated), HR 72 bpm, RR 14, SpO₂ 98%. Cardiovascular exam: regular rate and rhythm, no murmurs. Lungs clear. No peripheral oedema.",
                "assessment": "Hypertension — well controlled on current regimen. Anxiety — stable, no dose change warranted at this time. Vitamin D deficiency — supplementation ongoing, recheck at 6-month mark.",
                "plan": "Continue Lisinopril 10 mg daily. Continue Sertraline 50 mg. Vitamin D3 2000 IU daily ongoing. Reinforce lifestyle: 30 min moderate exercise ≥5 days/week. Repeat BMP and lipid panel in 3 months. RTC in 8 weeks or sooner if symptoms change.",
            },
            {
                "date": "Feb 20, 2025", "type": "Telehealth", "chip": "chip-telehealth",
                "provider": "Dr. Reyes, MD — Cardiology",
                "cc": "Anxiety flare and BP reading at home (132/84).",
                "subjective": "Patient called in reporting two consecutive home BP readings of 132/84 and 130/82 over three days. Reports increased work stress ('major project deadline'). Anxiety symptoms elevated — GAD-7 self-report of 11 (moderate). Denies headache, visual changes, or chest symptoms.",
                "objective": "Telehealth — no in-person exam. Patient took BP during call: 128/80 mmHg. HR self-reported 78 bpm.",
                "assessment": "Transient BP elevation likely stress-mediated. Anxiety — moderately elevated, situational. Reassurance provided. No medication change at this time.",
                "plan": "Advised patient on stress reduction strategies (breathing exercises, screen time limits before bed). Instructed to monitor BP twice daily for 1 week and log results. If consistent readings above 135/85, call to adjust medication. Sertraline unchanged. Scheduled in-person follow-up for May.",
            },
            {
                "date": "Nov 08, 2024", "type": "Routine", "chip": "chip-routine",
                "provider": "Dr. Reyes, MD — Cardiology",
                "cc": "Annual review — hypertension and anxiety management.",
                "subjective": "Patient reports feeling generally well. BP readings at home have been 'a bit better.' Sertraline initiated 6 months ago — 'I think it's helping.' No new complaints. Completed mammogram (results normal). Flu vaccine received at pharmacy.",
                "objective": "BP 122/78, HR 74, SpO₂ 98%. BMI 23.4. Physical exam unremarkable. Fundoscopic exam: no hypertensive retinopathy.",
                "assessment": "Hypertension — stable. Anxiety — improved on Sertraline. Vitamin D deficiency — new finding on labs (28 ng/mL). Lipid panel within normal limits.",
                "plan": "Added Vitamin D3 2000 IU supplementation. All other medications continued. Repeat Vitamin D at 6-month follow-up. Counselled on calcium-rich diet. Skin cancer check overdue — referred to dermatology.",
            },
        ],
        "Marcus Webb, 67": [
            {
                "date": "May 02, 2025", "type": "Follow-Up", "chip": "chip-follow-up",
                "provider": "Dr. Okafor, MD — Internal Medicine",
                "cc": "Quarterly diabetes and hypertension review.",
                "subjective": "Patient reports fatigue after meals and increased urinary frequency. 'My knees have been worse this winter.' Compliance with Metformin confirmed. Patient skipped two Atorvastatin doses last week. Foot inspection performed at home by patient daily.",
                "objective": "BP 142/88 mmHg, HR 81, SpO₂ 95%. BMI 27.1. Fasting glucose today: 148 mg/dL. HbA1c: 7.8%. Lower extremity exam: no ulcerations, sensation mildly reduced bilateral toes. Pedal pulses intact.",
                "assessment": "Type 2 DM — suboptimally controlled. Hypertension — elevated, requires closer monitoring. Hyperlipidaemia — LDL 112, above target. Osteoarthritis — worsening bilaterally.",
                "plan": "Increase dietary counselling — refer to registered dietitian. Reinforce Atorvastatin compliance. Consider Amlodipine dose titration at next visit if BP remains elevated. Celecoxib PRN for knee pain. Podiatry referral placed. Next HbA1c in 3 months.",
            },
            {
                "date": "Jan 15, 2025", "type": "Urgent", "chip": "chip-urgent",
                "provider": "Dr. Okafor, MD — Internal Medicine",
                "cc": "Dizziness and near-syncope episode at home.",
                "subjective": "Patient brought in by son after feeling lightheaded and nearly fainting at home. 'I hadn't eaten since breakfast — it was about 7 pm.' Reports sweating and hand tremor preceding episode. Recovered after eating a snack. No loss of consciousness, no chest pain.",
                "objective": "BP 118/70 (lying), 106/64 (standing) — orthostatic changes noted. HR 91. CBG on arrival: 54 mg/dL. Alert and oriented ×3. Skin pale, diaphoretic on presentation, normalised by time of exam.",
                "assessment": "Hypoglycaemic episode — likely secondary to missed meal with ongoing Metformin use. Orthostatic hypotension — possibly compounded by antihypertensives.",
                "plan": "Advised structured meal timing. Hypoglycaemia action plan reviewed with patient and son. Amlodipine held for 48 hours; BP to be monitored at home. No insulin changes. Return for urgent review if further episodes. Educated on early symptoms of hypoglycaemia.",
            },
        ],
        "Aisha Patel, 29": [
            {
                "date": "Apr 22, 2025", "type": "Follow-Up", "chip": "chip-follow-up",
                "provider": "Dr. Lin, MD — Endocrinology",
                "cc": "Thyroid function monitoring and anaemia review.",
                "subjective": "Patient reports reduced fatigue compared to prior visits. 'I feel about 70% — better than before.' Still experiencing occasional brain fog and cold intolerance. Iron supplement taken consistently, though GI side effects (constipation) noted. Menstrual cycle still heavy — 7–8 days.",
                "objective": "BP 110/70, HR 68, Temp 98.2°F, SpO₂ 99%. BMI 21.8. Thyroid: mildly enlarged, non-tender. TSH: 4.8 mIU/L (↓ from 6.2), Free T4: 0.9 ng/dL. Ferritin: 11 ng/mL (↑ from 6). CBC: Hgb 10.2 g/dL.",
                "assessment": "Hypothyroidism — partially controlled, Levothyroxine dose may require upward titration. Iron-deficiency anaemia — improving slowly. Menorrhagia — contributing to ongoing anaemia, gynaecology referral warranted.",
                "plan": "Increase Levothyroxine to 88 mcg (trial). Add stool softener to manage constipation from iron. Refer to gynaecology for menorrhagia evaluation. Recheck TSH and CBC in 8 weeks. Dietary consult to improve iron absorption.",
            },
            {
                "date": "Jan 10, 2025", "type": "Routine", "chip": "chip-routine",
                "provider": "Dr. Lin, MD — Endocrinology",
                "cc": "New patient intake and thyroid management.",
                "subjective": "Patient transferred care from prior provider. Reports 4 years of managed hypothyroidism. Current symptoms: fatigue ('always tired'), weight fluctuation, hair thinning, brain fog. Recently started Ferrous Sulfate from prior provider. Exercise frequency: 5×/week (yoga and running).",
                "objective": "Comprehensive metabolic panel, thyroid function, iron studies ordered. TSH: 6.2 mIU/L, Free T4: 0.8 ng/dL, Ferritin: 6 ng/mL, Hgb: 9.8 g/dL. BP 112/72, HR 70.",
                "assessment": "Hypothyroidism — undertreated on current dose. Iron-deficiency anaemia — significant. Establish care and optimise regimen.",
                "plan": "Continue Levothyroxine 75 mcg; reassess in 8 weeks. Continue Ferrous Sulfate 325 mg BD. Add Folic Acid 1 mg. Nutritional counselling referral. PHQ-9 administered: score 6 (mild) — monitor. Return in 3 months.",
            },
        ],
        "David Torres, 54": [
            {
                "date": "May 20, 2025", "type": "Procedure", "chip": "chip-procedure",
                "provider": "Dr. Nguyen, MD — Oncology",
                "cc": "Cycle 3 chemotherapy administration and response assessment.",
                "subjective": "Patient reports manageable nausea (grade 1–2) following cycle 2. Fatigue significant on days 5–10 post-infusion. Appetite poor — 'I force myself to eat.' No fever, no infection symptoms. Peripheral neuropathy: mild tingling in fingertips. Reports emotional distress — 'I worry about my kids.'",
                "objective": "BP 130/82, HR 76, Temp 98.6°F, SpO₂ 96%. Weight: 172 lbs (↓ 4 lbs from cycle 2). ECOG performance status: 1. CBC pre-chemo: WBC 5.8, ANC 3.4 (adequate for treatment). Neuropathy assessment: grade 1 bilateral digital paraesthesia.",
                "assessment": "Stage IIB NSCLC — on treatment, tolerating cycle 3. Nausea — grade 1–2, manageable. Neuropathy — grade 1, monitor. Nutritional compromise — weight loss concerning. Psychological distress — significant.",
                "plan": "Administer Carboplatin AUC 5 + Pemetrexed 500 mg/m² IV. Ondansetron prophylaxis. Continue Omeprazole. Nutritionist consult urgent. Refer to oncology social worker and psychology. Neuropathy: continue monitoring; dose reduction threshold at grade 2+. CT thorax scheduled in 3 weeks for interim response. Next review in 4 weeks.",
            },
            {
                "date": "Apr 01, 2025", "type": "Follow-Up", "chip": "chip-follow-up",
                "provider": "Dr. Nguyen, MD — Oncology",
                "cc": "Post-cycle 2 review and lab interpretation.",
                "subjective": "Patient recovering from cycle 2. Reports nadir fatigue on days 7–9. Nausea controlled with Ondansetron. 'The hardest part is not being able to work.' No fever, no chills, no haemoptysis since starting treatment. GERD symptomatic — heartburn 3–4 ×/week.",
                "objective": "BP 128/80, HR 78. WBC 4.9, ANC 2.8. CEA: 6.2 ng/mL (↓ from 8.4 at diagnosis). CA 19-9: 87 U/mL (↓ from 140). Weight stable from last visit.",
                "assessment": "NSCLC — early tumour marker response; promising. GERD — breakthrough symptoms. Fatigue — expected post-chemotherapy nadir.",
                "plan": "Proceed to cycle 3 per schedule. Increase Omeprazole to 40 mg daily for GERD. Dietary modifications for reflux. Fatigue management: encourage short activity breaks, conserve energy. Palliative care team to touch base this week. Psycho-oncology referral placed.",
            },
        ],
    }

    visits = visit_notes[selected_patient]

    for i, visit in enumerate(visits):
        chip_label = visit["type"]
        with st.expander(f"📄 {visit['date']}  —  {visit['type']}  |  {visit['provider']}"):
            st.markdown(f"""
            <div style="margin-bottom:.8rem">
              <span class="visit-chip {visit['chip']}">{chip_label}</span>
              <span style="font-size:.82rem;color:#5a7a72">{visit['provider']}</span>
            </div>
            <div class="card" style="margin-bottom:.6rem;padding:1rem 1.3rem">
              <p style="font-size:.78rem;font-weight:700;color:#5a7a72;text-transform:uppercase;letter-spacing:.07em;margin:0 0 .25rem">Chief Complaint</p>
              <p style="font-size:.87rem;margin:0">{visit['cc']}</p>
            </div>
            """, unsafe_allow_html=True)

            c_s, c_o = st.columns(2)
            with c_s:
                st.markdown(f"""
                <div class="card" style="padding:1rem 1.3rem">
                  <p style="font-size:.78rem;font-weight:700;color:#5a7a72;text-transform:uppercase;letter-spacing:.07em;margin:0 0 .4rem">Subjective (S)</p>
                  <p style="font-size:.84rem;line-height:1.65;margin:0">{visit['subjective']}</p>
                </div>
                """, unsafe_allow_html=True)
            with c_o:
                st.markdown(f"""
                <div class="card" style="padding:1rem 1.3rem">
                  <p style="font-size:.78rem;font-weight:700;color:#5a7a72;text-transform:uppercase;letter-spacing:.07em;margin:0 0 .4rem">Objective (O)</p>
                  <p style="font-size:.84rem;line-height:1.65;margin:0">{visit['objective']}</p>
                </div>
                """, unsafe_allow_html=True)

            c_a, c_p = st.columns(2)
            with c_a:
                st.markdown(f"""
                <div class="card card-clay" style="padding:1rem 1.3rem">
                  <p style="font-size:.78rem;font-weight:700;color:#5a7a72;text-transform:uppercase;letter-spacing:.07em;margin:0 0 .4rem">Assessment (A)</p>
                  <p style="font-size:.84rem;line-height:1.65;margin:0">{visit['assessment']}</p>
                </div>
                """, unsafe_allow_html=True)
            with c_p:
                st.markdown(f"""
                <div class="card card-blue" style="padding:1rem 1.3rem">
                  <p style="font-size:.78rem;font-weight:700;color:#5a7a72;text-transform:uppercase;letter-spacing:.07em;margin:0 0 .4rem">Plan (P)</p>
                  <p style="font-size:.84rem;line-height:1.65;margin:0">{visit['plan']}</p>
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — HEALING ARTS
# ════════════════════════════════════════════════════════════════════════════════
elif view == "🎨 Healing Arts":

    st.markdown('<div class="section-title">Art & Healing</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#5a7a72;font-size:.92rem;margin-bottom:1.5rem'>"
        "Art can reduce anxiety, promote mindfulness, and support the healing process. "
        "These selections are thoughtfully curated to resonate with your health journey."
        "</p>", unsafe_allow_html=True
    )

    artworks = [
        {
            "emoji": "🌿", "bg": "linear-gradient(135deg,#d4e8e2,#a8d5c7)",
            "title": "The Water Lilies", "artist": "Claude Monet · 1906",
            "theme": "Calm & Serenity",
            "desc": "Monet's soft, shimmering water lilies invite a meditative stillness. Studies show that viewing nature-inspired art lowers cortisol and slows the heart rate — perfect for moments of recovery.",
            "benefit": ["Reduces anxiety", "Promotes calm"],
            "link": "https://www.moma.org/collection/works/80220",
            "link_label": "View at MoMA →",
        },
        {
            "emoji": "🌄", "bg": "linear-gradient(135deg,#fde8d4,#f5c9a0)",
            "title": "The Starry Night", "artist": "Vincent van Gogh · 1889",
            "theme": "Hope & Resilience",
            "desc": "Painted during his time in a sanatorium, Van Gogh transformed personal anguish into transcendent beauty. A powerful reminder that darkness can give birth to extraordinary light.",
            "benefit": ["Inspires resilience", "Emotional validation"],
            "link": "https://www.moma.org/collection/works/79802",
            "link_label": "View at MoMA →",
        },
        {
            "emoji": "🦋", "bg": "linear-gradient(135deg,#dce9f5,#b8d4ed)",
            "title": "The Birth of Venus", "artist": "Sandro Botticelli · 1485",
            "theme": "Renewal & New Beginnings",
            "desc": "This iconic Renaissance masterpiece celebrates emergence and transformation. Its themes of rebirth and grace mirror the patient's journey toward restored health and vitality.",
            "benefit": ["Encourages hope", "Symbolises transformation"],
            "link": "https://www.uffizi.it/en/artworks/birth-of-venus",
            "link_label": "View at Uffizi Gallery →",
        },
        {
            "emoji": "🌺", "bg": "linear-gradient(135deg,#f5e6f5,#e2bde2)",
            "title": "The Two Fridas", "artist": "Frida Kahlo · 1939",
            "theme": "Strength Through Pain",
            "desc": "Kahlo painted through chronic illness, turning suffering into self-affirmation. Her work speaks directly to those navigating long-term medical challenges — a testament to the power of identity and will.",
            "benefit": ["Validates suffering", "Affirms identity"],
            "link": "https://www.museodeartemoderno.mx/en/collection/the-two-fridas/",
            "link_label": "View at Museo de Arte Moderno →",
        },
        {
            "emoji": "🍃", "bg": "linear-gradient(135deg,#e8f5e0,#c2e09e)",
            "title": "The Great Wave off Kanagawa", "artist": "Katsushika Hokusai · 1831",
            "theme": "Courage in Adversity",
            "desc": "An immovable Mt Fuji behind a crashing wave — a metaphor for enduring stability within life's turbulent moments. Patients facing difficult treatments often connect with its message of inner steadiness.",
            "benefit": ["Builds courage", "Grounding perspective"],
            "link": "https://www.metmuseum.org/art/collection/search/45434",
            "link_label": "View at The Met →",
        },
        {
            "emoji": "☀️", "bg": "linear-gradient(135deg,#fef9d4,#f5e67a)",
            "title": "Irises", "artist": "Vincent van Gogh · 1889",
            "theme": "Finding Joy in Small Things",
            "desc": "Van Gogh painted this series to calm himself, focusing intently on the beauty of a single flower. Mindful art-viewing practices derived from works like this reduce perceived pain levels in clinical settings.",
            "benefit": ["Mindfulness practice", "Pain perception reduction"],
            "link": "https://www.getty.edu/art/collection/object/103JNH",
            "link_label": "View at The Getty →",
        },
    ]

    cols1 = st.columns(3)
    for i, art in enumerate(artworks[:3]):
        with cols1[i]:
            st.markdown(f"""
            <div class="art-card">
              <div class="art-canvas" style="background:{art['bg']}">{art['emoji']}</div>
              <div class="art-body">
                <div class="art-title">{art['title']}</div>
                <div class="art-sub">{art['artist']}</div>
                <div style="margin-top:.5rem"><span class="badge badge-green">{art['theme']}</span></div>
                <div class="art-desc">{art['desc']}</div>
                <div style="margin-top:.6rem">{''.join([f'<span class="badge badge-blue">{b}</span>' for b in art['benefit']])}</div>
                <div style="margin-top:.7rem"><a href="{art['link']}" target="_blank" style="font-size:.78rem;color:#4a7c6f;font-weight:600;text-decoration:none">🔗 {art['link_label']}</a></div>
              </div>
            </div>
            <br>
            """, unsafe_allow_html=True)

    cols2 = st.columns(3)
    for i, art in enumerate(artworks[3:]):
        with cols2[i]:
            st.markdown(f"""
            <div class="art-card">
              <div class="art-canvas" style="background:{art['bg']}">{art['emoji']}</div>
              <div class="art-body">
                <div class="art-title">{art['title']}</div>
                <div class="art-sub">{art['artist']}</div>
                <div style="margin-top:.5rem"><span class="badge badge-green">{art['theme']}</span></div>
                <div class="art-desc">{art['desc']}</div>
                <div style="margin-top:.6rem">{''.join([f'<span class="badge badge-blue">{b}</span>' for b in art['benefit']])}</div>
                <div style="margin-top:.7rem"><a href="{art['link']}" target="_blank" style="font-size:.78rem;color:#4a7c6f;font-weight:600;text-decoration:none">🔗 {art['link_label']}</a></div>
              </div>
            </div>
            <br>
            """, unsafe_allow_html=True)

    # ── Medical Quotes ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Words That Heal</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#5a7a72;font-size:.88rem;margin-bottom:1.2rem'>Wisdom from physicians, writers, and healers across the centuries.</p>", unsafe_allow_html=True)

    quotes = [
        ("The art of medicine consists of amusing the patient while nature cures the disease.", "Voltaire"),
        ("Wherever the art of medicine is loved, there is also a love of humanity.", "Hippocrates"),
        ("The good physician treats the disease; the great physician treats the patient who has the disease.", "William Osler"),
        ("To cure sometimes, to relieve often, to comfort always.", "Edward Livingston Trudeau"),
        ("The greatest medicine of all is teaching people how not to need it.", "Hippocrates"),
        ("Healing is a matter of time, but it is sometimes also a matter of opportunity.", "Hippocrates"),
        ("Medicine is not only a science; it is also an art. It does not consist of compounding pills and plasters; it deals with the very processes of life.", "Paracelsus"),
        ("The body heals with play, the mind heals with laughter, and the spirit heals with joy.", "Proverb"),
    ]

    q_cols = st.columns(2)
    for idx, (quote, attr) in enumerate(quotes):
        with q_cols[idx % 2]:
            st.markdown(f"""
            <div class="quote-block">
              "{quote}"
              <div class="quote-attr">— {attr}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Recommended Books ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recommended Reading</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#5a7a72;font-size:.88rem;margin-bottom:1.2rem'>Books at the intersection of medicine, humanity, and healing — for patients and caregivers alike.</p>", unsafe_allow_html=True)

    books = [
        {
            "emoji": "📗", "bg": "#d4e8e2",
            "title": "When Breath Becomes Air",
            "author": "Paul Kalanithi",
            "year": "2016",
            "desc": "A neurosurgeon confronts a terminal lung cancer diagnosis and writes a profound memoir about mortality, meaning, and what makes life worth living. Essential reading for anyone facing serious illness.",
            "tags": ["Terminal Illness", "Mortality", "Memoir"],
            "link": "https://www.goodreads.com/book/show/25899336",
        },
        {
            "emoji": "📘", "bg": "#dce9f5",
            "title": "Being Mortal",
            "author": "Atul Gawande",
            "year": "2014",
            "desc": "A surgeon and public health researcher examines how medicine can better support the elderly and dying — arguing for dignity and autonomy over endless intervention.",
            "tags": ["End of Life", "Geriatrics", "Medical Ethics"],
            "link": "https://www.goodreads.com/book/show/20696006",
        },
        {
            "emoji": "📙", "bg": "#fde8d4",
            "title": "The Emperor of All Maladies",
            "author": "Siddhartha Mukherjee",
            "year": "2010",
            "desc": "Pulitzer Prize–winning biography of cancer — its history, science, and the human stories behind one of medicine's most formidable challenges. A landmark work of science writing.",
            "tags": ["Oncology", "History of Medicine", "Science"],
            "link": "https://www.goodreads.com/book/show/7170627",
        },
        {
            "emoji": "📕", "bg": "#fde4e4",
            "title": "The Body Keeps the Score",
            "author": "Bessel van der Kolk",
            "year": "2014",
            "desc": "Groundbreaking exploration of how trauma reshapes the body and brain, and the therapies — from yoga to EMDR — that help people reclaim their lives.",
            "tags": ["Mental Health", "Trauma", "Neuroscience"],
            "link": "https://www.goodreads.com/book/show/18693771",
        },
        {
            "emoji": "📒", "bg": "#fef9d4",
            "title": "Mountains Beyond Mountains",
            "author": "Tracy Kidder",
            "year": "2003",
            "desc": "The story of Dr. Paul Farmer — infectious disease physician and humanitarian — and his mission to deliver healthcare to the world's poorest communities.",
            "tags": ["Global Health", "Inspiration", "Biography"],
            "link": "https://www.goodreads.com/book/show/337732",
        },
        {
            "emoji": "📓", "bg": "#ede8f5",
            "title": "Do No Harm",
            "author": "Henry Marsh",
            "year": "2014",
            "desc": "A British neurosurgeon reflects candidly on decades of operations — the successes, the failures, and the impossible decisions that define a life in medicine.",
            "tags": ["Surgery", "Ethics", "Memoir"],
            "link": "https://www.goodreads.com/book/show/20696002",
        },
    ]

    b_cols = st.columns(3)
    for idx, book in enumerate(books):
        with b_cols[idx % 3]:
            tags_html = "".join([
                '<span class="badge badge-blue" style="font-size:.68rem">' + t + '</span>'
                for t in book["tags"]
            ])
            bg    = book["bg"]
            emoji = book["emoji"]
            title = book["title"]
            auth  = book["author"]
            yr    = book["year"]
            desc  = book["desc"]
            link  = book["link"]
            html  = (
                '<div class="art-card" style="margin-bottom:1rem">'
                '<div class="art-canvas" style="background:' + bg + ';height:100px;font-size:3rem">' + emoji + '</div>'
                '<div class="art-body">'
                '<div class="art-title">' + title + '</div>'
                '<div class="art-sub">' + auth + ' · ' + yr + '</div>'
                '<div style="margin-top:.4rem">' + tags_html + '</div>'
                '<div class="art-desc">' + desc + '</div>'
                '<div style="margin-top:.7rem">'
                '<a href="' + link + '" target="_blank" '
                'style="font-size:.78rem;color:#4a7c6f;font-weight:600;text-decoration:none">'
                '📖 View on Goodreads →</a>'
                '</div>'
                '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)
    # ── Art Therapy Stats ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">The Science of Art Therapy</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2.5rem;font-family:\'DM Serif Display\',serif;color:#4a7c6f">45%</div><div style="font-size:.85rem;color:#5a7a72;margin-top:.3rem">reduction in anxiety reported by patients engaged in visual art therapy programmes</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2.5rem;font-family:\'DM Serif Display\',serif;color:#c17a4a">30%</div><div style="font-size:.85rem;color:#5a7a72;margin-top:.3rem">decrease in pain perception for patients who engage with art during treatment</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2.5rem;font-family:\'DM Serif Display\',serif;color:#4a90d9">2x</div><div style="font-size:.85rem;color:#5a7a72;margin-top:.3rem">more likely to report positive mood following structured art therapy sessions</div></div>', unsafe_allow_html=True)

    with st.expander("📚 Art Therapy Resources & Further Reading"):
        st.markdown("""
- **American Art Therapy Association** — [arttherapy.org](https://arttherapy.org)
- **Cleveland Clinic Arts & Medicine Institute** — [my.clevelandclinic.org](https://my.clevelandclinic.org/departments/wellness/integrative/arts-medicine)
- **Global Alliance for Arts & Health** — [thesah.org](https://thesah.org)
- *"The Effects of Art on Healing"* — Journal of Pain and Symptom Management, 2023
- *Healing Arts* by Noah Charney — accessible introduction to art in medical contexts
        """)


# ════════════════════════════════════════════════════════════════════════════════
# FOOTER — appears on every page
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-banner">
  <b>Important Disclaimer</b><br>
  This dashboard is entirely <b>simulated</b>. All patient names, diagnoses, medications, lab values,
  visit notes, and clinical data are <b>fictitious and generated for educational purposes only</b>.
  This is <b>not medical advice</b>. Nothing presented here should be used to inform real healthcare
  decisions. Always consult a qualified, licensed healthcare professional for any medical concerns.<br><br>
  <b>Academic Project</b> &nbsp;·&nbsp; Created for <b>SCIE 4392</b> — Final Creative Project
  &nbsp;·&nbsp; Created by <b>Alain Siddiqui</b>
  &nbsp;·&nbsp; All artwork links direct to public museum collections. Book links direct to Goodreads.
</div>
""", unsafe_allow_html=True)
