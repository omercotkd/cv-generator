from pydantic import BaseModel, Field
from typing import Optional, Literal


class CVSettings(BaseModel):
    
    class FontSettings(BaseModel):
        font_name: str = Field(..., title="Font Name")
        font_size: int = Field(..., title="Font Size")
        font_weight: int = Field(..., title="Font Weight")
    
    output_format: Literal["pdf"] = Field(..., title="Output Format")
    font_size: int = Field(..., title="Font Size")
    page_margin: float = Field(..., title="Page Margin (inches)")
    header_font: FontSettings = Field(..., title="Header Font Settings for name and ")
    sections_title_font: FontSettings = Field(..., title="Sections Title Font Settings")
    body_font: FontSettings = Field(..., title="Body Font Settings")

class CV(BaseModel):

    class Experience(BaseModel):
        position: str = Field(..., title="Position")
        company: str = Field(..., title="Company")
        location: str = Field(..., title="Location")
        start_date: str = Field(..., title="Start Date")
        end_date: str = Field(..., title="End Date")
        bullets: list[str] = Field(..., title="Bullets")
        skills: Optional[list[str]] = Field(None, title="Skills")

    class Certificate(BaseModel):
        name: str = Field(..., title="Certificate Name")
        issuer: str = Field(..., title="Issuer")
        date: str = Field(..., title="Date")
        link: Optional[str] = Field(None, title="Link")

    class LanguageProficiency(BaseModel):
        language: str = Field(..., title="Language")
        proficiency: str = Field(..., title="Proficiency Level")

    full_name: str = Field(..., title="Full Name")
    email: str = Field(..., title="Email Address")
    phone: str = Field(..., title="Phone Number")
    links: dict[str, str] = Field(default_factory=dict, title="Links")
    descriptions: Optional[list[str]] = Field(None, title="Description")
    experiences: list[Experience] = Field(..., title="Experiences")
    certificates: Optional[list[Certificate]] = Field(None, title="Certificates")
    languages: Optional[list[LanguageProficiency]] = Field(None, title="Languages")
