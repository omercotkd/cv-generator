from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from models import CVWithPersonalInfo


def render_cv_template(cv: CVWithPersonalInfo, output_path: str | Path) -> None:
    """
    Render a CV using the Jinja template and save it to the specified path.
    
    Args:
        cv: CVWithPersonalInfo model containing the CV data
        output_path: Path where the rendered HTML file should be saved
    """
    # Set up Jinja2 environment
    template_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Load the template
    template = env.get_template("cv_template.html")
    
    # Render the template with CV data
    rendered_html = template.render(
        full_name=cv.full_name,
        email=cv.email,
        phone=cv.phone,
        links=cv.links,
        title=cv.title,
        self_summary=cv.self_summary,
        experiences=cv.experiences,
        certificates=cv.certificates,
        languages=cv.languages,
        education=cv.education,
        volunteer_work=cv.volunteer_work,
        skills=cv.skills,
    )
    
    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the rendered HTML
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
