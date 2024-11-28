import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Deepash/Visualiser")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    # Read the uploaded file
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.write(data)

    # Select Columns for X and Y
    x_col = st.selectbox("Select X-axis column", data.columns)
    y_col = st.selectbox("Select Y-axis column", data.columns)

    # Data Selection Mode
    st.write("### Choose Data Selection Mode")
    selection_mode = st.radio(
        "Select how to filter data:",
        ("By Percentage", "By Row Range"),
        index=0
    )

    if selection_mode == "By Percentage":
        # Select Percentage of Data
        percentage = st.slider("Select percentage of data to display", 10, 100, 100, step=10)
        num_rows = int(len(data) * (percentage / 100))
        data_subset = data.head(num_rows)
        st.write(f"Displaying the first {percentage}% of the data ({num_rows} rows):")
        st.write(data_subset)

    elif selection_mode == "By Row Range":
        # Manual Row Range Selection
        start_row = st.number_input("Start Row (0-based index)", min_value=0, max_value=len(data)-1, value=0, step=1)
        end_row = st.number_input("End Row (exclusive, 0-based index)", min_value=1, max_value=len(data), value=len(data), step=1)

        if start_row >= end_row:
            st.error("End Row must be greater than Start Row.")
        else:
            data_subset = data.iloc[start_row:end_row]
            st.write(f"Displaying rows {start_row} to {end_row - 1} ({len(data_subset)} rows):")
            st.write(data_subset)

    # Plot Type
    plot_type = st.radio(
        "Select Plot Type",
        ("Line", "Bar", "Scatter")
    )

    # Plot Graph
    st.subheader("Graph:")
    try:
        fig, ax = plt.subplots()
        if plot_type == "Line":
            ax.plot(data_subset[x_col], data_subset[y_col], label=f"{y_col} vs {x_col}")
        elif plot_type == "Bar":
            ax.bar(data_subset[x_col], data_subset[y_col], label=f"{y_col} vs {x_col}")
        elif plot_type == "Scatter":
            ax.scatter(data_subset[x_col], data_subset[y_col], label=f"{y_col} vs {x_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.error("An error occurred while generating the graph. Please check the details below:")
        error_message = f"**Error Message:** {str(e)}"
        st.warning(error_message)
else:
    st.info("Please upload a CSV file to plot the graph.")
