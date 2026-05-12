import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI Client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# App Title
st.title("AI Prototype: Unified Human & Non-Human Identity Intelligence Platform")

st.write("""
This prototype explores AI-driven governance and lifecycle intelligence
across human and non-human identities including service accounts,
workload identities, APIs, automation accounts and AI agents.
""")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Identity Dataset",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Identity Data")
    st.dataframe(df)

    findings = []

    # Identity analysis logic
    for index, row in df.iterrows():

        risk_score = 0
        issues = []

        # High privilege
        if row["privilege_level"] == "high":
            risk_score += 40
            issues.append("High privilege identity")

        # Dormant identity
        if row["last_activity_days"] > 90:
            risk_score += 30
            issues.append("Dormant identity")

        # Missing owner
        if row["owner"] == "none":
            risk_score += 30
            issues.append("Missing ownership")

        # Non-human identity risks
        if row["identity_type"] != "human":

            risk_score += 20

            if row["credential_rotation"] == "no":
                risk_score += 30
                issues.append("Credential rotation gap")

        # AI Agent
        if row["identity_type"] == "ai_agent":
            risk_score += 30
            issues.append("AI agent governance required")

        findings.append({
            "identity": row["identity"],
            "identity_type": row["identity_type"],
            "risk_score": risk_score,
            "issues": ", ".join(issues)
        })

    risk_df = pd.DataFrame(findings)

    # Display findings
    st.subheader("Unified Identity Risk Findings")

    st.dataframe(risk_df)

    # High risk identities
    high_risk = risk_df[risk_df["risk_score"] >= 60]

    st.subheader("High Risk Identities")

    st.dataframe(high_risk)

    # Charts
    st.bar_chart(
        high_risk.set_index("identity")["risk_score"]
    )

    # Metrics
    st.metric(
        "High Risk Identities",
        len(high_risk)
    )

    # AI Insights
    st.subheader("AI Governance Intelligence")

    summary = high_risk.to_string(index=False)

    prompt = f"""
    Analyze the following human and non-human identity governance findings.

    Identify:
    - machine identity governance gaps
    - service account lifecycle risks
    - AI agent governance concerns
    - ownership weaknesses
    - credential management risks
    - operational governance issues

    Recommend:
    - governance improvements
    - lifecycle management controls
    - AI identity governance recommendations
    - workload identity governance strategies
    - remediation priorities

    Findings:
    {summary}
    """

    with st.spinner("Generating AI governance insights..."):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior identity governance and machine identity security expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        output = response.choices[0].message.content

        st.write(output)
