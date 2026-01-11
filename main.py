import streamlit as st
from pathlib import Path
import json
from models import CV
from cv_generator import generate_cv
from cv_analyzer import analyze_cv_file


def load_system_prompt() -> str:
    """Load system prompt from file."""
    prompt_path = Path("system_prompt.txt")
    if not prompt_path.exists():
        return "System prompt file not found."
    
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading system prompt: {str(e)}")
        return ""


def save_system_prompt(prompt: str) -> bool:
    """Save system prompt to file."""
    prompt_path = Path("system_prompt.txt")
    try:
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        return True
    except Exception as e:
        st.error(f"Error saving system prompt: {str(e)}")
        return False


def load_cv_data() -> CV | None:
    """Load CV data from cv.json file."""
    cv_path = Path("cv.json")
    if not cv_path.exists():
        return None
    
    try:
        with open(cv_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return CV(**data)
    except Exception as e:
        st.error(f"Error loading CV data: {str(e)}")
        return None


def save_cv_data(cv_data: CV) -> bool:
    """Save CV data to cv.json file."""
    cv_path = Path("cv.json")
    try:
        with open(cv_path, "w", encoding="utf-8") as f:
            json.dump(cv_data.model_dump(), f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving CV data: {str(e)}")
        return False


def handle_cv_upload(uploaded_file) -> CV | None:
    """Handle CV file upload and analysis."""
    if uploaded_file is None:
        return None
    
    try:
        # Read file content
        file_content = uploaded_file.read()
        filename = uploaded_file.name
        
        with st.spinner(f"🔍 Analyzing {filename}..."):
            # Analyze the CV and extract structured data
            cv_data = analyze_cv_file(file_content, filename)
            
            # Save to cv.json
            if save_cv_data(cv_data):
                st.success("✅ CV analyzed and saved successfully!")
                return cv_data
            else:
                st.error("Failed to save CV data")
                return None
                
    except NotImplementedError as e:
        st.warning(f"⚠️ {str(e)}")
        st.info("For now, please create a cv.json file manually. See README.md for the structure.")
        return None
    except Exception as e:
        st.error(f"❌ Error analyzing CV: {str(e)}")
        return None


def main():
    st.set_page_config(
        page_title="AI CV Generator",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("🎯 AI-Powered CV Generator")
    st.markdown("Generate a tailored CV optimized for your target job description")
    
    # Load CV data
    cv_data = load_cv_data()
    cv_exists = cv_data is not None
    
    # CV Upload/Reupload Section
    if not cv_exists:
        st.info("👋 Welcome! Please upload your CV to get started.")
        
        uploaded_file = st.file_uploader(
            "📤 Upload Your CV",
            type=["pdf", "docx", "txt"],
            help="Upload your CV in PDF, DOCX, or TXT format. The AI will analyze and extract your information."
        )
        
        if uploaded_file is not None:
            if st.button("🔍 Analyze CV", type="primary"):
                cv_data = handle_cv_upload(uploaded_file)
                if cv_data is not None:
                    st.rerun()
        
        st.divider()
        st.markdown("**Alternative:** You can also create a `cv.json` file manually. See the README.md for the structure.")
        return
    
    # Show reupload option when CV exists
    with st.expander("📤 Reupload CV", expanded=False):
        st.warning("⚠️ Uploading a new CV will replace your existing cv.json file.")
        
        uploaded_file = st.file_uploader(
            "Choose a new CV file",
            type=["pdf", "docx", "txt"],
            help="Upload your CV in PDF, DOCX, or TXT format.",
            key="reupload"
        )
        
        if uploaded_file is not None:
            if st.button("🔄 Replace CV", type="primary"):
                cv_data = handle_cv_upload(uploaded_file)
                if cv_data is not None:
                    st.rerun()
    
    # Display current CV info
    with st.expander("📋 Current CV Data", expanded=False):
        st.write(f"**Name:** {cv_data.full_name}")
        st.write(f"**Email:** {cv_data.email}")
        st.write(f"**Experiences:** {len(cv_data.experiences)} positions")
        if cv_data.certificates:
            st.write(f"**Certificates:** {len(cv_data.certificates)}")
        if cv_data.languages:
            st.write(f"**Languages:** {len(cv_data.languages)}")
    
    st.divider()
    
    # Create two columns for the main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=400,
            placeholder="Paste the full job description including requirements, responsibilities, and qualifications...",
            help="The AI will analyze this to tailor your CV"
        )
    
    with col2:
        st.subheader("🤖 System Prompt")
        
        # Initialize session state for system prompt if not exists
        if "system_prompt" not in st.session_state:
            st.session_state.system_prompt = load_system_prompt()
        
        # Toggle to enable/disable editing
        enable_edit = st.checkbox("Edit System Prompt", value=False)
        
        if enable_edit:
            edited_prompt = st.text_area(
                "Customize the AI instructions",
                value=st.session_state.system_prompt,
                height=320,
                help="Modify how the AI should tailor your CV"
            )
            
            col_save, col_reset = st.columns(2)
            with col_save:
                if st.button("💾 Save Changes", use_container_width=True):
                    if save_system_prompt(edited_prompt):
                        st.session_state.system_prompt = edited_prompt
                        st.success("Prompt saved!")
                        st.rerun()
            
            with col_reset:
                if st.button("🔄 Reload from File", use_container_width=True):
                    st.session_state.system_prompt = load_system_prompt()
                    st.rerun()
        else:
            st.text_area(
                "Current system prompt (read-only)",
                value=st.session_state.system_prompt,
                height=350,
                disabled=True,
                help="Enable 'Edit System Prompt' to modify"
            )
    
    st.divider()
    
    # Generate button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        generate_button = st.button(
            "🚀 Generate CV",
            type="primary",
            use_container_width=True,
            disabled=not job_description.strip()
        )
    
    # Handle CV generation
    if generate_button:
        if not job_description.strip():
            st.error("Please provide a job description")
            return
        
        with st.spinner("🔄 Generating your tailored CV..."):
            try:
                # Generate the CV
                pdf_path = generate_cv(
                    cv_data=cv_data,
                    job_description=job_description,
                    system_prompt=st.session_state.system_prompt
                )
                
                st.success("✅ CV generated successfully!")
                st.info("Note: CV generation with AI will be implemented using LangChain")
                
                # Display download/open options
                col_action1, col_action2 = st.columns(2)
                
                with col_action1:
                    # TODO: Implement actual file reading when PDF is generated
                    st.download_button(
                        label="📥 Download CV",
                        data=b"",  # Placeholder - will be actual PDF bytes
                        file_name=f"CV_{cv_data.full_name.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                with col_action2:
                    if st.button("🌐 Open in Browser", use_container_width=True):
                        st.info(f"CV would open at: {Path(pdf_path).absolute()}")
                        # TODO: Implement browser opening
                        # import webbrowser
                        # webbrowser.open(f"file://{Path(pdf_path).absolute()}")
                
            except Exception as e:
                st.error(f"❌ Error generating CV: {str(e)}")
    
    # Footer
    st.divider()
    st.markdown(
        "<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit and LangChain</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
