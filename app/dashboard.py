import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

@st.cache_data
def load_all_data():
    fit_df = pd.read_excel("assets/Player Fit & Comfort Data.xlsx")
    impact_df = pd.read_excel("assets/Impact & Collision Data.xlsx")
    materials_df = pd.read_excel("assets/Materials Testing Data.xlsx")
    safety_df = pd.read_excel("assets/Safety Performance Data.xlsx")
    return fit_df, impact_df, materials_df, safety_df

def generate_pdf(avg_comfort, concussion_reduction, avg_durability, pass_rate):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Riddell Helmet R&D Executive Summary", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Average Fit Comfort Score: {avg_comfort:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Avg Concussion Risk Reduction: {concussion_reduction:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Avg Material Durability Score: {avg_durability:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Safety Test Pass Rate: {pass_rate:.2f}%", ln=True)
    pdf.cell(200, 10, txt="AI Insights:", ln=True)
    if avg_comfort < 85:
        pdf.cell(200, 10, txt="- Helmet fit comfort below optimal.", ln=True)
    if concussion_reduction < 15:
        pdf.cell(200, 10, txt="- Concussion risk reduction marginal.", ln=True)
    if avg_durability < 80:
        pdf.cell(200, 10, txt="- Material durability below threshold.", ln=True)
    if pass_rate < 95:
        pdf.cell(200, 10, txt="- Safety test pass rate below standard.", ln=True)
    return pdf

def run():
    st.header("📊 R&D Executive Dashboard")

    role = st.session_state.get("user_role", "analyst")  # fallback to analyst

    fit_df, impact_df, materials_df, safety_df = load_all_data()

    avg_comfort = fit_df['comfortRating'].mean()
    concussion_reduction = 100 - (impact_df['injuryReported'].mean() * 100)
    avg_durability = materials_df['durabilityScore'].mean()
    pass_rate = safety_df['pass'].value_counts(normalize=True).get(True, 0) * 100

    st.subheader("📈 Key Performance Indicators")
    st.metric("Average Fit Comfort Score", f"{avg_comfort:.2f}")
    st.metric("Avg Concussion Risk Reduction", f"{concussion_reduction:.2f}%")
    st.metric("Avg Material Durability Score", f"{avg_durability:.2f}")
    st.metric("Safety Test Pass Rate", f"{pass_rate:.2f}%")

    st.subheader("💡 AI-Powered Insights")
    if avg_comfort < 85:
        st.warning("⚠️ Helmet fit comfort is below optimal. Recommend design adjustments.")
    if concussion_reduction < 15:
        st.warning("⚠️ Concussion risk reduction is marginal. Review impact absorption materials.")
    if avg_durability < 80:
        st.warning("⚠️ Material durability is below threshold. Evaluate alternative materials.")
    if pass_rate < 95:
        st.warning("⚠️ Safety test pass rate below desired standards.")
    else:
        st.success("✅ All modules performing within expected ranges.")

    if role in ['executive', 'admin']:
        st.subheader("🧾 Download Executive Summary PDF")
        if st.button("📥 Generate PDF"):
            pdf = generate_pdf(avg_comfort, concussion_reduction, avg_durability, pass_rate)
            pdf.output("Executive_Report.pdf")
            with open("Executive_Report.pdf", "rb") as file:
                st.download_button("📄 Download Executive Report", file, file_name="Executive_Report.pdf")

    if role != 'executive':
        st.subheader("📊 Interactive Visualizations")
        fig1 = px.histogram(fit_df, x='helmetSize', title='Helmet Size Distribution')
        st.plotly_chart(fig1)

        fig2 = px.scatter(materials_df, x='cost', y='durabilityScore', color='foamType', title='Cost vs Durability by Foam Type')
        st.plotly_chart(fig2)

        fig3 = px.box(safety_df, x='helmetModel', y='HIC15', title='HIC15 Distribution per Helmet Model')
        st.plotly_chart(fig3)

    st.caption("✅ Role-based dashboard with embedded insights and reporting capabilities.")
