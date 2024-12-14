import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io

st.set_page_config(
    page_title="My Cool App",
    page_icon="😂",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊Data Analysis Web App")
st.sidebar.image("logo/images.png", caption='Data Exploring App')
st.sidebar.header("Input Features")

tab1, tab2, tab3 = st.tabs(['EDA', "Data Cleaning", "Modelling"])
radio = st.sidebar.radio("Navigate through", ["EDA", "Data Cleaning", "Modelling"])

if radio == "EDA":
    st.sidebar.subheader("Provide Input for EDA")
    file = st.sidebar.file_uploader("Upload the CSV file", type = "CSV")
    info = st.sidebar.checkbox("Click me to see the Data Info")
    describe = st.sidebar.checkbox("Click to see the summary")


if "df" not in st.session_state:
    st.session_state.df = None

if radio == "EDA":
    if file is not None:
        df = pd.read_csv(file)
        if st.session_state.df is None:
            st.session_state.df = df.copy()





    if st.session_state.df is not None:
        with tab1:
            filt = st.checkbox("Apply Filters in the Data")
            if filt:
                st.session_state.filtered_df = st.session_state.df.copy()
                filt_cols  = st.multiselect("Select Columns to Filter",st.session_state.df.columns)
                if len(filt_cols)>0:
                    ncol = st.columns(len(filt_cols))

                    for i in range(len(ncol)):
                        with ncol[i]:
                            if st.session_state.df[filt_cols[i]].dtype in [int, float, "int64", "float64"]:
                                ran = st.slider(f"Range {filt_cols[i]}", min_value=st.session_state.df[filt_cols[i]].min(),
                                                max_value=st.session_state.df[filt_cols[i]].max(), value=(st.session_state.df[filt_cols[i]].min(),
                                                                                                          st.session_state.df[filt_cols[i]].max()))
                                st.session_state.filtered_df = st.session_state.filtered_df[(st.session_state.filtered_df[filt_cols[i]]>=ran[0]) & (st.session_state.filtered_df[filt_cols[i]] <= ran[1])]
                            elif st.session_state.df[filt_cols[i]].dtype == "object":
                                cat = st.multiselect(f"Category {filt_cols[i]}",st.session_state.df[filt_cols[i]].unique())
                                st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df[filt_cols[i]].isin(cat)]
                    st.markdown("**Filtered Data**")
                    st.write(st.session_state.filtered_df)
                    #filt_button = st.button("Apply this filter to original DataFrame")




            if filt:
                if st.button("👇Apply Filter to Original Data"):
                    st.session_state.df = st.session_state.filtered_df.copy()
                else:
                    st.session_state.df = df.copy()

            with st.expander("Original DataFrame"):
                st.write(st.session_state.df)

            if info:
                col1, col2 = st.columns(2)

                with col1:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")

                    st.info("Shape", icon="📌")
                    col3, col4 = st.columns(2)
                    with col3:
                        st.metric(label="No. Of Rows", value=f"{st.session_state.df.shape[0]}")
                    with col4:
                        st.metric(label="No. Of Columns", value=f"{st.session_state.df.shape[1]}")

                    # Checkbox to change data types
                    st.session_state.dtype_fl = st.checkbox("Change Data type")
                    if st.session_state.dtype_fl:
                        col3, col4 = st.columns(2)
                        with col3:
                            st.session_state.to_num = st.multiselect("Change to Numeric", st.session_state.df.columns)
                        with col4:
                            st.session_state.to_obj = st.multiselect("Change to Object", st.session_state.df.columns)
                    if st.button("Apply Changes"):
                        st.session_state.df[st.session_state.to_obj] = st.session_state.df[
                            st.session_state.to_obj].astype(str)
                        st.session_state.df[st.session_state.to_num] = st.session_state.df[st.session_state.to_num].apply(pd.to_numeric, errors='coerce')

                with col2:

                    buffer = io.StringIO()
                    st.session_state.df.info(buf=buffer)
                    info_str = buffer.getvalue()  # Get the output as a string

                    st.subheader("Data Info")
                    st.code(info_str, language="plaintext")


            if describe:
                with st.container():
                    st.header("Descriptive Statistics")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Numerical Features")
                        percent = st.text_input("Add Percentile if needed (comma separated)")
                        if percent == "":
                            st.write(st.session_state.df.describe())
                        else:
                            st.write(st.session_state.df.describe(percentiles=list(map(float, percent.split(",")))))

                    with col2:
                        st.subheader("Categorical Variable")
                        var = st.session_state.df.select_dtypes("object")
                        var_name = st.selectbox("Select particular Column to see", list(var.columns) + ["None"], index=len(var.columns))

                        if var_name == "None":
                            st.write(pd.DataFrame(var.nunique(), columns=["Unique Entries"]))
                        else:
                            fig, axes = plt.subplots(figsize=(6, 6))
                            sns.countplot(data=var, x=var_name, ax=axes, orient="h")
                            st.pyplot(fig)

            st.subheader("Univariate Analysis")
            chat1,chat2 = st.columns(2)
            with chat1:
                st.write("")
                st.empty()
                st.empty()
                var_plot = st.selectbox("Select the Variable name to Visualize", st.session_state.df.columns)


            with chat2:

                chart_type = st.selectbox("Select the type of Chart(count plot and pie chart for Categorical data and rest for numericals)",["Count Plot","Pie Chart","Histogram","Density Plot","Box-Plot","Line-Chart"])
            with chat1:
                if chart_type in ["Count Plot","Histogram","Box-Plot","Line-Chart"]:
                    hue = st.selectbox("Select Categorical Variable to add as Hue parameter",[None] + list(st.session_state.df.columns))


            fig,axes = plt.subplots()
            if chart_type =="Count Plot":
                sns.countplot(st.session_state.df,x=var_plot,ax=axes,hue = hue)
            elif chart_type=="Pie Chart":
                value_counts = st.session_state.df[var_plot].value_counts()
                axes.pie(value_counts, labels = value_counts.index,autopct='%1.1f%%')
            elif chart_type == "Histogram":
                sns.histplot(st.session_state.df,x=var_plot,ax=axes,hue = hue,multiple = "dodge")
            elif chart_type == "Density Plot":
                sns.distplot(st.session_state.df[var_plot],ax=axes)
            elif chart_type == "Box-Plot":
                sns.boxplot(st.session_state.df,x=var_plot,ax=axes,hue = hue)
            elif chart_type == "Line-Chart":
                sns.lineplot(st.session_state.df,y = var_plot,x = st.session_state.df.index, ax=axes,hue  = hue)
            axes.set_title(f'{chart_type} of {var_plot}')
            st.pyplot(fig)

            st.subheader("Multivariate Analysis")



elif radio == "Data Cleaning":
    st.sidebar.subheader("Provide Input for Data Cleaning")
else:
    st.sidebar.subheader("Provide Input for Modellings")
