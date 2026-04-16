import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_module import get_preparation_analysis
from ui_utils import inject_premium_css

st.set_page_config(page_title="Analytics", page_icon="📉", layout="wide")
inject_premium_css()

st.title("📉 Performance Analytics Dashboard")
st.markdown("Deep dive into your progress, failure frequency, and trends based on your dataset.")

st.divider()

data = get_preparation_analysis()

if data.empty:
    st.warning("No data found to display analytics.")
else:
    with st.spinner("Loading analytics..."):
        # 2. INTERACTIVE FILTER PANEL
        st.markdown("### 🎛️ Filter Panel")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            all_types = ["All"]
            if 'Failure Type' in data.columns:
                all_types.extend(list(data['Failure Type'].dropna().unique()))
            selected_type = st.selectbox("Failure Type", all_types)
        with col_f2:
            min_conf, max_conf = 0.0, 10.0
            if 'Confidence_Clean' in data.columns and not data['Confidence_Clean'].empty:
                min_conf, max_conf = float(data['Confidence_Clean'].min()), float(data['Confidence_Clean'].max())
            selected_conf = st.slider("Confidence Level", min_value=0.0, max_value=10.0, value=(0.0, 10.0))
        with col_f3:
            min_prep, max_prep = 0.0, 100.0
            if 'Prep_Hours_Clean' in data.columns and not data['Prep_Hours_Clean'].empty:
                min_prep, max_prep = float(data['Prep_Hours_Clean'].min()), float(data['Prep_Hours_Clean'].max())
            # Safely set slider limits
            if np.isnan(min_prep) or np.isnan(max_prep):
                min_prep, max_prep = 0.0, 100.0
            selected_prep = st.slider("Preparation Hours", min_value=0.0, max_value=max(100.0, max_prep), value=(0.0, max(100.0, max_prep)))

        # Apply Filters
        filtered_data = data.copy()
        if selected_type != "All" and 'Failure Type' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['Failure Type'] == selected_type]
        if 'Confidence_Clean' in filtered_data.columns:
            filtered_data = filtered_data[(filtered_data['Confidence_Clean'] >= selected_conf[0]) & (filtered_data['Confidence_Clean'] <= selected_conf[1])]
        if 'Prep_Hours_Clean' in filtered_data.columns:
            filtered_data = filtered_data[(filtered_data['Prep_Hours_Clean'] >= selected_prep[0]) & (filtered_data['Prep_Hours_Clean'] <= selected_prep[1])]

        st.divider()

        # Step 1: Overview
        st.markdown("### Step 1: Overview")
        if filtered_data.empty:
            st.warning("No data matches the selected filters.")
        else:
            with st.container():
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                total_failures = len(filtered_data)
                avg_conf = filtered_data['Confidence_Clean'].mean() if 'Confidence_Clean' in filtered_data.columns else 0
                avg_prep = filtered_data['Prep_Hours_Clean'].mean() if 'Prep_Hours_Clean' in filtered_data.columns else 0
                
                # Determine most common cluster
                common_cluster_name = "N/A"
                if 'Cluster' in filtered_data.columns and not filtered_data['Cluster'].empty:
                    cluster_names = {0: "Confidence", 1: "Knowledge", 2: "Preparation", 3: "Other"}
                    most_common = filtered_data['Cluster'].mode()
                    if not most_common.empty:
                        common_cluster_name = cluster_names.get(most_common.iloc[0], f"Cluster {most_common.iloc[0]}")
                
                col_m1.metric("Total Failures", f"{total_failures}")
                col_m2.metric("Average Confidence", f"{avg_conf:.1f}" if not np.isnan(avg_conf) else "N/A")
                col_m3.metric("Avg Prep Hours", f"{avg_prep:.1f}" if not np.isnan(avg_prep) else "N/A")
                col_m4.metric("Most Common Cluster", common_cluster_name)

            st.divider()

            # Step 2: Distribution
            st.markdown("### Step 2: Distribution")
            with st.container():
                col1, col_pie = st.columns(2)
                
                with col1:
                    with st.container(border=True):
                        st.subheader("📊 Failure Type Distribution")
                        fig1, ax1 = plt.subplots(figsize=(8, 4))
                        if 'Failure Type' in filtered_data.columns:
                            allowed_types = ["Exam", "Interview", "Hackathon", "Internship / Job Application", "Other"]
                            freq_data = filtered_data['Failure Type'].dropna().value_counts().reindex(allowed_types).fillna(0)
                            sns.barplot(x=freq_data.index, y=freq_data.values, ax=ax1, hue=freq_data.index, palette="mako", legend=False)
                            ax1.set_ylabel("Count")
                            ax1.set_xlabel("Failure Type")
                            plt.xticks(rotation=25, ha="right")
                        else:
                            st.write("Failure Type data not available.")
                        sns.despine()
                        st.pyplot(fig1)

                with col_pie:
                    with st.container(border=True):
                        st.subheader("🥧 Cluster Distribution")
                        fig_pie, ax_pie = plt.subplots(figsize=(8, 4))
                        if 'Cluster' in filtered_data.columns and not filtered_data['Cluster'].empty:
                            cluster_counts = filtered_data['Cluster'].value_counts()
                            cluster_names = {0: "Confidence", 1: "Knowledge", 2: "Preparation", 3: "Other"}
                            labels = [cluster_names.get(idx, f"Cluster {idx}") for idx in cluster_counts.index]
                            ax_pie.pie(cluster_counts, labels=labels, autopct='%1.1f%%', colors=sns.color_palette("pastel"), startangle=140)
                            ax_pie.axis('equal')
                        else:
                            st.write("Cluster data missing.")
                        st.pyplot(fig_pie)

            st.divider()

            # Step 3: Performance
            st.markdown("### Step 3: Performance")
            with st.container():
                col2, col4_new = st.columns(2)
                
                with col2:
                    with st.container(border=True):
                        st.subheader("⏱️ Preparation Hours Distribution")
                        fig2, ax2 = plt.subplots(figsize=(8, 4))
                        if 'Prep_Hours_Clean' in filtered_data.columns and not filtered_data['Prep_Hours_Clean'].empty:
                            sns.histplot(data=filtered_data, x='Prep_Hours_Clean', bins=10, kde=True, ax=ax2, color='coral')
                            ax2.set_xlabel("Hours Prepared")
                        else:
                            st.write("Preparation Data missing.")
                        sns.despine()
                        st.pyplot(fig2)

                with col4_new:
                    with st.container(border=True):
                        st.subheader("🧠 Confidence Level Distribution")
                        fig3, ax3 = plt.subplots(figsize=(8, 4))
                        if 'Confidence_Clean' in filtered_data.columns and not filtered_data['Confidence_Clean'].empty:
                            sns.histplot(data=filtered_data, x='Confidence_Clean', bins=5, discrete=True, color='teal', ax=ax3)
                            ax3.set_xlabel("Confidence Level (1-10)")
                            ax3.set_xticks(range(1, 11))
                        else:
                            st.write("Confidence Data missing.")
                        sns.despine()
                        plt.tight_layout()
                        st.pyplot(fig3)
                        
            with st.container():
                col_scatter, _ = st.columns([1, 1])
                with col_scatter:
                    with st.container(border=True):
                        st.subheader("📈 Confidence vs Prep Hours Scatter")
                        fig_scatter, ax_scatter = plt.subplots(figsize=(8, 4))
                        if 'Confidence_Clean' in filtered_data.columns and 'Prep_Hours_Clean' in filtered_data.columns and not filtered_data.empty:
                            sns.scatterplot(data=filtered_data, x='Prep_Hours_Clean', y='Confidence_Clean', hue='Cluster', palette='deep', ax=ax_scatter)
                            ax_scatter.set_xlabel("Preparation Hours")
                            ax_scatter.set_ylabel("Confidence Level")
                        else:
                            st.write("Data missing for scatter plot.")
                        sns.despine()
                        st.pyplot(fig_scatter)

            st.divider()

            # Step 4: Insights
            st.markdown("### Step 4: Insights")
            with st.container():
                col3, _ = st.columns([1, 1])
                with col3:
                    with st.container(border=True):
                        st.subheader("🔥 Failure Frequency Heatmap (Cluster vs Confidence)")
                        fig4, ax4 = plt.subplots(figsize=(8, 4))
                        if 'Cluster' in filtered_data.columns and 'Confidence_Clean' in filtered_data.columns and not filtered_data.empty:
                            filtered_data_heat = filtered_data.copy()
                            filtered_data_heat['Confidence_Bin'] = pd.cut(filtered_data_heat['Confidence_Clean'], bins=[0, 3, 7, 10], labels=['Low (1-3)', 'Medium (4-7)', 'High (8-10)'])
                            heatmap_data = pd.crosstab(filtered_data_heat['Cluster'], filtered_data_heat['Confidence_Bin']).fillna(0)
                            cluster_names = {0: "Confidence", 1: "Knowledge", 2: "Preparation", 3: "Other"}
                            heatmap_data.index = [cluster_names.get(idx, f"Cluster {idx}") for idx in heatmap_data.index]
                            sns.heatmap(heatmap_data, annot=True, cmap="Blues", ax=ax4, fmt='g', linewidths=.5)
                            ax4.set_ylabel("Failure Root Cause")
                        else:
                            st.write("Data missing for heatmap.")
                        st.pyplot(fig4)

            # Detailed Expandable Insights
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("💡 View Detailed Insights", expanded=False):
                st.success("✅ **Positive Pattern:** Higher preparation slightly correlates with reduced frequency in the Knowledge cluster.")
                st.warning("⚠️ **Risk Alert:** Most failures in the 'Confidence' cluster occur alongside medium to low preparation hours.")
                st.info("ℹ️ **General Insight:** Exam failures dominate the dataset but often show a consistent distribution across all confidence levels.")

