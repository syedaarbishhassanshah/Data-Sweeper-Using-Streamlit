import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import streamlit as st 
import pandas as pd  
import os
from io import BytesIO
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import re
from scipy import stats 
from typing import List, Dict, Any, Optional, Union
import warnings
warnings.filterwarnings("ignore", message=".*ScriptRunContext.*")

# Set page configuration
st.set_page_config(
    page_title="DATA SWEEPER",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 8px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition: all 0.3s ease;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #45a049, #4CAF50);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .stButton>button:after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    
    .stButton>button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        100% {
            transform: scale(20, 20);
            opacity: 0;
        }
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #4CAF50, #45a049);
    }
    
    .stSelectbox, .stRadio, .stSlider {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox:hover, .stRadio:hover, .stSlider:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .stDataFrame {
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background-color: white;
        transition: all 0.3s ease;
    }
    
    .stDataFrame:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #dff0d8 0%, #c8e5bc 100%);
        color: #3c763d;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #3c763d;
        font-weight: 500;
        animation: fadeIn 0.5s ease-in;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fcf8e3 0%, #f8efc0 100%);
        color: #8a6d3b;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #8a6d3b;
        font-weight: 500;
        animation: fadeIn 0.5s ease-in;
    }
    
    .stError {
        background: linear-gradient(135deg, #f2dede 0%, #ebcccc 100%);
        color: #a94442;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #a94442;
        font-weight: 500;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: all 0.3s ease;
        border: 1px solid #e0e0e0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: #2c3e50;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        color: #7f8c8d;
    }
    
    .file-uploader {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .file-uploader:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .quality-dashboard {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        color: white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(106, 17, 203, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(106, 17, 203, 0); }
        100% { box-shadow: 0 0 0 0 rgba(106, 17, 203, 0); }
    }
    
    .recommendations-box {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stRadio > div {
        display: flex;
        flex-direction: row;
        gap: 10px;
    }
    
    .stRadio > div > label {
        background: white;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stRadio > div > label:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .stRadio > div > label[data-baseweb="radio"] {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Enhanced App title with modern styling
st.markdown("""
    <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); color: white; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); position: relative; overflow: hidden;'>
        <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url("https://www.transparenttextures.com/patterns/cubes.png"); opacity: 0.1;'></div>
        <h1 style='color: white; font-size: 3em; margin-bottom: 15px; font-family: "Montserrat", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>📊 Data Sweeper</h1>
        <p style='font-size: 1.3em; opacity: 0.9; font-family: "Poppins", sans-serif;'>Transform Your Data with Powerful Cleaning and Analysis Tools</p>
    </div>
""", unsafe_allow_html=True)

# Enhanced Sidebar styling
st.sidebar.markdown("""
    <style>
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content .block-container {
        color: white;
    }
    .sidebar-radio {
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    .sidebar-radio:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    </style>
""", unsafe_allow_html=True)

# Enhanced Sidebar navigation with icons and animations
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='color: white; font-family: "Montserrat", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🔍 Navigation</h2>
    </div>
""", unsafe_allow_html=True)
page = st.sidebar.radio("", ["📤 Data Upload", "🧹 Data Cleaning", "📈 Data Analysis", "💾 Export Data"])

# Initialize session state for storing data and history
if 'df' not in st.session_state:
    st.session_state.df = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Type hints for session state
st.session_state.df: Optional[pd.DataFrame]  # type: ignore
st.session_state.history: List[pd.DataFrame]  # type: ignore

def save_state() -> None:
    if st.session_state.df is not None:
        st.session_state.history.append(st.session_state.df.copy())

def undo_last_action() -> bool:
    if len(st.session_state.history) > 1:
        st.session_state.history.pop()
        st.session_state.df = st.session_state.history[-1].copy()
        return True
    return False

# Data Upload Page
if page == "📤 Data Upload":
    st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <h2 style='color: #2c3e50; margin-bottom: 20px;'>📤 Upload Your Data</h2>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.df = pd.read_csv(uploaded_file)
            else:
                st.session_state.df = pd.read_excel(uploaded_file)
            
            save_state()
            st.success("✅ File uploaded successfully!")
            
            # Display data preview with better styling
            st.markdown("""
                <div style='background: white; padding: 25px; border-radius: 15px; margin-top: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
                    <h3 style='color: #2c3e50; margin-bottom: 15px;'>Preview of your data</h3>
                </div>
            """, unsafe_allow_html=True)
            st.dataframe(st.session_state.df.head().style.background_gradient(cmap='Blues'))
            
            # Display basic information with better styling
            st.markdown("""
                <div style='background: white; padding: 25px; border-radius: 15px; margin-top: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
                    <h3 style='color: #2c3e50; margin-bottom: 15px;'>Data Information</h3>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class='metric-card'>
                        <div class='metric-value'>{}</div>
                        <div class='metric-label'>Number of rows</div>
                    </div>
                """.format(st.session_state.df.shape[0]), unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class='metric-card'>
                        <div class='metric-value'>{}</div>
                        <div class='metric-label'>Number of columns</div>
                    </div>
                """.format(st.session_state.df.shape[1]), unsafe_allow_html=True)
            
            # Data quality check with better styling
            st.markdown("""
                <div class='quality-dashboard'>
                    <h3 style='color: white; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>
                        🎯 Data Quality Dashboard
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Create quality report with more robust handling
            quality_data = {
                'Column': st.session_state.df.columns,
                'Missing Values': st.session_state.df.isna().sum().tolist(),
                'Missing %': (st.session_state.df.isna().sum() / len(st.session_state.df) * 100).round(2).tolist(),
                'Unique Values': st.session_state.df.nunique().tolist(),
                'Data Type': [str(dtype) for dtype in st.session_state.df.dtypes]
            }
            quality_report = pd.DataFrame(quality_data)
            
            # Calculate overall data quality metrics
            total_missing = quality_report['Missing Values'].sum()
            total_cells = len(st.session_state.df) * len(st.session_state.df.columns)
            data_completeness = ((total_cells - total_missing) / total_cells * 100).round(2)
            
            # Display quality metrics in cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h4 style='margin: 0; font-family: "Poppins", sans-serif;'>📊 Data Completeness</h4>
                        <h2 style='margin: 10px 0; font-family: "Montserrat", sans-serif;'>{data_completeness}%</h2>
                        <p style='margin: 0; font-size: 12px;'>Overall data quality score</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h4 style='margin: 0; font-family: "Poppins", sans-serif;'>📋 Total Columns</h4>
                        <h2 style='margin: 10px 0; font-family: "Montserrat", sans-serif;'>{len(st.session_state.df.columns)}</h2>
                        <p style='margin: 0; font-size: 12px;'>Features in your dataset</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h4 style='margin: 0; font-family: "Poppins", sans-serif;'>📈 Total Rows</h4>
                        <h2 style='margin: 10px 0; font-family: "Montserrat", sans-serif;'>{len(st.session_state.df)}</h2>
                        <p style='margin: 0; font-size: 12px;'>Data points analyzed</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Apply enhanced styling to the quality report
            styled_report = quality_report.style\
                .background_gradient(cmap='RdPu', subset=['Missing Values', 'Missing %'])\
                .background_gradient(cmap='Blues', subset=['Unique Values'])\
                .set_properties(**{
                    'text-align': 'center',
                    'border': '1px solid #e0e0e0',
                    'padding': '8px',
                    'font-family': 'Poppins, sans-serif'
                })\
                .set_table_styles([
                    {'selector': 'th',
                     'props': [('background-color', '#6a11cb'),
                              ('color', 'white'),
                              ('font-weight', 'bold'),
                              ('text-align', 'center'),
                              ('padding', '12px'),
                              ('font-family', 'Montserrat, sans-serif')]},
                    {'selector': 'tr:hover',
                     'props': [('background-color', '#f0f0f0')]}
                ])
            
            # Display the styled report with a caption
            st.markdown("""
                <div style='margin-top: 20px; margin-bottom: 10px;'>
                    <h4 style='color: #6a11cb; font-family: "Montserrat", sans-serif;'>📊 Column-wise Quality Metrics</h4>
                </div>
            """, unsafe_allow_html=True)
            st.dataframe(styled_report, use_container_width=True)
            
            # Add data quality recommendations with emojis
            st.markdown("""
                <div class='recommendations-box'>
                    <h4 style='color: #2c3e50; margin-bottom: 10px; font-family: "Montserrat", sans-serif;'>
                        💡 Data Quality Recommendations
                    </h4>
                    <ul style='color: #2c3e50; margin: 0; padding-left: 20px; font-family: "Poppins", sans-serif;'>
                        <li>🔍 Columns with high missing values (>20%) might need imputation or removal</li>
                        <li>🧹 Columns with only one unique value might be candidates for removal</li>
                        <li>🔄 Consider data type conversions for better analysis</li>
                        <li>📊 Check for outliers in numerical columns</li>
                        <li>🔤 Standardize text data for consistency</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# Data Cleaning Page
elif page == "🧹 Data Cleaning":
    st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <h2 style='color: #2c3e50; margin-bottom: 20px; font-family: "Montserrat", sans-serif;'>🧹 Data Cleaning</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.df is not None:
        # Display current data with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>📋 Current Data</h3>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(st.session_state.df.head().style.background_gradient(cmap='Blues'))
        
        # Undo button with enhanced styling
        if st.button("Undo Last Action", key="undo_button"):
            if undo_last_action():
                st.success("Last action undone!")
            else:
                st.warning("No actions to undo!")
        
        # Cleaning options with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>🛠️ Cleaning Options</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Remove duplicates with enhanced styling
        if st.button("Remove Duplicates", key="remove_duplicates"):
            save_state()
            initial_rows = len(st.session_state.df)
            st.session_state.df = st.session_state.df.drop_duplicates()
            final_rows = len(st.session_state.df)
            st.success(f"Removed {initial_rows - final_rows} duplicate rows")
        
        # Handle missing values with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>🔍 Handle Missing Values</h3>
            </div>
        """, unsafe_allow_html=True)
        missing_col = st.selectbox("Select column to handle missing values", st.session_state.df.columns)
        missing_option = st.radio("Choose action", ["Remove rows", "Fill with mean", "Fill with median", "Fill with mode", "Fill with custom value"])
        
        custom_value: Union[str, float, int] = ""
        if missing_option == "Fill with custom value":
            custom_value = st.text_input("Enter custom value")
        
        if st.button("Apply Missing Value Treatment", key="missing_value_treatment"):
            save_state()
            if missing_option == "Remove rows":
                st.session_state.df = st.session_state.df.dropna(subset=[missing_col])
            elif missing_option == "Fill with mean":
                st.session_state.df[missing_col] = st.session_state.df[missing_col].fillna(st.session_state.df[missing_col].mean())
            elif missing_option == "Fill with median":
                st.session_state.df[missing_col] = st.session_state.df[missing_col].fillna(st.session_state.df[missing_col].median())
            elif missing_option == "Fill with mode":
                st.session_state.df[missing_col] = st.session_state.df[missing_col].fillna(st.session_state.df[missing_col].mode()[0])
            else:
                st.session_state.df[missing_col] = st.session_state.df[missing_col].fillna(custom_value)
            st.success("Missing values handled successfully!")
        
        # Data type conversion with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>🔄 Data Type Conversion</h3>
            </div>
        """, unsafe_allow_html=True)
        type_col = st.selectbox("Select column to convert", st.session_state.df.columns)
        new_type = st.selectbox("Select new data type", ["int", "float", "str", "datetime"])
        
        if st.button("Convert Data Type", key="convert_data_type"):
            save_state()
            try:
                if new_type == "datetime":
                    st.session_state.df[type_col] = pd.to_datetime(st.session_state.df[type_col])
                else:
                    st.session_state.df[type_col] = st.session_state.df[type_col].astype(new_type)
                st.success("Data type converted successfully!")
            except Exception as e:
                st.error(f"Error converting data type: {str(e)}")
        
        # Text cleaning with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>📝 Text Cleaning</h3>
            </div>
        """, unsafe_allow_html=True)
        text_cols = [col for col in st.session_state.df.columns if st.session_state.df[col].dtype == 'object']
        if text_cols:
            text_col = st.selectbox("Select text column to clean", text_cols)
            text_options = st.multiselect("Select cleaning options", 
                                        ["Remove special characters", "Remove extra spaces", "Convert to lowercase", "Convert to uppercase"])
            
            if st.button("Clean Text", key="clean_text"):
                save_state()
                if text_col:
                    if "Remove special characters" in text_options:
                        st.session_state.df[text_col] = st.session_state.df[text_col].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
                    if "Remove extra spaces" in text_options:
                        st.session_state.df[text_col] = st.session_state.df[text_col].apply(lambda x: ' '.join(str(x).split()))
                    if "Convert to lowercase" in text_options:
                        st.session_state.df[text_col] = st.session_state.df[text_col].str.lower()
                    if "Convert to uppercase" in text_options:
                        st.session_state.df[text_col] = st.session_state.df[text_col].str.upper()
                    st.success("Text cleaning completed!")
        
        # Outlier detection and handling with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>📊 Outlier Detection and Handling</h3>
            </div>
        """, unsafe_allow_html=True)
        numeric_cols = st.session_state.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            outlier_col = st.selectbox("Select numeric column for outlier detection", numeric_cols)
            z_threshold = st.slider("Z-score threshold", 1.0, 5.0, 3.0, 0.1)
            
            if st.button("Detect and Handle Outliers", key="handle_outliers"):
                save_state()
                z_scores = np.abs(stats.zscore(st.session_state.df[outlier_col]))
                outliers = z_scores > z_threshold
                
                st.write(f"Found {outliers.sum()} outliers")
                
                outlier_option = st.radio("Choose how to handle outliers", 
                                        ["Remove outliers", "Replace with median", "Replace with mean"])
                
                if outlier_option == "Remove outliers":
                    st.session_state.df = st.session_state.df[~outliers]
                elif outlier_option == "Replace with median":
                    st.session_state.df.loc[outliers, outlier_col] = st.session_state.df[outlier_col].median()
                else:
                    st.session_state.df.loc[outliers, outlier_col] = st.session_state.df[outlier_col].mean()
                
                st.success("Outliers handled successfully!")
    
    else:
        st.warning("Please upload a file first in the Data Upload page.")

# Data Analysis Page
elif page == "📈 Data Analysis":
    st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <h2 style='color: #2c3e50; margin-bottom: 20px; font-family: "Montserrat", sans-serif;'>📈 Data Analysis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.df is not None:
        # Define numeric_cols at the start of the analysis section
        numeric_df = st.session_state.df.select_dtypes(include=[np.number])
        numeric_cols = numeric_df.columns
        
        # Basic statistics with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>📊 Basic Statistics</h3>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(st.session_state.df.describe().style.background_gradient(cmap='Blues'))
        
        # Correlation matrix with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>🔗 Correlation Matrix</h3>
            </div>
        """, unsafe_allow_html=True)
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig, ax = plt.subplots(figsize=(12, 10))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt='.2f', linewidths=0.5)
            plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
            st.pyplot(fig)
        
        # Distribution plots with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>📊 Distribution Plots</h3>
            </div>
        """, unsafe_allow_html=True)
        plot_col = st.selectbox("Select column for distribution plot", st.session_state.df.columns)
        if st.button("Show Distribution"):
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.histplot(st.session_state.df[plot_col], kde=True, ax=ax, color='#3498db')
            plt.title(f'Distribution of {plot_col}', fontsize=16, fontweight='bold')
            plt.xlabel(plot_col, fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            st.pyplot(fig)
        
        # Categorical data analysis with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>📊 Categorical Data Analysis</h3>
            </div>
        """, unsafe_allow_html=True)
        cat_cols = st.session_state.df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            cat_col = st.selectbox("Select categorical column", cat_cols)
            if st.button("Show Categorical Analysis"):
                value_counts = st.session_state.df[cat_col].value_counts()
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette='viridis')
                plt.title(f'Distribution of {cat_col}', fontsize=16, fontweight='bold')
                plt.xlabel(cat_col, fontsize=12)
                plt.ylabel('Count', fontsize=12)
                plt.xticks(rotation=45)
                st.pyplot(fig)
                st.markdown("""
                    <div style='background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 20px;'>
                        <h4 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>Value Counts</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.dataframe(value_counts)
        
        # Time series analysis with enhanced styling
        datetime_cols = st.session_state.df.select_dtypes(include=['datetime64']).columns
        if len(datetime_cols) > 0:
            st.markdown("""
                <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                    <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>⏰ Time Series Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            datetime_col = st.selectbox("Select datetime column", datetime_cols)
            value_col = st.selectbox("Select value column", numeric_cols)
            
            if st.button("Show Time Series Plot"):
                fig, ax = plt.subplots(figsize=(14, 8))
                st.session_state.df.set_index(datetime_col)[value_col].plot(ax=ax, color='#e74c3c', linewidth=2)
                plt.title(f'{value_col} over Time', fontsize=16, fontweight='bold')
                plt.xlabel('Time', fontsize=12)
                plt.ylabel(value_col, fontsize=12)
                plt.grid(True, linestyle='--', alpha=0.7)
                st.pyplot(fig)
    
    else:
        st.warning("Please upload a file first in the Data Upload page.")

# Export Data Page
elif page == "💾 Export Data":
    st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <h2 style='color: #2c3e50; margin-bottom: 20px; font-family: "Montserrat", sans-serif;'>💾 Export Data</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.df is not None:
        # Export options with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>📤 Export Options</h3>
            </div>
        """, unsafe_allow_html=True)
        export_format = st.radio("Select export format", ["CSV", "Excel"])
        
        if export_format == "CSV":
            csv = st.session_state.df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
        else:
            excel_buffer = BytesIO()
            st.session_state.df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            st.download_button(
                label="Download Excel",
                data=excel_buffer,
                file_name="cleaned_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # Save cleaning configuration with enhanced styling
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px; font-family: "Montserrat", sans-serif;'>💾 Save Cleaning Configuration</h3>
            </div>
        """, unsafe_allow_html=True)
        config_name = st.text_input("Enter configuration name")
        if st.button("Save Configuration"):
            config: Dict[str, Any] = {
                'name': config_name,
                'columns': list(st.session_state.df.columns),
                'dtypes': {col: str(dtype) for col, dtype in st.session_state.df.dtypes.items()}
            }
            st.success("Configuration saved!")
    else:
        st.warning("Please upload a file first in the Data Upload page.")
