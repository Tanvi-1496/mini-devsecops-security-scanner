
import streamlit as st
from pathlib import Path
from scanner import scan_directory, calculate_score
import tempfile
import zipfile


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="DevSecOps Security Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM STYLING
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    .score-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        background-color: #ffffff;
    }

    .score-number {
        font-size: 2.2rem;
        font-weight: 700;
    }

    .status-pass {
        color: #16a34a;
        font-weight: 700;
    }

    .status-warning {
        color: #ca8a04;
        font-weight: 700;
    }

    .status-fail {
        color: #dc2626;
        font-weight: 700;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🛡️ Mini DevSecOps Security Scanner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Scan projects for common security, configuration and file-hygiene risks.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🔍 Security Scanner")

st.sidebar.write(
    "Choose how you want to scan a project."
)

scan_mode = st.sidebar.radio(
    "Scan Source",
    [
        "🧪 Sample Project",
        "📦 Upload Project ZIP"
    ]
)


uploaded_file = None

if scan_mode == "📦 Upload Project ZIP":

    uploaded_file = st.sidebar.file_uploader(
        "Upload Project ZIP",
        type=["zip"],
        help="Compress your project folder into a ZIP file and upload it."
    )

    scan_button = st.sidebar.button(
        "🔍 Scan Uploaded Project",
        type="primary",
        use_container_width=True
    )

else:

    scan_button = st.sidebar.button(
        "🧪 Scan Sample Project",
        type="primary",
        use_container_width=True
    )


# ==================================================
# INITIAL SCREEN
# ==================================================

if not scan_button:

    st.info(
        "👈 Select a scan source from the sidebar and start a security scan."
    )

    st.markdown(
        '<div class="section-title">🔐 Security Checks</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🔑 Secrets")

        st.write(
            "Detects hardcoded passwords, API keys, tokens and secrets."
        )

    with col2:

        st.markdown("### 📁 File Hygiene")

        st.write(
            "Checks `.env` files, private keys and unusually large files."
        )

    with col3:

        st.markdown("### ⚠️ Suspicious Files")

        st.write(
            "Detects potentially risky executable and archive files."
        )

    st.divider()

    st.markdown(
        '<div class="section-title">⚙️ How It Works</div>',
        unsafe_allow_html=True
    )

    step1, step2, step3, step4, step5 = st.columns(5)

    with step1:
        st.markdown("**1️⃣ Upload**")
        st.caption("Provide a project ZIP")

    with step2:
        st.markdown("**2️⃣ Extract**")
        st.caption("Project is extracted")

    with step3:
        st.markdown("**3️⃣ Scan**")
        st.caption("Security checks run")

    with step4:
        st.markdown("**4️⃣ Score**")
        st.caption("Risk score calculated")

    with step5:
        st.markdown("**5️⃣ Report**")
        st.caption("Findings displayed")

    st.divider()

    st.markdown(
        '<div class="section-title">🧰 Technology Stack</div>',
        unsafe_allow_html=True
    )

    tech1, tech2, tech3, tech4 = st.columns(4)

    with tech1:
        st.markdown("**Python**")
        st.caption("Scanning engine")

    with tech2:
        st.markdown("**Streamlit**")
        st.caption("Web dashboard")

    with tech3:
        st.markdown("**Git & GitHub**")
        st.caption("Version control")

    with tech4:
        st.markdown("**DevSecOps**")
        st.caption("Security workflow")


# ==================================================
# SAMPLE PROJECT SCAN
# ==================================================

if scan_mode == "🧪 Sample Project" and scan_button:

    sample_directory = Path(__file__).parent / "sample-project"

    if not sample_directory.exists():

        st.error(
            "❌ Sample project folder was not found."
        )

        st.stop()

    with st.spinner("🔍 Scanning sample project..."):

        try:

            results = scan_directory(sample_directory)

            score, status = calculate_score(results)

        except Exception as error:

            st.error(
                f"❌ Scan failed: {error}"
            )

            st.stop()

    project_name = "sample-project"


# ==================================================
# UPLOADED PROJECT SCAN
# ==================================================

elif scan_mode == "📦 Upload Project ZIP" and scan_button:

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload a project ZIP file first."
        )

        st.stop()

    project_name = uploaded_file.name

    with tempfile.TemporaryDirectory() as temp_directory:

        zip_path = Path(temp_directory) / uploaded_file.name

        with open(zip_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        extract_path = Path(temp_directory) / "project"

        extract_path.mkdir()

        # ------------------------------------------
        # Extract ZIP
        # ------------------------------------------

        try:

            with zipfile.ZipFile(zip_path, "r") as zip_ref:

                # Prevent ZIP path traversal attacks
                for member in zip_ref.infolist():

                    target_path = (
                        extract_path / member.filename
                    ).resolve()

                    if not str(target_path).startswith(
                        str(extract_path.resolve())
                    ):

                        st.error(
                            "❌ Unsafe ZIP file detected. "
                            "Extraction was blocked."
                        )

                        st.stop()

                zip_ref.extractall(extract_path)

        except zipfile.BadZipFile:

            st.error(
                "❌ Invalid ZIP file. Please upload a valid project ZIP."
            )

            st.stop()

        # ------------------------------------------
        # Handle root project folder
        # ------------------------------------------

        extracted_items = list(extract_path.iterdir())

        if (
            len(extracted_items) == 1
            and extracted_items[0].is_dir()
        ):

            target_directory = extracted_items[0]

        else:

            target_directory = extract_path

        # ------------------------------------------
        # Scan
        # ------------------------------------------

        with st.spinner(
            "🔍 Scanning uploaded project..."
        ):

            try:

                results = scan_directory(target_directory)

                score, status = calculate_score(results)

            except Exception as error:

                st.error(
                    f"❌ Scan failed: {error}"
                )

                st.stop()


# ==================================================
# DISPLAY RESULTS
# ==================================================

if scan_button and (
    scan_mode == "🧪 Sample Project"
    or uploaded_file is not None
):

    st.success(
        "✅ Security scan completed successfully."
    )

    st.divider()

    # ==================================================
    # PROJECT INFORMATION
    # ==================================================

    st.markdown(
        '<div class="section-title">📦 Project Information</div>',
        unsafe_allow_html=True
    )

    info1, info2 = st.columns(2)

    with info1:

        st.write("**Project:**")

        st.code(project_name)

    with info2:

        st.write("**Scanner:**")

        st.code("Mini DevSecOps Security Scanner")

    st.divider()

    # ==================================================
    # FINDINGS COUNT
    # ==================================================

    total_findings = (
        len(results["private_keys"])
        + len(results["hardcoded_secrets"])
        + len(results["large_files"])
        + len(results["suspicious_files"])
    )

    if results["env_file_detected"]:
        total_findings += 1

    if not results["gitignore_present"]:
        total_findings += 1

    # ==================================================
    # SECURITY OVERVIEW
    # ==================================================

    st.markdown(
        '<div class="section-title">📊 Security Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Security Score",
            f"{score}/100"
        )

    with col2:

        st.metric(
            "Final Status",
            status
        )

    with col3:

        st.metric(
            "Issues Detected",
            total_findings
        )

    # ==================================================
    # SCORE PROGRESS
    # ==================================================

    st.write("### 📈 Security Score")

    st.progress(score / 100)

    if status == "PASS":

        st.success(
            "🟢 PASS: The project meets the defined security checks."
        )

    elif status == "WARNING":

        st.warning(
            "🟡 WARNING: Some security issues require attention."
        )

    else:

        st.error(
            "🔴 FAIL: Security issues were detected in the project."
        )

    st.divider()

    # ==================================================
    # SECURITY CHECKS
    # ==================================================

    st.markdown(
        '<div class="section-title">🔐 Security Checks</div>',
        unsafe_allow_html=True
    )

    check1, check2 = st.columns(2)

    with check1:

        if results["gitignore_present"]:

            st.success("✅ `.gitignore` file present")

        else:

            st.error("❌ `.gitignore` file missing")

        if results["env_file_detected"]:

            st.error("❌ `.env` file detected")

        else:

            st.success("✅ No `.env` file detected")

        if results["private_keys"]:

            st.error(
                f"❌ Private key files detected "
                f"({len(results['private_keys'])})"
            )

        else:

            st.success(
                "✅ No private key files detected"
            )

    with check2:

        if results["hardcoded_secrets"]:

            st.error(
                f"❌ Hardcoded secrets detected "
                f"({len(results['hardcoded_secrets'])})"
            )

        else:

            st.success(
                "✅ No hardcoded secrets detected"
            )

        if results["large_files"]:

            st.warning(
                f"⚠️ Large files detected "
                f"({len(results['large_files'])})"
            )

        else:

            st.success(
                "✅ No large files detected"
            )

        if results["suspicious_files"]:

            st.warning(
                f"⚠️ Suspicious files detected "
                f"({len(results['suspicious_files'])})"
            )

        else:

            st.success(
                "✅ No suspicious files detected"
            )

    st.divider()

    # ==================================================
    # FINDINGS SUMMARY
    # ==================================================

    st.markdown(
        '<div class="section-title">📋 Findings Summary</div>',
        unsafe_allow_html=True
    )

    summary1, summary2, summary3, summary4 = st.columns(4)

    with summary1:

        st.metric(
            "🔴 Secrets",
            len(results["hardcoded_secrets"])
        )

    with summary2:

        st.metric(
            "🔴 Private Keys",
            len(results["private_keys"])
        )

    with summary3:

        st.metric(
            "🟡 Large Files",
            len(results["large_files"])
        )

    with summary4:

        st.metric(
            "🟡 Suspicious Files",
            len(results["suspicious_files"])
        )

    st.divider()

    # ==================================================
    # DETAILED FINDINGS
    # ==================================================

    st.markdown(
        '<div class="section-title">🔎 Detailed Findings</div>',
        unsafe_allow_html=True
    )

    findings_found = False

    if results["hardcoded_secrets"]:

        findings_found = True

        st.markdown("### 🔴 Hardcoded Secrets")

        for finding in results["hardcoded_secrets"]:

            st.code(finding)

    if results["private_keys"]:

        findings_found = True

        st.markdown("### 🔴 Private Key Files")

        for finding in results["private_keys"]:

            st.code(finding)

    if results["env_file_detected"]:

        findings_found = True

        st.markdown("### 🟠 Environment File")

        st.code(".env file detected")

    if results["large_files"]:

        findings_found = True

        st.markdown("### 🟡 Large Files")

        for finding in results["large_files"]:

            st.code(finding)

    if results["suspicious_files"]:

        findings_found = True

        st.markdown("### 🟡 Suspicious Files")

        for finding in results["suspicious_files"]:

            st.code(finding)

    if not results["gitignore_present"]:

        findings_found = True

        st.markdown("### 🟠 Missing `.gitignore`")

        st.info(
            "Create a `.gitignore` file to prevent sensitive "
            "or unnecessary files from being committed."
        )

    if not findings_found:

        st.success(
            "🎉 No security issues were detected."
        )

    st.divider()

    # ==================================================
    # RECOMMENDATIONS
    # ==================================================

    st.markdown(
        '<div class="section-title">💡 Security Recommendations</div>',
        unsafe_allow_html=True
    )

    recommendations = []

    if not results["gitignore_present"]:

        recommendations.append(
            "Create a `.gitignore` file and exclude sensitive files."
        )

    if results["env_file_detected"]:

        recommendations.append(
            "Do not commit `.env` files containing credentials."
        )

    if results["private_keys"]:

        recommendations.append(
            "Remove private key files from the repository."
        )

    if results["hardcoded_secrets"]:

        recommendations.append(
            "Move secrets to environment variables or a secret manager."
        )

    if results["large_files"]:

        recommendations.append(
            "Review large files and remove unnecessary files from Git."
        )

    if results["suspicious_files"]:

        recommendations.append(
            "Review executable and archive files before committing them."
        )

    if recommendations:

        for recommendation in recommendations:

            st.info(
                f"💡 {recommendation}"
            )

    else:

        st.success(
            "🎉 No recommendations. The project passed all security checks."
        )

    st.divider()

    # ==================================================
    # SCAN AGAIN
    # ==================================================

    st.markdown(
        '<div class="section-title">🔄 Scan Another Project</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Use the sidebar to select another project or upload a new ZIP file."
    )
