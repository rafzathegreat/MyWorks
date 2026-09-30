import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import io

# ---------------------------------------------------------
# 1. Page Configuration & Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="Team AI & Digital Readiness Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .metric-container {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 14px;
        color: #94a3b8;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Hardcoded Fallback Dataset (Cleaned from your uploaded file)
# ---------------------------------------------------------
FALLBACK_DATA = """Name|Position & Grade|Agency|Years in Service|Role|Staff Supervised|Digital Maturity|AI Readiness|Personal AI Conf|Data Readiness|Cyber Maturity|Change Readiness|Current AI Usage|Top Learning Priorities
Anas Bin Safian|Head of mechanical|Ministry of youth|16|Head of Division|1-10|3.1|2.2|1.0|1.1|1.2|3.4|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Anisah Binti Ting|Vocational training|Ministry of youth|20|Head of Division|1-10|3.4|3.0|2.1|2.0|2.4|3.4|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Arieff Abdullah Bi|Administrative ar|Ministry of digital|5|Senior Assistant|1-10|3.4|2.5|3.4|3.1|3.9|3.2|Gemini, ChatGPT|Agentic AI, Responsible AI, AI Governance
Artiesa Binti Arris|Information techr|Ministry of defend|19|Head of Division|11-30|3.0|3.0|3.0|3.0|3.0|3.0|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Astrahuda Kama|Assistant director|Ministry of higher|25|Manager|1-10|2.9|1.8|1.7|3.3|4.0|3.2|Gemini, ChatGPT|Responsible AI, AI Governance, Leadership
Chong Chai Yun|Assistant secreta|Ministry of wome|13|Assistant Secreta|1-10|3.4|3.8|4.0|4.1|4.8|4.2|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Faizura Haneem|Principal assistar|Ministry of econo|21|Manager|11-30|3.2|2.4|3.1|2.1|2.0|3.2|Gemini, Noteboo|Gemini Enterprise, NotebookLM, Google Workspace AI
Fariz Ubaidullah|Head of digital tra|Ministry of nation|22|Head of Unit|1-10|3.7|3.0|3.3|4.0|4.0|4.0|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Ibrahim Bin Abdu|Principal assistar|Ministry of digital|22|Principal Assistar|1-10|3.1|2.6|2.1|2.0|3.3|2.6|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Joanne Koo Yoke|Senior assistant|Ministry of investi|13|Senior Assistant|None|2.8|2.6|2.7|2.9|3.7|3.4|Gemini, ChatGPT|Digital Transformation, Agentic AI, Responsible AI
Mohamad Khairo|Science officer|Ministry of scienc|14|Senior Assistant|None|4.1|3.0|4.0|3.0|4.0|3.8|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Mohammad Azfa|Deputy undersec|Ministry of works|25|Deputy Director|1-10|2.6|1.4|2.8|2.2|2.8|2.6|Gemini, ChatGPT|Gemini Enterprise, Google Workspace Al, Al Productivity
Muhamad Hishar|Senior assistant|Ministry of tourisr|10|Penolong Setiaus|1-10|4.0|2.1|1.5|1.9|1.8|3.6|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Muhammad Irsya|Senior assistant|Ministry of humar|20|Deputy Director|1-10|3.5|2.5|4.0|3.0|3.7|3.2|Gemini, ChatGPT|Digital Transformation, Agentic AI, Responsible AI
Noorzaiti Ashikin|Information techr|Ministry of humar|19|Head of IT Unit|1-10|3.0|3.0|1.5|3.0|3.4|3.3|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Norhayati Ahmad|Principal assistar|Ministry of scienc|20|Head of Section|1-10|4.1|3.1|4.0|4.2|4.7|3.8|Gemini, ChatGPT|Gemini Enterprise, Deep Research, Al Productivity
Nory Afzan Binti|IT officer / senior|Ministry of financ|19|Manager|1-10|3.1|2.0|2.5|2.7|1.4|3.4|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Nur Munirah Bt A|Training officer|Ministry of youth|16|Manager|1-10|2.9|2.0|1.6|2.6|3.9|3.0|Gemini, ChatGPT|Deep Research, Al Productivity, Digital Transformation
Nurul Hidayah Bi|Senior assistant|Ministry of transp|16|Assistant Directo|1-10|3.6|1.2|3.4|2.4|3.9|2.4|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Siti Khadijah Yaa|Assistant director|Ministry of foreigi|4|Secretary Gener|1-10|3.1|3.3|3.1|2.5|3.7|2.4|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Tang Chun Huan|Senior assistant|Ministry of health|17|Manager|1-10|2.6|1.7|1.9|1.8|2.9|2.6|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI
Umi Syuhairah B|Principal assistar|Ministry of planta|22|Manager|1-10|3.3|2.1|2.2|2.4|2.4|3.4|Gemini, ChatGPT|Gemini Enterprise, NotebookLM, Google Workspace AI"""

# ---------------------------------------------------------
# 3. Data Ingestion (Local + Google Sheet Link configuration)
# ---------------------------------------------------------
@st.cache_data
def load_data(url=None):
    try:
        if url:
            # Direct CSV export parse from Google Sheets
            return pd.read_csv(url)
        else:
            return pd.read_csv(io.StringIO(FALLBACK_DATA), sep="|")
    except Exception as e:
        st.warning(f"Unable to read live Google Sheet: {e}. Loading cached profile data instead.")
        return pd.read_csv(io.StringIO(FALLBACK_DATA), sep="|")

# Sidebar Configuration for the Google Sheet URL
st.sidebar.markdown("## ⚙️ Data Source Connection")
sheet_id = st.sidebar.text_input(
    "Google Sheet ID (Optional)",
    placeholder="e.g., 1BxiMVs0XRA5nFMdKvDn_rDPLf_N_GXLw"
)

if sheet_id:
    # Formulate Google Sheets CSV Export Link
    SHEET_URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df_raw = load_data(SHEET_URL)
else:
    df_raw = load_data()

# Ensure consistent datatypes
df_raw['Years in Service'] = pd.to_numeric(df_raw['Years in Service'], errors='coerce')
readiness_dims = ['Digital Maturity', 'AI Readiness', 'Data Readiness', 'Cyber Maturity', 'Change Readiness']
for col in readiness_dims + ['Personal AI Conf']:
    if col in df_raw.columns:
        df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

# ---------------------------------------------------------
# 4. Interactive Sidebar Filters
# ---------------------------------------------------------
st.sidebar.markdown("## 🔍 Dashboard Filters")

# Agency Multi-Select
agencies = sorted(df_raw['Agency'].dropna().unique())
selected_agencies = st.sidebar.multiselect(
    "Select Agency / Ministry",
    options=agencies,
    default=agencies
)

# Years in Service Range Slider
min_years = int(df_raw['Years in Service'].min())
max_years = int(df_raw['Years in Service'].max())
selected_years = st.sidebar.slider(
    "Years in Service Range",
    min_value=min_years,
    max_value=max_years,
    value=(min_years, max_years)
)

# Role Multi-Select
roles = sorted(df_raw['Role'].dropna().unique())
selected_roles = st.sidebar.multiselect(
    "Select Position / Role",
    options=roles,
    default=roles
)

# Apply filter masks dynamically
df_filtered = df_raw[
    (df_raw['Agency'].isin(selected_agencies)) &
    (df_raw['Years in Service'].between(selected_years[0], selected_years[1])) &
    (df_raw['Role'].isin(selected_roles))
]

# ---------------------------------------------------------
# 5. UI Layout - Title & Metrics Section
# ---------------------------------------------------------
st.title("🛡️ Public Sector AI & Digital Readiness Dashboard")
st.markdown("Monitor and analyze AI literacy, cybersecurity maturity, and change agility across key ministries.")
st.markdown("---")

if df_filtered.empty:
    st.error("No data matches the selected filters. Please adjust your selections in the sidebar.")
else:
    # Top-Level KPI Dashboard Cards
    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">TOTAL PERSONNEL SELECTED</div>
                <div class="metric-value">{len(df_filtered)}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_cols[1]:
        avg_ai = df_filtered['AI Readiness'].mean()
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">AVERAGE AI READINESS</div>
                <div class="metric-value">{avg_ai:.2f} / 5.00</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_cols[2]:
        avg_dig = df_filtered['Digital Maturity'].mean()
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">AVERAGE DIGITAL MATURITY</div>
                <div class="metric-value">{avg_dig:.2f} / 5.00</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_cols[3]:
        avg_cyber = df_filtered['Cyber Maturity'].mean()
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">AVERAGE CYBER MATURITY</div>
                <div class="metric-value">{avg_cyber:.2f} / 5.00</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------------------------------------------------
    # 6. Charts & Visualizations
    # ---------------------------------------------------------
    tab1, tab2 = st.tabs(["📊 Performance Visualizations", "🧠 Capabilities & Learning Priorities"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Agency Multi-Metric Profiles")
            
            # Group scores by Agency for comparative profiling
            agency_grouped = df_filtered.groupby('Agency')[readiness_dims].mean().reset_index()
            df_melted = agency_grouped.melt(id_vars='Agency', value_vars=readiness_dims, 
                                            var_name='Maturity Dimension', value_name='Average Score')
            
            fig_bar = px.bar(
                df_melted,
                x='Agency',
                y='Average Score',
                color='Maturity Dimension',
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Plotly,
                template="plotly_dark",
                labels={'Agency': 'Ministry/Agency', 'Average Score': 'Average Competency Score'}
            )
            fig_bar.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=50, b=50)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("AI Readiness vs. Cyber Maturity Matrix")
            
            # Dynamic Scatter Plot
            fig_scatter = px.scatter(
                df_filtered,
                x='AI Readiness',
                y='Cyber Maturity',
                size='Years in Service',
                color='Agency',
                hover_name='Name',
                hover_data={'Role': True, 'Years in Service': True},
                template="plotly_dark",
                labels={'AI Readiness': 'AI Readiness (1-5)', 'Cyber Maturity': 'Cyber Maturity (1-5)'}
            )
            fig_scatter.update_layout(
                xaxis=dict(range=[0.5, 5.5]),
                yaxis=dict(range=[0.5, 5.5]),
                margin=dict(t=50, b=50)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    with tab2:
        col3, col4 = st.columns([1.5, 1])
        
        with col3:
            st.subheader("Top Learning Priorities Demand")
            
            # Aggregate and list learning demands
            priorities_list = []
            for priorities_str in df_filtered['Top Learning Priorities'].dropna():
                priorities_list.extend([p.strip() for p in priorities_str.split(',') if p.strip()])
                
            priority_counts = Counter(priorities_list)
            df_prio = pd.DataFrame(priority_counts.items(), columns=['Priority Topic', 'Mentions']).sort_values(by='Mentions', ascending=True)
            
            fig_prio = px.bar(
                df_prio,
                x='Mentions',
                y='Priority Topic',
                orientation='h',
                template="plotly_dark",
                color='Mentions',
                color_continuous_scale=px.colors.sequential.Bluyl
            )
            fig_prio.update_layout(coloraxis_showscale=False, margin=dict(t=30, b=30))
            st.plotly_chart(fig_prio, use_container_width=True)

        with col4:
            st.subheader("Radar Capability Profile (Average Selected)")
            
            # Polar radar plot of aggregated average competencies
            radar_vals = [df_filtered[dim].mean() for dim in readiness_dims]
            # Close the radar profile loop
            radar_vals_closed = radar_vals + [radar_vals[0]]
            dims_closed = readiness_dims + [readiness_dims[0]]
            
            fig_radar = go.Figure(
                data=go.Scatterpolar(
                    r=radar_vals_closed,
                    theta=dims_closed,
                    fill='toself',
                    fillcolor='rgba(56, 189, 248, 0.2)',
                    line=dict(color='#38bdf8', width=2)
                )
            )
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 5])
                ),
                showlegend=False,
                template="plotly_dark",
                margin=dict(t=40, b=40, l=40, r=40)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    # ---------------------------------------------------------
    # 7. Interactive Raw Data Explorer
    # ---------------------------------------------------------
    st.markdown("---")
    with st.expander("🔍 Interactive Data Explorer & Search"):
        # Custom search bar for searching names/roles instantly
        search_query = st.text_input("Quick Search Name or Role", "")
        
        df_display = df_filtered.copy()
        if search_query:
            df_display = df_display[
                df_display['Name'].str.contains(search_query, case=False, na=False) |
                df_display['Role'].str.contains(search_query, case=False, na=False)
            ]
            
        st.dataframe(
            df_display[['Name', 'Agency', 'Role', 'Years in Service'] + readiness_dims + ['Top Learning Priorities']],
            use_container_width=True,
            hide_index=True
        )
