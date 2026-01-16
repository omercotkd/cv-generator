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
    class Link(BaseModel):
        label: str = Field(..., title="Link Label")
        # Optional - sometimes the LLM returned null for url
        url: Optional[str] = Field(None, title="Link URL")

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
        link: CV.Link = Field(..., title="Link")

    class LanguageProficiency(BaseModel):
        language: str = Field(..., title="Language")
        proficiency: str = Field(..., title="Proficiency Level")

    class Education(BaseModel):
        degree: str = Field(..., title="Degree")
        institution: str = Field(..., title="Institution")
        start_date: str = Field(..., title="Start Date")
        end_date: str = Field(..., title="End Date")
        details: Optional[list[str]] = Field(None, title="Details")

    class Skill(BaseModel):
        category: str = Field(..., title="Skill Category")
        skills: list[str] = Field(..., title="Skills")

    title: str = Field(..., title="Professional Title")
    self_summary: str = Field(..., title="Description")
    experiences: list[Experience] = Field(default_factory=list, title="Experiences")
    certificates: list[Certificate] = Field(default_factory=list, title="Certificates")
    languages: list[LanguageProficiency] = Field(
        default_factory=list, title="Languages"
    )
    education: list[Education] = Field(default_factory=list, title="Education")
    volunteer_work: list[Experience] = Field(
        default_factory=list, title="Volunteer Work"
    )
    skills: list[Skill] = Field(default_factory=list, title="Skills", min_length=1)


class CVWithPersonalInfo(CV):

    full_name: str = Field(..., title="Full Name")
    email: str = Field(..., title="Email Address")
    phone: str = Field(..., title="Phone Number")
    links: list[CV.Link] = Field(
        default_factory=list, title="Links (e.g., LinkedIn, GitHub)"
    )

    def into_cv(self) -> CV:
        return CV(
            title=self.title,
            self_summary=self.self_summary,
            experiences=self.experiences,
            certificates=self.certificates,
            languages=self.languages,
            education=self.education,
            volunteer_work=self.volunteer_work,
        )

    @staticmethod
    def from_cv(
        cv: CV, full_name: str, email: str, phone: str, links: list[CV.Link]
    ) -> "CVWithPersonalInfo":
        return CVWithPersonalInfo(
            full_name=full_name,
            email=email,
            phone=phone,
            links=links,
            title=cv.title,
            self_summary=cv.self_summary,
            experiences=cv.experiences,
            certificates=cv.certificates,
            languages=cv.languages,
            education=cv.education,
            volunteer_work=cv.volunteer_work,
            skills=cv.skills,
        )

