from datetime import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="PulseTriage - DM Decision Engine", page_icon="🏥", layout="wide"
)

# Custom Styling (Light Coral Red Gradient at Top)
st.markdown(
    """
    <style>
    /* App Background Gradient: Light Coral Red (#FFE4E1) at Top fading to Slate Gray (#F1F5F9) */
    .stApp {
        background: linear-gradient(180deg, #FFE4E1 0%, #F8FAFC 22%, #F1F5F9 100%);
        background-attachment: fixed;
    }
    
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E293B; }
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

# Application Title & Subtitle
st.markdown(
    "<div class='main-header'>🏥 PulseTriage: Clinical Decision Support System</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='sub-header'>A Discrete Mathematics Application using Propositional Logic & Truth Table Evaluation</div>",
    unsafe_allow_html=True,
)

st.write("---")

# Main Layout
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    st.subheader("📋 Step 1: Patient Symptom & Vitals Assessment")

    st.markdown("#### **Primary Symptoms (Propositions)**")
    c1, c2 = st.columns(2)
    with c1:
        fever = st.checkbox("High Fever / Chills [P]", help="Body Temp ≥ 101°F")
        breathless = st.checkbox(
            "Shortness of Breath [Q]", help="Respiratory distress observed"
        )
    with c2:
        cough = st.checkbox(
            "Severe / Persistent Cough [S]", help="Productive or dry cough"
        )
        chest_pain = st.checkbox(
            "Chest Tightness / Pain [T]", help="Pressure or sharp chest pain"
        )

    st.markdown("#### **Vitals Data (Inputs for Logical Propositions)**")
    v1, v2 = st.columns(2)
    with v1:
        temp_val = st.slider("Body Temperature (°F)", 96.0, 105.0, 98.6, 0.1)
    with v2:
        spo2_val = st.slider("Oxygen Saturation - SpO2 (%)", 70, 100, 98, 1)

    # Derived Propositional Logic Variables
    low_spo2 = spo2_val < 95  # Proposition R
    critical_fever = temp_val >= 101.0  # Refinement for P

with col_right:
    st.subheader("⚙️ Step 2: Diagnostic Output & Action")

    # Evaluate Logical Propositions
    P = fever or critical_fever
    Q = breathless
    R = low_spo2
    S = cough
    T = chest_pain

    # Propositional Logic Rules
    # Rule 1 (Critical): (P AND (Q OR R)) OR T
    is_critical = (P and (Q or R)) or T

    # Rule 2 (Urgent): (P AND S) AND NOT (Q OR R)
    is_urgent = (P and S) and not (Q or R)

    st.markdown("#### **Current Evaluation Status**")

    if is_critical:
        st.error("🚨 **PRIORITY 1: CRITICAL / EMERGENCY**")
        st.markdown("""
        * **Clinical Action:** Immediate emergency transport, oxygen therapy, and physician escalation.
        * **Discrete Math Rule:** $(P \\wedge (Q \\vee R)) \\vee T = \\text{TRUE}$
        """)
    elif is_urgent:
        st.warning("⚠️ **PRIORITY 2: URGENT CARE**")
        st.markdown("""
        * **Clinical Action:** Priority consultation within 2 hours. Start oral rehydration and monitoring.
        * **Discrete Math Rule:** $((P \\wedge S) \\wedge \\neg(Q \\vee R)) = \\text{TRUE}$
        """)
    else:
        st.success("🟢 **PRIORITY 3: ROUTINE / MONITORED**")
        st.markdown("""
        * **Clinical Action:** Home-care protocol, basic antipyretics if needed, and 24-hour symptom check.
        * **Discrete Math Rule:** Fallback State $(\\neg\\text{Rule}_1 \\wedge \\neg\\text{Rule}_2)$
        """)

    # Professional Clinical & Mathematical Report Generator
    triage_status = (
        "PRIORITY 1: CRITICAL / EMERGENCY"
        if is_critical
        else (
            "PRIORITY 2: URGENT CARE"
            if is_urgent
            else "PRIORITY 3: ROUTINE / MONITORED"
        )
    )

    formula_used = (
        "(P ∧ (Q ∨ R)) ∨ T"
        if is_critical
        else (
            "((P ∧ S) ∧ ¬(Q ∨ R))" if is_urgent else "¬(Rule_1) ∧ ¬(Rule_2)"
        )
    )

    action_plan = (
        "Immediate emergency transport, high-flow oxygen, and physician escalation."
        if is_critical
        else (
            "Priority consultation within 2 hours. Start oral rehydration and monitoring."
            if is_urgent
            else "Home-care protocol, basic antipyretics if needed, and 24-hour symptom check."
        )
    )

    report_data = f"""================================================================================
                PULSETRIAGE: CLINICAL DECISION SUPPORT REPORT
================================================================================
Generated On        : {datetime.now().strftime('%Y-%m-%d at %I:%M %p')}
System Version      : 2.1 (Discrete Math Propositional Logic Engine)
Target Deployment   : Rural & Primary Health Centers (PHCs)
================================================================================

1. PATIENT VITALS & OBSERVATIONS
--------------------------------------------------------------------------------
- Body Temperature  : 
{temp_val:.1f} °F  [Threshold ≥ 101.0°F]
- Oxygen Saturation : 
{spo2_val}%       [Threshold < 95%]
- Observed Symptoms : 
{', '.join([name for name, val in [('Fever', fever), ('Shortness of Breath', breathless), ('Cough', cough), ('Chest Pain', chest_pain)] if val]) or 'None reported'}

2. EVALUATION
--------------------------------------------------------------------------------
[P] High Fever / Temp ≥ 101°F : {P}
[Q] Shortness of Breath       : {Q}
[R] Low SpO2 (< 95%)          : {R}
[S] Severe / Persistent Cough : {S}
[T] Chest Tightness / Pain    : {T}

3. DIAGNOSTIC TRIAGE RESULT
--------------------------------------------------------------------------------
FINAL ASSESSMENT    : {triage_status}
LOGICAL FORMULA     : {formula_used} = TRUE
RECOMMENDED ACTION  : {action_plan}

4. MATHEMATICAL VERIFICATION & PROOF
--------------------------------------------------------------------------------
The priority result was determined deterministically through Boolean proposition 
evaluation. Rule precedence evaluates Critical conditions first, followed by Urgent 
conditions, defaulting to Routine care under null-trigger states. All results are 
potential threats only for the project, not clinically tested.

================================================================================
CONFIDENTIAL - FOR RURAL HEALTH WORKER & CLINICAL EVALUATION PURPOSES ONLY
================================================================================
"""

    st.download_button(
        label="📄 Download Patient Triage Summary (.txt)",
        data=report_data,
        file_name=f"triage_summary_{datetime.now().strftime('%H%M%S')}.txt",
        mime="text/plain",
    )

st.write("---")

# Discrete Math Theory & Truth Table Section
st.subheader("📊 Discrete Mathematics Foundations")
tab1, tab2 = st.tabs([" Truth Table Evaluation", " Proposition Definitions"])

with tab1:
    st.write("Truth table for evaluated propositions based on current inputs:")
    tt_data = {
        "Proposition": [
            "P (Fever/Temp)",
            "Q (Breathless)",
            "R (Low SpO2)",
            "S (Cough)",
            "T (Chest Pain)",
        ],
        "Value": [P, Q, R, S, T],
        "Interpretation": [
            "Temp ≥ 101°F or Checked" if P else "Normal Temp",
            "Shortness of Breath Present" if Q else "Normal Breathing",
            "SpO2 < 95% (Hypoxia Risk)" if R else "SpO2 Normal",
            "Cough Present" if S else "No Cough",
            "Chest Pain Present" if T else "No Chest Pain",
        ],
    }
    st.table(pd.DataFrame(tt_data))

with tab2:
    st.markdown("""
    * **Logical Connectives Used:**
      * **Conjunction ($\wedge$):** Represents `AND`—both conditions must be true.
      * **Disjunction ($\vee$):** Represents `OR`—at least one condition must be true.
      * **Negation ($\neg$):** Represents `NOT`—reverses truth value.
    * **Societal Value:** Automates initial triage for primary healthcare centers where doctors are not immediately present.
    """)