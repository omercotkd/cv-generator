from typing import TypedDict

class TranslationKeys(TypedDict):
    browser_title: str
    page_title: str
    page_description: str
    
    # CV Edit Section
    cv_section_title: str
    cv_edit_placeholder: str
    cv_empty_message: str
    cv_load_error: str
    cv_save_success: str
    cv_save_error: str
    save_cv_button: str
    
    # Upload CV Section
    upload_section_title: str
    upload_button: str
    upload_file_label: str
    upload_success: str
    upload_error: str
    
    # User Story Section
    user_story_section_title: str
    user_story_placeholder: str
    user_story_save_success: str
    user_story_save_error: str
    user_story_load_error: str
    
    # Generate CV Section
    generate_section_title: str
    job_description_label: str
    job_description_placeholder: str
    user_input_label: str
    user_input_placeholder: str
    generate_button: str
    generate_error_no_cv: str
    generate_error_no_job_desc: str
    