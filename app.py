import streamlit as st
from PIL import Image

from predict import predict_image
from utils.google_maps import get_maps_link
from utils.geolocation import reverse_geocode, is_valid_coordinate
from utils.email_sender import send_report_email
from utils.database import init_db, add_report, get_all_reports
from utils.file_utils import save_uploaded_image
from utils.report_generator import generate_excel_report, generate_pdf_report
from utils.helper import format_confidence, format_timestamp
from utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Road Damage Detection", page_icon="🛣️", layout="centered")

init_db()  # safe to call every run, only creates the table if missing

st.markdown("## Road damage detection")
st.caption("EfficientNet classifier · 7 classes")
st.divider()

tab_report, tab_history = st.tabs(["📤 New Report", "📋 Report History"])

# ============================================================
# TAB 1 -- Upload, predict, locate, and report
# ============================================================
with tab_report:
    uploaded_file = st.file_uploader(
        "Upload a road image", type=["jpg", "jpeg", "png"], help="JPG, JPEG or PNG"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded image", use_container_width=True)

        result = predict_image(image)
        all_probs = result["all_probs"]

        with col2:
            st.success(f"**{result['class']}**")
            st.caption(f"{format_confidence(result['confidence'])} confidence")

        st.markdown("**Class probabilities**")
        for class_name, prob in sorted(all_probs.items(), key=lambda x: -x[1]):
            st.progress(prob, text=f"{class_name} — {prob * 100:.1f}%")

        st.divider()
        st.markdown("**📍 Location of the issue**")
        st.caption("Enter coordinates manually (right-click a spot on Google Maps to get lat, lon).")

        loc_col1, loc_col2 = st.columns(2)
        with loc_col1:
            lat = st.number_input("Latitude", value=28.6139, format="%.6f")
        with loc_col2:
            lon = st.number_input("Longitude", value=77.2090, format="%.6f")

        address = ""
        if is_valid_coordinate(lat, lon):
            address = reverse_geocode(lat, lon)
            st.caption(f"📌 {address}")

        maps_link = get_maps_link(lat, lon)
        st.map({"lat": [lat], "lon": [lon]}, zoom=14)
        st.markdown(f"[Open in Google Maps]({maps_link})")

        st.divider()
        report_col1, report_col2 = st.columns(2)

        with report_col1:
            send_email_now = st.button("📨 Report to authority", use_container_width=True, type="primary")

        with report_col2:
            generate_docs_now = st.button("📄 Generate PDF + Excel", use_container_width=True)

        if send_email_now:
            saved_image_path = save_uploaded_image(image)

            with open(saved_image_path, "rb") as f:
                image_bytes = f.read()

            success, message = send_report_email(
                predicted_class=result["class"],
                confidence=result["confidence"],
                lat=lat, lon=lon, maps_link=maps_link,
                image_bytes=image_bytes,
            )

            add_report(
                predicted_class=result["class"], confidence=result["confidence"],
                lat=lat, lon=lon, address=address,
                image_path=saved_image_path, emailed=success,
            )

            st.success(message) if success else st.warning(message)

        if generate_docs_now:
            saved_image_path = save_uploaded_image(image)
            timestamp = format_timestamp()

            excel_path = generate_excel_report(
                result["class"], result["confidence"], lat, lon, address, timestamp
            )
            pdf_path = generate_pdf_report(
                result["class"], result["confidence"], lat, lon, address,
                image_path=saved_image_path, created_at=timestamp,
            )

            add_report(
                predicted_class=result["class"], confidence=result["confidence"],
                lat=lat, lon=lon, address=address,
                image_path=saved_image_path, emailed=False,
            )

            st.success("Reports generated!")
            with open(excel_path, "rb") as f:
                st.download_button("⬇️ Download Excel report", f, file_name="report.xlsx")
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF report", f, file_name="report.pdf")
    else:
        st.info("Upload an image to get a prediction.")

# ============================================================
# TAB 2 -- Report history
# ============================================================
with tab_history:
    reports = get_all_reports()

    if not reports:
        st.info("No reports yet. Submit one from the 'New Report' tab.")
    else:
        st.caption(f"{len(reports)} report(s) logged")
        for r in reports:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{r['predicted_class']}** — {r['confidence'] * 100:.1f}% confidence")
                    location_text = r["address"] or f"{r['latitude']}, {r['longitude']}"
                    st.caption(f"📍 {location_text}")
                    st.caption(f"🕒 {r['created_at']}")
                with c2:
                    st.markdown("✅ Emailed" if r["emailed"] else "⚠️ Not emailed")