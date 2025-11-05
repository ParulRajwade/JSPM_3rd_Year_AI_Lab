import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
from src.fetch_live_data_nasa import fetch_live_data
from src.predict_live import generate_forecast
from src.ga_optimization import run_ga_optimization
from src.tank_simulation import simulate_tank_levels

# Page configuration
st.set_page_config(
    page_title="💧 Smart Rainwater Harvesting",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling 
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .success-box {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💧 Smart Rainwater Harvesting Management System</h1>
    <p style="font-size: 1.2rem; margin: 0;">AI-Powered Forecast + Optimization + Simulation</p>
    <p style="font-size: 1rem; margin: 0.5rem 0 0 0;">Real-time NASA data • LSTM Forecasting • Genetic Algorithm Optimization</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    # RainFlow Logo
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="
            color: #0066cc;
            padding: 10px;
            border-radius: 15px;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            font-size: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        ">
            <div style="
                position: relative;
                width: 50px;
                height: 50px;
            ">
                <!-- Circular tank/droplet shape -->
                <div style="
                    width: 40px;
                    height: 40px;
                    border: 3px solid #0066cc;
                    border-radius: 50%;
                    border-top: none;
                    position: relative;
                "></div>
                <!-- House roof inside -->
                <div style="
                    position: absolute;
                    top: 8px;
                    left: 8px;
                    width: 24px;
                    height: 12px;
                    background: #0066cc;
                    clip-path: polygon(0% 100%, 50% 0%, 100% 100%);
                "></div>
                <!-- Water spout above -->
                <div style="
                    position: absolute;
                    top: -5px;
                    left: 18px;
                    width: 4px;
                    height: 8px;
                    background: #0066cc;
                    border-radius: 2px;
                "></div>
                <!-- Curved arrow -->
                <div style="
                    position: absolute;
                    top: -8px;
                    right: -5px;
                    width: 20px;
                    height: 20px;
                    border: 2px solid #0066cc;
                    border-radius: 50%;
                    border-left: none;
                    border-bottom: none;
                    transform: rotate(-45deg);
                "></div>
            </div>
            <span style="color: #0066cc;">RainFlow</span>
        </div>
        <p style="
            color: #666;
            font-size: 12px;
            margin: 0;
            font-style: italic;
        ">Smart Rainwater Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ System Configuration")
    st.markdown("Enter the details below :")
    st.markdown("---")
    
    # Location settings
    st.markdown("**📍 Location Settings**")
    lat = st.number_input("Latitude (°N)", value=18.54, min_value=-90.0, max_value=90.0, step=0.01, help="Enter your location's latitude")
    lon = st.number_input("Longitude (°E)", value=73.85, min_value=-180.0, max_value=180.0, step=0.01, help="Enter your location's longitude")
    
    st.markdown("---")
    st.markdown("**🏗️ Tank & Catchment Parameters**")
    
    # Tank parameters
    catchment_area = st.number_input(
        "Catchment Area (m²)", 
        value=100, 
        min_value=10, 
        max_value=10000,
        help="Total roof/catchment area for rainwater collection"
    )
    
    runoff_coefficient = st.slider(
        "Runoff Coefficient", 
        0.0, 1.0, 0.85, 0.01,
        help="Efficiency of rainwater collection (0.85 = 85% efficiency)"
    )
    
    tank_capacity = st.number_input(
        "Tank Capacity (liters)", 
        value=3000, 
        min_value=500, 
        max_value=100000,
        help="Total storage capacity of your tank"
    )
    
    initial_storage = st.number_input(
        "Initial Storage (liters)", 
        value=1500, 
        min_value=0, 
        max_value=tank_capacity,
        help="Current water level in tank"
    )
    
    st.markdown("---")
    st.markdown("**💧 Usage Constraints**")
    
    usage_min = st.number_input(
        "Daily Usage Min (liters)", 
        value=300, 
        min_value=50, 
        max_value=1000,
        help="Minimum daily water consumption"
    )
    
    usage_max = st.number_input(
        "Daily Usage Max (liters)", 
        value=800, 
        min_value=usage_min, 
        max_value=2000,
        help="Maximum daily water consumption"
    )
    
    st.markdown("---")
    
    # System status
    st.markdown("**📊 System Status**")
    if 'system_status' in st.session_state:
        if st.session_state.system_status == 'success':
            st.markdown('<div class="success-box">✅ System Ready</div>', unsafe_allow_html=True)
        elif st.session_state.system_status == 'error':
            st.markdown('<div class="info-box">❌ System Error</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">⏳ System Idle</div>', unsafe_allow_html=True)
    
# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🚀 Run Smart System")
    
    # Run button with enhanced styling
    if st.button("🚀 Launch Smart Analysis", use_container_width=True):
        try:
            # Initialize session state
            st.session_state.system_status = 'running'
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Fetch live data
            status_text.text("📡 Fetching live NASA rainfall data (45 days to ensure 30+ valid days)...")
            progress_bar.progress(20)
            
            with st.spinner("🌍 Connecting to NASA POWER API (fetching 45 days for LSTM model)..."):
                live_df = fetch_live_data(lat=lat, lon=lon, days_back=45)
            
            progress_bar.progress(40)
            status_text.text("🔮 Generating LSTM rainfall forecast...")
            
            # Step 2: Generate forecast
            with st.spinner("🤖 Running AI prediction model..."):
                forecast_df = generate_forecast(live_df)
            
            progress_bar.progress(60)
            status_text.text("⚙️ Running Genetic Algorithm optimization...")
            
            # Step 3: GA optimization
            with st.spinner("🧬 Optimizing water usage plan..."):
                optimized_df, merged_df = run_ga_optimization(
                    forecast_df,
                    catchment_area,
                    runoff_coefficient,
                    tank_capacity,
                    initial_storage,
                    usage_min,
                    usage_max
                )
            
            progress_bar.progress(80)
            status_text.text("💧 Simulating tank levels...")
            
            # Step 4: Tank simulation
            with st.spinner("📊 Calculating water balance..."):
                simulated_df = simulate_tank_levels(
                    merged_df=merged_df,
                    catchment_area_m2=catchment_area,
                    runoff_coefficient=runoff_coefficient,
                    tank_capacity_liters=tank_capacity,
                    initial_storage_liters=initial_storage
                )
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Success message
            st.success("🎉 Smart analysis completed successfully!")
            st.session_state.system_status = 'success'
            
            # Store results in session state
            st.session_state.forecast_df = forecast_df
            st.session_state.merged_df = merged_df
            st.session_state.simulated_df = simulated_df
            st.session_state.live_df = live_df
            
            # Save outputs
            os.makedirs("outputs", exist_ok=True)
            forecast_df.to_csv("outputs/predictions_next_7_days_on_NASA_data.csv", index=False)
            merged_df.to_csv("outputs/final_plan.csv", index=False)
            simulated_df.to_csv("outputs/tank_simulation_next_7_days.csv", index=False)
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.session_state.system_status = 'error'
            st.stop()

with col2:
    st.markdown("### 📍 Current Location")
    # Create a DataFrame for the map
    map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_df)
    
    st.markdown("### 📊 Quick Stats")
    if 'system_status' in st.session_state and st.session_state.system_status == 'success':
        # Calculate key metrics
        avg_rainfall = st.session_state.forecast_df['predicted_rainfall_mm'].mean()
        total_collection = (avg_rainfall * catchment_area * runoff_coefficient) / 1000  # m³
        
        st.metric("🌧️ Avg Rainfall", f"{avg_rainfall:.1f} mm/day")
        st.metric("💧 Daily Collection", f"{total_collection:.2f} m³/day")
        st.metric("🏗️ Tank Utilization", f"{(initial_storage/tank_capacity)*100:.1f}%")

# Display results if available
if 'system_status' in st.session_state and st.session_state.system_status == 'success':
    st.markdown("---")
    
    # Results section
    st.markdown("## 📊 Analysis Results")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🌧️ Rainfall Forecast", "⚙️ Usage Optimization", "💧 Tank Simulation", "📈 Summary"])
    
    with tab1:
        st.markdown("### 🌧️ Rainfall Forecast & Historical Data")
        
        # Create interactive plot with Plotly
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Historical vs Forecasted Rainfall', 'Forecast Details'),
            vertical_spacing=0.1
        )
        
        # Historical data (last 7 days)
        fig.add_trace(
            go.Scatter(
                x=st.session_state.live_df['date'],
                y=st.session_state.live_df['rainfall_mm'],
                mode='lines+markers',
                name='Historical (Last 7 days)',
                line=dict(color='blue', width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Forecast data
        fig.add_trace(
            go.Scatter(
                x=st.session_state.forecast_df['date'],
                y=st.session_state.forecast_df['predicted_rainfall_mm'],
                mode='lines+markers',
                name='Forecast (Next 7 days)',
                line=dict(color='red', width=3, dash='dash'),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Bar chart for forecast
        fig.add_trace(
            go.Bar(
                x=st.session_state.forecast_df['date'],
                y=st.session_state.forecast_df['predicted_rainfall_mm'],
                name='Daily Forecast',
                marker_color='lightcoral'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            title_text="🌧️ Rainfall Analysis Dashboard",
            showlegend=True,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Forecast Start", st.session_state.forecast_df['date'].min().strftime('%Y-%m-%d'))
        with col2:
            st.metric("📅 Forecast End", st.session_state.forecast_df['date'].max().strftime('%Y-%m-%d'))
        with col3:
            st.metric("🌧️ Total Predicted", f"{st.session_state.forecast_df['predicted_rainfall_mm'].sum():.1f} mm")
    
    with tab2:
        st.markdown("### ⚙️ Optimized Water Usage Plan")
        
        # Usage optimization chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=st.session_state.merged_df['date'],
            y=st.session_state.merged_df['optimized_usage_liters'],
            name='Optimized Usage',
            marker_color='lightgreen'
        ))
        
        fig.update_layout(
            title="💧 Daily Water Usage Optimization",
            xaxis_title="Date",
            yaxis_title="Water Usage (liters/day)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Usage statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💧 Avg Daily Usage", f"{st.session_state.merged_df['optimized_usage_liters'].mean():.0f} L")
        with col2:
            st.metric("💧 Total Usage", f"{st.session_state.merged_df['optimized_usage_liters'].sum():.0f} L")
        with col3:
            st.metric("⚖️ Usage Efficiency", f"{(st.session_state.merged_df['optimized_usage_liters'].mean()/usage_max)*100:.1f}%")
    
    with tab3:
        st.markdown("### 💧 Tank Storage Simulation")
        
        # Tank simulation chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=st.session_state.simulated_df['date'],
            y=st.session_state.simulated_df['storage_liters'],
            fill='tonexty',
            name='Tank Storage',
            line=dict(color='blue', width=3)
        ))
        
        # Add tank capacity line
        fig.add_hline(y=tank_capacity, line_dash="dash", line_color="red", 
                     annotation_text=f"Tank Capacity: {tank_capacity:,} L")
        
        fig.update_layout(
            title="💧 Tank Water Level Over Time",
            xaxis_title="Date",
            yaxis_title="Storage (liters)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Simulation statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💧 Min Storage", f"{st.session_state.simulated_df['storage_liters'].min():.0f} L")
        with col2:
            st.metric("💧 Max Storage", f"{st.session_state.simulated_df['storage_liters'].max():.0f} L")
        with col3:
            st.metric("⚠️ Overflow Days", f"{len(st.session_state.simulated_df[st.session_state.simulated_df['overflow_liters'] > 0])}")
    
    with tab4:
        st.markdown("### 📈 System Summary")
        
        # Key metrics in cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🌧️ Rainfall Collection</h3>
                <p style="font-size: 2rem; margin: 0;">{:.1f} m³</p>
                <p>Total potential collection</p>
            </div>
            """.format((st.session_state.forecast_df['predicted_rainfall_mm'].sum() * catchment_area * runoff_coefficient) / 1000), 
            unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <h3>💧 Water Efficiency</h3>
                <p style="font-size: 2rem; margin: 0;">{:.1f}%</p>
                <p>Collection efficiency</p>
            </div>
            """.format(runoff_coefficient * 100), 
            unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🏗️ Storage Utilization</h3>
                <p style="font-size: 2rem; margin: 0;">{:.1f}%</p>
                <p>Peak tank usage</p>
            </div>
            """.format((st.session_state.simulated_df['storage_liters'].max() / tank_capacity) * 100), 
            unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <h3>⚙️ Optimization Score</h3>
                <p style="font-size: 2rem; margin: 0;">{:.0f}</p>
                <p>GA fitness score</p>
            </div>
            """.format(1000),  # Placeholder - you can get this from GA
            unsafe_allow_html=True)
        
        # Download section
        st.markdown("### 📥 Download Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📊 Rainfall Forecast CSV",
                data=st.session_state.forecast_df.to_csv(index=False),
                file_name="rainfall_forecast.csv",
                mime="text/csv"
            )
        
        with col2:
            st.download_button(
                label="⚙️ Usage Plan CSV",
                data=st.session_state.merged_df.to_csv(index=False),
                file_name="usage_plan.csv",
                mime="text/csv"
            )
        
        with col3:
            st.download_button(
                label="💧 Tank Simulation CSV",
                data=st.session_state.simulated_df.to_csv(index=False),
                file_name="tank_simulation.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💧 Smart Rainwater Harvesting Management System | Powered by AI & NASA Data</p>
    <p>Built with Streamlit • LSTM • Genetic Algorithms • Real-time Optimization</p>
</div>
""", unsafe_allow_html=True)
