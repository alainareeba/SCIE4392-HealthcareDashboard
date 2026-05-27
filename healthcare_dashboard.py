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

  /* Root tokens */
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

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: var(--sage) !important;
  }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stRadio label { color: white !important; }

  /* Headings */
  h1, h2, h3, h4 { font-family: 'DM Serif Display', serif !important; color: var(--slate) !important; }

  /* Metric cards */
  [data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1rem;
    border-left: 4px solid var(--sage);
    box-shadow: 0 2px 12px rgba(74,124,111,.10);
  }
  [data-testid="stMetricValue"] { color: var(--sage) !important; font-weight: 600; }
  [data-testid="stMetricLabel"] { color: var(--sub) !important; font-size: .85rem !important; }

  /* Cards */
  .card {
    background: white;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 16px rgba(74,124,111,.08);
    border-top: 3px solid var(--sage);
  }
  .card-clay { border-top-color: var(--clay); }

  /* Pills / badges */
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

  /* Section divider */
  .section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--sage);
    border-bottom: 2px solid var(--sage-lt);
    padding-bottom: .4rem;
    margin-bottom: 1.2rem;
  }

  /* Art card */
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

  /* Timeline */
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
  .timeline-dot.clay { background: var(--clay); }

  /* Tabs override */
  .stTabs [role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500;
    color: var(--sub) !important;
  }
  .stTabs [aria-selected="true"] {
    color: var(--sage) !important;
    border-bottom-color: var(--sage) !important;
  }

  /* Progress bars */
  .prog-wrap { margin-bottom: .8rem; }
  .prog-label { font-size: .82rem; color: var(--sub); display: flex; justify-content: space-between; margin-bottom: .25rem; }
  .prog-bar { height: 8px; background: var(--sage-lt); border-radius: 999px; overflow: hidden; }
  .prog-fill { height: 100%; background: var(--sage); border-radius: 999px; transition: width .6s; }
  .prog-fill.clay { background: var(--clay); }
  .prog-fill.blue { background: #4a90d9; }

  hr { border: none; border-top: 1px solid var(--sage-lt); margin: 1.2rem 0; }

  /* Expander */
  .streamlit-expanderHeader { color: var(--sage) !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🫀 Health Portal")
    st.markdown("---")

    patients = {
        "Sarah Chen, 42":    {"dob": "1982-04-15", "id": "P-2847", "blood": "A+",  "doctor": "Dr. Reyes",   "dept": "Cardiology"},
        "Marcus Webb, 67":   {"dob": "1957-09-03", "id": "P-1193", "blood": "O−",  "doctor": "Dr. Okafor",  "dept": "Internal Medicine"},
        "Aisha Patel, 29":   {"dob": "1995-01-22", "id": "P-3561", "blood": "B+",  "doctor": "Dr. Lin",     "dept": "Endocrinology"},
        "David Torres, 54":  {"dob": "1970-07-30", "id": "P-0984", "blood": "AB+", "doctor": "Dr. Nguyen",  "dept": "Oncology"},
    }

    selected_patient = st.selectbox("Select Patient", list(patients.keys()))
    pt = patients[selected_patient]

    st.markdown("---")
    st.markdown(f"**Patient ID:** `{pt['id']}`")
    st.markdown(f"**Blood Type:** {pt['blood']}")
    st.markdown(f"**Physician:** {pt['doctor']}")
    st.markdown(f"**Department:** {pt['dept']}")
    st.markdown("---")

    view = st.radio("Navigate", ["📋 Overview", "💊 Treatment Plan", "🛡️ Preventative Health", "🎨 Healing Arts"])
    st.markdown("---")
    st.markdown("<small style='opacity:.7'>Last updated: " + datetime.now().strftime("%b %d, %Y %H:%M") + "</small>", unsafe_allow_html=True)


name  = selected_patient.split(",")[0]
age   = int(selected_patient.split(", ")[1])

# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"<h1 style='margin-bottom:0'>Welcome back, {name.split()[0]}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#5a7a72;font-size:1rem;margin-top:.2rem'>Patient ID {pt['id']} · {pt['dept']} · {pt['doctor']}</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
if view == "📋 Overview":

    # ── Vitals strip ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Vitals at a Glance</div>', unsafe_allow_html=True)

    vitals_data = {
        "Sarah Chen, 42":   {"hr": 72,  "bp": "118/76", "temp": 98.4, "o2": 98, "bmi": 23.4, "weight": "138 lbs"},
        "Marcus Webb, 67":  {"hr": 81,  "bp": "142/88", "temp": 98.9, "o2": 95, "bmi": 27.1, "weight": "198 lbs"},
        "Aisha Patel, 29":  {"hr": 68,  "bp": "110/70", "temp": 98.2, "o2": 99, "bmi": 21.8, "weight": "126 lbs"},
        "David Torres, 54": {"hr": 76,  "bp": "130/82", "temp": 98.6, "o2": 96, "bmi": 25.3, "weight": "172 lbs"},
    }
    v = vitals_data[selected_patient]

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Heart Rate",    f"{v['hr']} bpm",  delta="−3 bpm")
    c2.metric("Blood Pressure", v['bp'],           delta="Stable")
    c3.metric("Temperature",   f"{v['temp']}°F",  delta="Normal")
    c4.metric("O₂ Saturation", f"{v['o2']}%",     delta="+1%")
    c5.metric("BMI",           str(v['bmi']),      delta="Healthy")
    c6.metric("Weight",        v['weight'],        delta="−2 lbs")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Patient profile + conditions ─────────────────────────────────────────
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

    # ── Vital history chart ───────────────────────────────────────────────────
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
    fig.add_trace(go.Scatter(x=months, y=hr_vals,  name="Heart Rate",      line=dict(color="#4a7c6f", width=2.5), mode="lines+markers"))
    fig.add_trace(go.Scatter(x=months, y=sys_vals, name="Systolic BP",     line=dict(color="#c17a4a", width=2.5), mode="lines+markers"))
    fig.add_trace(go.Scatter(x=months, y=dia_vals, name="Diastolic BP",    line=dict(color="#4a90d9", width=2.5), mode="lines+markers", line_dash="dot"))
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
        # Goals
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

        # Physician notes
        st.markdown("**📝 Physician Notes**")
        st.markdown(f'<div class="card card-clay"><p style="font-size:.88rem;line-height:1.65;margin:0">{plan["notes"]}</p></div>', unsafe_allow_html=True)

    with col2:
        # Medications
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

    # Appointments timeline
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

        # Vaccines
        st.markdown("**💉 Immunisation Record**")
        vaccines = {
            "Sarah Chen, 42":   [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Oct 2024", "green"), ("Tdap", "2020", "green"), ("Hepatitis B", "Complete", "green")],
            "Marcus Webb, 67":  [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Oct 2024", "green"), ("Pneumococcal", "2022", "green"), ("Shingles (Shingrix)", "2019", "orange")],
            "Aisha Patel, 29":  [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Oct 2024", "green"), ("HPV (Gardasil)", "2018", "green"), ("MMR", "Childhood", "green")],
            "David Torres, 54": [("COVID-19 Booster", "2024", "green"), ("Flu Vaccine", "Due Oct 2025", "orange"), ("Pneumococcal", "Not done", "red"), ("Hepatitis B", "Complete", "green")],
        }
        badges = "".join([f'<span class="badge badge-{c}">{v} · {yr}</span>' for v, yr, c in vaccines[selected_patient]])
        st.markdown(f'<div class="card">{badges}</div>', unsafe_allow_html=True)

    # Radar chart
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
        polar=dict(bgcolor='white', radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor="#eef4f2"), angularaxis=dict(gridcolor="#eef4f2")),
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='DM Sans', color='#2c3e50'),
        margin=dict(l=30, r=30, t=20, b=20), height=300,
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — HEALING ARTS
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
        },
        {
            "emoji": "🌄", "bg": "linear-gradient(135deg,#fde8d4,#f5c9a0)",
            "title": "Starry Night", "artist": "Vincent van Gogh · 1889",
            "theme": "Hope & Resilience",
            "desc": "Painted during his time in a sanatorium, Van Gogh transformed personal anguish into transcendent beauty. A powerful reminder that darkness can give birth to extraordinary light.",
            "benefit": ["Inspires resilience", "Emotional validation"],
        },
        {
            "emoji": "🦋", "bg": "linear-gradient(135deg,#dce9f5,#b8d4ed)",
            "title": "The Birth of Venus", "artist": "Sandro Botticelli · 1485",
            "theme": "Renewal & New Beginnings",
            "desc": "This iconic Renaissance masterpiece celebrates emergence and transformation. Its themes of rebirth and grace mirror the patient's journey toward restored health and vitality.",
            "benefit": ["Encourages hope", "Symbolises transformation"],
        },
        {
            "emoji": "🌺", "bg": "linear-gradient(135deg,#f5e6f5,#e2bde2)",
            "title": "Two Fridas", "artist": "Frida Kahlo · 1939",
            "theme": "Strength Through Pain",
            "desc": "Kahlo painted through chronic illness, turning suffering into self-affirmation. Her work speaks directly to those navigating long-term medical challenges — a testament to the power of identity and will.",
            "benefit": ["Validates suffering", "Affirms identity"],
        },
        {
            "emoji": "🍃", "bg": "linear-gradient(135deg,#e8f5e0,#c2e09e)",
            "title": "The Great Wave", "artist": "Katsushika Hokusai · 1831",
            "theme": "Courage in Adversity",
            "desc": "An immovable Mt Fuji behind a crashing wave — a metaphor for enduring stability within life's turbulent moments. Patients facing difficult treatments often connect with its message of inner steadiness.",
            "benefit": ["Builds courage", "Grounding perspective"],
        },
        {
            "emoji": "☀️", "bg": "linear-gradient(135deg,#fef9d4,#f5e67a)",
            "title": "Irises", "artist": "Vincent van Gogh · 1889",
            "theme": "Finding Joy in Small Things",
            "desc": "Van Gogh painted this series to calm himself, focusing intently on the beauty of a single flower. Mindful art-viewing practices derived from works like this reduce perceived pain levels in clinical settings.",
            "benefit": ["Mindfulness practice", "Pain perception reduction"],
        },
    ]

    # Row 1
    cols1 = st.columns(3)
    for i, art in enumerate(artworks[:3]):
        with cols1[i]:
            st.markdown(f"""
            <div class="art-card">
              <div class="art-canvas" style="background:{art['bg']}">{art['emoji']}</div>
              <div class="art-body">
                <div class="art-title">{art['title']}</div>
                <div class="art-sub">{art['artist']}</div>
                <div style="margin-top:.5rem">
                  <span class="badge badge-green">{art['theme']}</span>
                </div>
                <div class="art-desc">{art['desc']}</div>
                <div style="margin-top:.6rem">
                  {''.join([f'<span class="badge badge-blue">{b}</span>' for b in art['benefit']])}
                </div>
              </div>
            </div>
            <br>
            """, unsafe_allow_html=True)

    # Row 2
    cols2 = st.columns(3)
    for i, art in enumerate(artworks[3:]):
        with cols2[i]:
            st.markdown(f"""
            <div class="art-card">
              <div class="art-canvas" style="background:{art['bg']}">{art['emoji']}</div>
              <div class="art-body">
                <div class="art-title">{art['title']}</div>
                <div class="art-sub">{art['artist']}</div>
                <div style="margin-top:.5rem">
                  <span class="badge badge-green">{art['theme']}</span>
                </div>
                <div class="art-desc">{art['desc']}</div>
                <div style="margin-top:.6rem">
                  {''.join([f'<span class="badge badge-blue">{b}</span>' for b in art['benefit']])}
                </div>
              </div>
            </div>
            <br>
            """, unsafe_allow_html=True)

    # Evidence section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">The Science of Art Therapy</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div class="card" style="text-align:center">
          <div style="font-size:2.5rem;font-family:'DM Serif Display',serif;color:#4a7c6f">45%</div>
          <div style="font-size:.85rem;color:#5a7a72;margin-top:.3rem">reduction in anxiety reported by patients engaged in visual art therapy programmes</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="card" style="text-align:center">
          <div style="font-size:2.5rem;font-family:'DM Serif Display',serif;color:#c17a4a">30%</div>
          <div style="font-size:.85rem;color:#5a7a72;margin-top:.3rem">decrease in pain perception for patients who engage with art during treatment</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div class="card" style="text-align:center">
          <div style="font-size:2.5rem;font-family:'DM Serif Display',serif;color:#4a90d9">2×</div>
          <div style="font-size:.85rem;color:#5a7a72;margin-top:.3rem">more likely to report positive mood following structured art therapy sessions</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📚 Art Therapy Resources & Further Reading"):
        st.markdown("""
        - **American Art Therapy Association** — arttherapy.org
        - *"The Effects of Art on Healing"* — Journal of Pain and Symptom Management, 2023
        - **Cleveland Clinic Arts & Medicine Institute** — structured in-hospital programmes
        - *Healing Arts* by Noah Charney — accessible introduction to art in medical contexts
        - **Global Alliance for Arts & Health** — thesah.org
        """)
