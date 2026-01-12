"""
Streamlit Dashboard for SIM Swap Detection System
Interactive web interface for viewing detection results

MVP Features:
- Built-in Excel datasets (no upload required)
- Optional Excel file upload
- Rule-based detection (NO ML)
- Report generation (Excel/CSV export)
- Forensic analysis display

Future Work (ML Integration):
- Machine learning model training can be added here
- Feature engineering pipeline
- Model evaluation metrics
- Hybrid rule-based + ML approach
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from data_ingestion import DataIngestion
from rule_engine import RuleEngine
from utils import format_alert_emoji
import config


# Page configuration
st.set_page_config(
    page_title="SIM Swap Detection System - MVP",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-high {
        background-color: #ffebee;
        border-left-color: #f44336;
    }
    .alert-medium {
        background-color: #fff3e0;
        border-left-color: #ff9800;
    }
    .alert-low {
        background-color: #e8f5e9;
        border-left-color: #4caf50;
    }
</style>
""", unsafe_allow_html=True)


def get_built_in_datasets():
    """Get list of built-in Excel datasets"""
    datasets_dir = os.path.join(os.path.dirname(__file__), 'datasets')
    if not os.path.exists(datasets_dir):
        return []

    datasets = []
    for file in os.listdir(datasets_dir):
        if file.endswith('.xlsx'):
            datasets.append({
                'name': file.replace('.xlsx', '').replace('dataset_', '').replace('_', ' ').title(),
                'filename': file,
                'path': os.path.join(datasets_dir, file)
            })
    return datasets


def generate_forensic_report(results, dataset_name):
    """Generate forensic report as DataFrame"""
    report_data = []

    for result in results:
        # Build triggered rules string
        triggered_rules_str = "; ".join([
            f"{rule['rule']}: {rule['reason']}"
            for rule in result['triggered_rules']
        ])

        report_data.append({
            'Detection_Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'User_ID': result['user_id'],
            'Risk_Score': result['risk_score'],
            'Alert_Level': result['alert_level'],
            'Alert_Severity': result['alert_emoji'] + ' ' + result['alert_level'],
            'Total_Rules_Triggered': result['total_rules_triggered'],
            'Triggered_Rules_Details': triggered_rules_str,
            'Dataset_Source': dataset_name,
            'Detection_Method': 'Rule-Based (No ML)',
            'Requires_Investigation': 'YES' if result['alert_level'] == 'HIGH' else 'REVIEW' if result['alert_level'] == 'MEDIUM' else 'NO'
        })

    return pd.DataFrame(report_data)


def main():
    """Main dashboard function - MVP with built-in datasets"""

    # Header
    st.markdown('<div class="main-header">🔒 SIM Swap Attack Detection System - MVP</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Rule-Based Detection Using User Behavior Analytics (No ML)</div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("📊 Control Panel")
    st.sidebar.markdown("---")

    # Data source selection
    st.sidebar.subheader("📁 Data Source")
    data_source = st.sidebar.radio(
        "Choose data source:",
        ["Built-in Datasets", "Upload Excel File"],
        help="Use built-in datasets for demo or upload your own Excel file"
    )

    # Add clear button for uploaded files
    if data_source == "Upload Excel File" and 'temp_file_path' in st.session_state:
        if st.sidebar.button("🗑️ Clear Uploaded File"):
            temp_path = st.session_state['temp_file_path']
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            del st.session_state['temp_file_path']
            del st.session_state['uploaded_filename']
            if 'results' in st.session_state:
                del st.session_state['results']
            if 'data_loaded' in st.session_state:
                del st.session_state['data_loaded']
            st.rerun()

    # Initialize components
    data_loader = DataIngestion()
    rule_engine = RuleEngine()

    selected_file_path = None
    dataset_name = None

    if data_source == "Built-in Datasets":
        # Get built-in datasets
        datasets = get_built_in_datasets()

        if not datasets:
            st.sidebar.error("❌ No built-in datasets found. Run data_generator.py first.")
            st.info("🔧 **Setup Required**: Run `python data_generator.py` to generate built-in datasets.")
            return

        # Dataset selection
        dataset_options = {ds['name']: ds for ds in datasets}
        selected_dataset_name = st.sidebar.selectbox(
            "Select built-in dataset:",
            options=list(dataset_options.keys()),
            help="Choose from pre-generated test datasets"
        )

        selected_dataset = dataset_options[selected_dataset_name]
        selected_file_path = selected_dataset['path']
        dataset_name = selected_dataset['filename']

        st.sidebar.info(f"📊 **Dataset**: {selected_dataset_name}")

    else:  # Upload Excel File
        uploaded_file = st.sidebar.file_uploader(
            "Upload Excel file (.xlsx)",
            type=['xlsx', 'xls'],
            help="Upload Excel file with user activity data"
        )

        if uploaded_file is not None:
            # Use a consistent temp file path based on session
            import tempfile
            if 'temp_file_path' not in st.session_state:
                # Create temp file
                temp_dir = tempfile.gettempdir()
                temp_file_path = os.path.join(temp_dir, f"simswap_{uploaded_file.name}")

                # Save uploaded file
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.session_state['temp_file_path'] = temp_file_path
                st.session_state['uploaded_filename'] = uploaded_file.name

            selected_file_path = st.session_state['temp_file_path']
            dataset_name = st.session_state['uploaded_filename']
            st.sidebar.success(f"✅ File uploaded: {dataset_name}")
        else:
            # Clear temp file if user removed upload
            if 'temp_file_path' in st.session_state:
                temp_path = st.session_state['temp_file_path']
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                del st.session_state['temp_file_path']
                del st.session_state['uploaded_filename']

            st.sidebar.warning("⚠️ Please upload an Excel file to continue")
            st.info("📤 **Upload Required**: Select an Excel file (.xlsx) containing user activity data.")
            return

    # Load and process data
    if selected_file_path:
        try:
            # Load data
            with st.spinner("Loading data..."):
                data_loader.load_data(selected_file_path)
                data_loader.validate_data()

            # Get summary
            summary = data_loader.get_summary()

            # Display summary in sidebar
            st.sidebar.success(f"✅ Loaded {summary['total_records']} records")
            
            if 'legitimate_count' in summary:
                st.sidebar.metric("Legitimate Users", summary['legitimate_count'])
                st.sidebar.metric("Suspicious Users", summary['suspicious_count'])
            
            st.sidebar.markdown("---")
            
            # Process data
            st.sidebar.subheader("🔍 Detection")
            if st.sidebar.button("Run Detection", type="primary"):
                with st.spinner("Analyzing user behavior..."):
                    # Get user records
                    user_records = data_loader.get_user_records()
                    
                    # Evaluate each user
                    results = []
                    for user_data in user_records:
                        result = rule_engine.evaluate_user(user_data)
                        results.append(result)
                    
                    # Store results in session state
                    st.session_state['results'] = results
                    st.session_state['data_loaded'] = True
                
                st.sidebar.success("✅ Detection complete!")
            
            # Display results
            if 'results' in st.session_state and st.session_state.get('data_loaded', False):
                display_results(st.session_state['results'], dataset_name)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            st.error(f"Details: {traceback.format_exc()}")


def display_results(results, dataset_name):
    """Display detection results with report generation"""

    st.header("🎯 Detection Results")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    total_users = len(results)
    high_risk = len([r for r in results if r['alert_level'] == 'HIGH'])
    medium_risk = len([r for r in results if r['alert_level'] == 'MEDIUM'])
    low_risk = len([r for r in results if r['alert_level'] == 'LOW'])

    with col1:
        st.metric("Total Users", total_users)
    with col2:
        st.metric("🚨 High Risk", high_risk)
    with col3:
        st.metric("⚠️ Medium Risk", medium_risk)
    with col4:
        st.metric("✅ Low Risk", low_risk)

    st.markdown("---")

    # Report Generation Section
    st.subheader("📄 Forensic Report Generation")
    col1, col2 = st.columns(2)

    with col1:
        report_format = st.selectbox(
            "Report Format",
            options=["Excel (.xlsx)", "CSV (.csv)"],
            help="Choose format for forensic report export"
        )

    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("📥 Generate & Download Report", type="primary"):
            # Generate forensic report
            report_df = generate_forensic_report(results, dataset_name)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            if report_format == "Excel (.xlsx)":
                # Export as Excel
                output_file = f"forensic_report_{timestamp}.xlsx"
                report_df.to_excel(output_file, index=False, engine='openpyxl')

                with open(output_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download Excel Report",
                        data=f,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                # Clean up
                if os.path.exists(output_file):
                    os.remove(output_file)

            else:  # CSV
                # Export as CSV
                csv_data = report_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV Report",
                    data=csv_data,
                    file_name=f"forensic_report_{timestamp}.csv",
                    mime="text/csv"
                )

            st.success(f"✅ Report generated with {len(report_df)} records")

    st.markdown("---")

    # Filter options
    st.subheader("🔍 Filter Results")
    col1, col2 = st.columns(2)

    with col1:
        alert_filter = st.multiselect(
            "Alert Level",
            options=['HIGH', 'MEDIUM', 'LOW'],
            default=['HIGH', 'MEDIUM', 'LOW']
        )

    with col2:
        min_risk_score = st.slider(
            "Minimum Risk Score",
            min_value=0,
            max_value=100,
            value=0
        )

    # Filter results
    filtered_results = [
        r for r in results
        if r['alert_level'] in alert_filter and r['risk_score'] >= min_risk_score
    ]

    st.markdown(f"**Showing {len(filtered_results)} of {total_users} users**")

    # Display results table
    st.subheader("📊 User Risk Assessment")

    # Create DataFrame for display
    display_data = []
    for result in filtered_results:
        triggered_rules_text = "\n".join([
            f"• {rule['rule']}: {rule['reason']}"
            for rule in result['triggered_rules']
        ])

        display_data.append({
            'User ID': result['user_id'],
            'Risk Score': result['risk_score'],
            'Alert Level': f"{result['alert_emoji']} {result['alert_level']}",
            'Rules Triggered': result['total_rules_triggered'],
            'Details': triggered_rules_text if triggered_rules_text else 'No rules triggered'
        })

    df_display = pd.DataFrame(display_data)

    # Display as table
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )

    # Detailed view
    st.markdown("---")
    st.subheader("🔎 Detailed Analysis")

    # Select user for detailed view
    user_ids = [r['user_id'] for r in filtered_results]

    if user_ids:
        selected_user = st.selectbox("Select user for detailed analysis", user_ids)

        # Find selected user result
        user_result = next((r for r in filtered_results if r['user_id'] == selected_user), None)

        if user_result:
            # Display user details
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("User ID", user_result['user_id'])
            with col2:
                st.metric("Risk Score", user_result['risk_score'])
            with col3:
                alert_class = f"alert-{user_result['alert_level'].lower()}"
                st.markdown(
                    f'<div class="metric-card {alert_class}">'
                    f'<h3>{user_result["alert_emoji"]} {user_result["alert_level"]} RISK</h3>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # Display triggered rules
            st.markdown("### 📋 Triggered Rules")

            if user_result['triggered_rules']:
                for rule in user_result['triggered_rules']:
                    with st.expander(f"🔴 {rule['rule'].replace('_', ' ').title()} (Weight: {rule['weight']})"):
                        st.write(f"**Reason:** {rule['reason']}")
                        st.write(f"**Risk Weight:** {rule['weight']} points")
            else:
                st.success("✅ No suspicious activity detected for this user")

    # Download results
    st.markdown("---")
    st.subheader("💾 Export Results")

    # Create export DataFrame
    export_data = []
    for result in results:
        triggered_rules_list = [rule['rule'] for rule in result['triggered_rules']]
        reasons_list = [rule['reason'] for rule in result['triggered_rules']]

        export_data.append({
            'user_id': result['user_id'],
            'risk_score': result['risk_score'],
            'alert_level': result['alert_level'],
            'total_rules_triggered': result['total_rules_triggered'],
            'triggered_rules': ', '.join(triggered_rules_list),
            'reasons': ' | '.join(reasons_list)
        })

    df_export = pd.DataFrame(export_data)

    # Convert to CSV
    csv = df_export.to_csv(index=False)

    st.download_button(
        label="📥 Download Results (CSV)",
        data=csv,
        file_name="simswap_detection_results.csv",
        mime="text/csv"
    )


if __name__ == '__main__':
    main()
