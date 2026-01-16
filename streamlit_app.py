import streamlit as st
from pathlib import Path
import json
import uuid
from models import CVWithPersonalInfo
from cv_generator import generate_cv
from cv_analyzer import analyze_cv_file
from cv_renderer import render_cv_template
from text import TRANSLATIONS


# ========================== Constants ==========================
CV_FILE_PATH = Path("cv.json")
USER_STORY_FILE_PATH = Path("user_story.txt")


# ========================== Helper Functions ==========================


def load_cv_data() -> str:
    """Load CV data from file and return as formatted JSON string."""
    try:
        if CV_FILE_PATH.exists():
            with open(CV_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return json.dumps(data, indent=2, ensure_ascii=False)
        return ""
    except Exception as e:
        st.error(f"{st.session_state.translate['cv_load_error']}: {str(e)}")
        return ""


def save_cv_data(cv_json_str: str) -> bool:
    """Save CV data to file from JSON string."""
    try:
        cv_data = json.loads(cv_json_str)
        with open(CV_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(cv_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"{st.session_state.translate['cv_save_error']}: {str(e)}")
        return False


def load_user_story() -> str:
    """Load user story from file."""
    try:
        if USER_STORY_FILE_PATH.exists():
            with open(USER_STORY_FILE_PATH, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    except Exception as e:
        st.error(f"{st.session_state.translate['user_story_load_error']}: {str(e)}")
        return ""


def save_user_story(story: str) -> bool:
    """Save user story to file."""
    try:
        with open(USER_STORY_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(story)
        return True
    except Exception as e:
        st.error(f"{st.session_state.translate['user_story_save_error']}: {str(e)}")
        return False


def process_uploaded_cv(uploaded_file):
    """Process uploaded CV file - to be implemented."""
    # TODO: Implement CV file processing
    pass


def generate_tailored_cv(job_description: str, user_input: str):
    """Generate tailored CV based on job description and user input."""
    try:
        # Load CV data from file
        with open(CV_FILE_PATH, "r", encoding="utf-8") as f:
            cv_data = json.load(f)
        
        # Parse into pydantic model
        
        base_cv = CVWithPersonalInfo(**cv_data)
        
        # Combine system prompt with user story if available
        user_story = load_user_story()
        
        # Generate tailored CV
        tailored_cv = generate_cv(base_cv, job_description, user_story)
        
        # Ensure temp folder exists
        temp_folder = Path("temp")
        temp_folder.mkdir(exist_ok=True)
        
        # Save generated CV to temp folder
        output_path = temp_folder / "tailored_cv.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(tailored_cv.model_dump(), f, indent=2, ensure_ascii=False)
        
        # Render HTML version with random filename
        random_filename = f"cv_{uuid.uuid4().hex[:8]}.html"
        html_output_path = temp_folder / random_filename
        render_cv_template(tailored_cv, html_output_path)
        
        st.success(f"{st.session_state.translate.get('generate_success', 'CV generated successfully!')}")
        st.info(f"Saved JSON to: {output_path}")
        st.info(f"Saved HTML to: {html_output_path}")
        
        # Display the generated CV
        with st.expander("View Generated CV"):
            st.json(tailored_cv.model_dump())
        
    except Exception as e:
        st.error(f"Error generating CV: {str(e)}")


# ========================== UI Sections ==========================


def render_cv_edit_section(translate):
    """Render the CV editing section."""
    st.subheader(translate["cv_section_title"])

    # Load CV data
    cv_data = load_cv_data()

    if not cv_data:
        st.info(translate["cv_empty_message"])

    # Text area for CV editing
    cv_text = st.text_area(
        label="CV JSON",
        value=cv_data,
        height=400,
        placeholder=translate["cv_edit_placeholder"],
        label_visibility="collapsed",
    )

    # Save button
    if st.button(translate["save_cv_button"], type="primary", use_container_width=True):
        if cv_text.strip():
            if save_cv_data(cv_text):
                st.success(translate["cv_save_success"])
                st.rerun()


def render_upload_section(translate):
    """Render the CV upload section."""
    st.subheader(translate["upload_section_title"])

    uploaded_file = st.file_uploader(
        translate["upload_file_label"],
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
    )

    if st.button(translate["upload_button"], use_container_width=True):
        if uploaded_file is not None:
            # TODO: Call process_uploaded_cv function when implemented
            st.info("Upload processing will be implemented soon")
        else:
            st.warning("Please select a file first")


def render_user_story_section(translate):
    """Render the user story editing section."""
    st.subheader(translate["user_story_section_title"])

    # Load user story
    user_story = load_user_story()

    # Text area for user story
    story_text = st.text_area(
        label="User Story",
        value=user_story,
        height=400,
        placeholder=translate["user_story_placeholder"],
        label_visibility="collapsed",
        key="user_story_input",
    )

    # Auto-save on change
    if story_text != user_story:
        if save_user_story(story_text):
            st.success(translate["user_story_save_success"])


def render_generate_cv_section(translate):
    """Render the CV generation section."""
    st.subheader(translate["generate_section_title"])

    # Job description input
    job_description = st.text_area(
        translate["job_description_label"],
        height=200,
        placeholder=translate["job_description_placeholder"],
        key="job_description_input",
    )

    # Additional user input
    user_input = st.text_area(
        translate["user_input_label"],
        height=150,
        placeholder=translate["user_input_placeholder"],
        key="additional_input",
    )

    # Generate button
    if st.button(
        translate["generate_button"], type="primary", use_container_width=True
    ):
        # Validation
        if not CV_FILE_PATH.exists():
            st.error(translate["generate_error_no_cv"])
        elif not job_description.strip():
            st.error(translate["generate_error_no_job_desc"])
        else:
            with st.spinner("Generating tailored CV..."):
                generate_tailored_cv(job_description, user_input)


# ========================== Main App ==========================


def main():
    # Initialize translation
    translate = TRANSLATIONS["en"]
    st.session_state.translate = translate

    # Page config
    st.set_page_config(
        page_title=translate["browser_title"], page_icon="📄", layout="wide"
    )

    # Header
    st.title(translate["page_title"])
    st.markdown(translate["page_description"])
    st.divider()

    # ========================== Layout ==========================

    # Top row: CV Edit (left) | User Story (right)
    col1, col2 = st.columns(2)

    with col1:
        render_cv_edit_section(translate)
        st.markdown("---")
        render_upload_section(translate)

    with col2:
        render_user_story_section(translate)

    st.divider()

    # Bottom section: Generate CV (full width)
    render_generate_cv_section(translate)


if __name__ == "__main__":
    main()
