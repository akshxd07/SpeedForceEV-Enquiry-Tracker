import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="SpeedForce EV - Enquiry Tracker", layout="wide")
st.title("SpeedForce EV Vehicle Enquiry Tracker")

st.sidebar.header("Enquiry Summary")
try:
    summary_res = requests.get(f"{API_URL}/summary")
    if summary_res.status_code == 200:
        summary_data = summary_res.json()
        
        for status, count in summary_data.items():
            st.sidebar.metric(label=status, value=count)
except Exception as e:
    st.sidebar.warning("Could not fetch summary metrics.")

tab1, tab2 = st.tabs(["Add New Enquiry", "View & Manage Enquiries"])

with tab1:
    st.subheader("Customer Enquiry Entry")
    with st.form("enquiry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name*")
            phone = st.text_input("Mobile Number (10 digits)*", help="Valid Indian mobile number starting with 6-9")
            city = st.text_input("City*")
        with col2:
            vehicle_model = st.selectbox(
                "Scooter Model*",
                ["Joy e-bike Monster", "Joy e-bike Wolf", "Joy e-bike Gen Nxt", "Joy e-bike Glob"]
            )
            notes = st.text_area("Notes / Requirements")

        submitted = st.form_submit_button("Submit Enquiry")

        if submitted:
            payload = {
                "customer_name": customer_name,
                "phone": phone,
                "city": city,
                "vehicle_model": vehicle_model,
                "notes": notes
            }
            res = requests.post(f"{API_URL}/enquiries", json=payload)
            if res.status_code == 201:
                st.success("Enquiry logged successfully!")
                st.rerun()
            else:
                error_msg = res.json().get("detail", "Error submitting form")
                if isinstance(error_msg, list):
                    error_msg = error_msg[0].get("msg", "Validation error")
                st.error(f"Failed to submit: {error_msg}")

with tab2:
    st.subheader("Enquiries Registry")
    
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "New", "Contacted", "Test Ride Done", "Purchased", "Lost"]
        )
    with f_col2:
        city_filter = st.text_input("Filter by City")

    
    params = {}
    if status_filter != "All":
        params["status"] = status_filter
    if city_filter.strip():
        params["city"] = city_filter.strip()

    res = requests.get(f"{API_URL}/enquiries", params=params)

    if res.status_code == 200:
        data = res.json()
        if data:
            df = pd.DataFrame(data)
            
            
            st.dataframe(df[["id", "customer_name", "phone", "city", "vehicle_model", "status", "created_date", "notes"]], use_container_width=True)

            
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Filtered List as CSV",
                data=csv_data,
                file_name="speedforce_enquiries.csv",
                mime="text/csv"
            )

            st.divider()
            st.subheader("Update Status or Delete Record")
            
            u_col1, u_col2, u_col3 = st.columns([1, 1, 1])
            with u_col1:
                selected_id = st.selectbox("Select Enquiry ID", df["id"].tolist())
            with u_col2:
                new_status = st.selectbox("New Status", ["New", "Contacted", "Test Ride Done", "Purchased", "Lost"])
            with u_col3:
                st.write("") 
                if st.button("Update Status"):
                    patch_res = requests.patch(f"{API_URL}/enquiries/{selected_id}/status", json={"status": new_status})
                    if patch_res.status_code == 200:
                        st.success(f"ID {selected_id} updated to {new_status}")
                        st.rerun()
                    else:
                        st.error("Failed to update status")

            if st.button("Delete Selected Enquiry", type="secondary"):
                del_res = requests.delete(f"{API_URL}/enquiries/{selected_id}")
                if del_res.status_code == 204:
                    st.success(f"Enquiry {selected_id} deleted successfully")
                    st.rerun()
        else:
            st.info("No enquiries found matching criteria.")