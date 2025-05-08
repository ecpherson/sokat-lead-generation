import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="SoKat Lead Generation",
    page_icon="📊",
    layout="wide"
)

# Authentication (simplified for demo)
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
        else:
            st.sidebar.error("Invalid credentials")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login if not logged in
if not st.session_state.logged_in:
    login()
    st.title("SoKat AI-Powered Lead Generation")
    st.write("Please log in to access the dashboard")
    st.image("https://www.sokatai.com/wp-content/uploads/2023/08/sokatai-logo.png", width=200)
    st.stop()

# Sample data (for demo purposes)
@st.cache_data
def load_sample_data():
    # Generate sample lead data
    companies = ["TechCorp", "FinanceX", "HealthPlus", "RetailGiant", "EduSmart"]
    industries = ["Technology", "Finance", "Healthcare", "Retail", "Education"]
    sources = ["Website", "Social Media", "Referral", "Event", "Cold Call"]
    categories = ["Hot", "Warm", "Cold"]
    
    # Create 50 sample leads
    np.random.seed(42)
    leads = []
    for i in range(50):
        company_idx = np.random.randint(0, len(companies))
        score = np.random.randint(1, 101)
        
        if score >= 70:
            category = "Hot"
        elif score >= 40:
            category = "Warm"
        else:
            category = "Cold"
        
        # Generate date within the last 30 days
        days_ago = np.random.randint(0, 30)
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        leads.append({
            "id": f"LD{i+1000}",
            "name": f"Contact {i+1}",
            "email": f"contact{i+1}@example.com",
            "company": companies[company_idx],
            "industry": industries[np.random.randint(0, len(industries))],
            "source": sources[np.random.randint(0, len(sources))],
            "interest": f"Interested in AI solutions for {industries[np.random.randint(0, len(industries))]}",
            "score": score,
            "category": category,
            "created_at": date
        })
    
    return pd.DataFrame(leads)

leads_df = load_sample_data()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Leads", "Add Lead", "Analytics", "Settings"])

# Dashboard page
if page == "Dashboard":
    st.title("SoKat Lead Generation Dashboard")
    
    # Key metrics
    total_leads = len(leads_df)
    hot_leads = len(leads_df[leads_df["category"] == "Hot"])
    warm_leads = len(leads_df[leads_df["category"] == "Warm"])
    cold_leads = len(leads_df[leads_df["category"] == "Cold"])
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", total_leads)
    with col2:
        st.metric("Hot Leads", hot_leads)
    with col3:
        st.metric("Warm Leads", warm_leads)
    with col4:
        st.metric("Cold Leads", cold_leads)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Leads by Category")
        category_counts = leads_df["category"].value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]
        fig = px.pie(category_counts, values="Count", names="Category", 
                    color="Category", color_discrete_map={"Hot":"red", "Warm":"orange", "Cold":"blue"})
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Leads by Source")
        source_counts = leads_df["source"].value_counts().reset_index()
        source_counts.columns = ["Source", "Count"]
        fig = px.bar(source_counts, x="Source", y="Count")
        st.plotly_chart(fig)
    
    # Recent leads
    st.subheader("Recent Leads")
    recent_leads = leads_df.sort_values("created_at", ascending=False).head(5)
    st.dataframe(recent_leads[["name", "company", "category", "score", "created_at"]])

# Leads page
elif page == "Leads":
    st.title("Lead Management")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.selectbox("Filter by Category", ["All", "Hot", "Warm", "Cold"])
    with col2:
        min_score = st.slider("Minimum Score", 0, 100, 0)
    
    # Apply filters
    filtered_df = leads_df
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["category"] == category_filter]
    if min_score > 0:
        filtered_df = filtered_df[filtered_df["score"] >= min_score]
    
    # Display leads table
    st.dataframe(filtered_df)
    
    # Lead actions
    if st.button("Export to CSV"):
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv,
            "leads.csv",
            "text/csv",
            key='download-csv'
        )

# Add Lead page
elif page == "Add Lead":
    st.title("Add New Lead")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *")
        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number")
        company = st.text_input("Company Name *")
    
    with col2:
        industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Manufacturing", "Retail", "Education", "Other"])
        company_size = st.selectbox("Company Size", ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"])
        source = st.selectbox("Lead Source", ["Website", "Social Media", "Referral", "Event", "Cold Call", "Other"])
        interest = st.text_area("Interest/Needs *")
    
    if st.button("Submit Lead"):
        if name and email and company and interest:
            # AI scoring logic (simplified)
            score = 0
            
            # Industry scoring
            if industry in ["Technology", "Finance", "Healthcare"]:
                score += 20
            else:
                score += 10
                
            # Company size scoring
            if company_size in ["201-500", "501-1000", "1000+"]:
                score += 30
            elif company_size in ["51-200"]:
                score += 20
            else:
                score += 10
                
            # Source scoring
            if source == "Referral":
                score += 25
            elif source == "Social Media":
                score += 15
            else:
                score += 10
                
            # Calculate category
            if score >= 70:
                category = "Hot"
            elif score >= 40:
                category = "Warm"
            else:
                category = "Cold"
                
            st.success(f"Lead added successfully! Score: {score}, Category: {category}")
            st.info("In a real implementation, this lead would be saved to Google Sheets")
        else:
            st.error("Please fill all required fields")

# Analytics page
elif page == "Analytics":
    st.title("Lead Analytics")
    
    # Time series analysis
    st.subheader("Lead Acquisition Trend")
    leads_df["created_at"] = pd.to_datetime(leads_df["created_at"])
    leads_by_date = leads_df.groupby(leads_df["created_at"].dt.date).size().reset_index()
    leads_by_date.columns = ["Date", "Count"]
    fig = px.line(leads_by_date, x="Date", y="Count")
    st.plotly_chart(fig)
    
    # Industry distribution
    st.subheader("Leads by Industry")
    industry_counts = leads_df["industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Count"]
    fig = px.bar(industry_counts, x="Industry", y="Count")
    st.plotly_chart(fig)
    
    # Score distribution
    st.subheader("Score Distribution")
    fig = px.histogram(leads_df, x="score", nbins=10)
    st.plotly_chart(fig)
    
    # Conversion funnel
    st.subheader("Conversion Funnel")
    funnel_data = [
        {"stage": "All Leads", "count": len(leads_df)},
        {"stage": "Hot Leads", "count": hot_leads},
        {"stage": "Contacted", "count": int(hot_leads * 0.8)},
        {"stage": "Meeting Scheduled", "count": int(hot_leads * 0.5)},
        {"stage": "Proposal Sent", "count": int(hot_leads * 0.3)},
        {"stage": "Closed Won", "count": int(hot_leads * 0.15)}
    ]
    funnel_df = pd.DataFrame(funnel_data)
    fig = px.funnel(funnel_df, x="count", y="stage")
    st.plotly_chart(fig)

# Settings page
elif page == "Settings":
    st.title("Settings")
    
    st.subheader("Lead Scoring Parameters")
    
    st.write("Industry Weights")
    tech_weight = st.slider("Technology", 0, 30, 20)
    finance_weight = st.slider("Finance", 0, 30, 20)
    healthcare_weight = st.slider("Healthcare", 0, 30, 20)
    
    st.write("Company Size Weights")
    enterprise_weight = st.slider("Enterprise (1000+)", 0, 30, 30)
    mid_weight = st.slider("Mid-size (51-500)", 0, 30, 20)
    small_weight = st.slider("Small (<50)", 0, 30, 10)
    
    st.write("Source Weights")
    referral_weight = st.slider("Referral", 0, 30, 25)
    social_weight = st.slider("Social Media", 0, 30, 15)
    website_weight = st.slider("Website", 0, 30, 10)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# Logout option
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()
