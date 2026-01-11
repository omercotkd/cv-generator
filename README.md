# CV Generator 🎯

An intelligent CV generator powered by AI that creates tailored, professional PDF resumes based on job descriptions. Built with LangChain and Streamlit, this tool automatically customizes your CV to match specific job requirements.

## Features ✨

- **AI-Powered Customization**: Automatically tailors your CV content to match job descriptions
- **Professional PDF Output**: Generates clean, well-formatted PDF resumes
- **Flexible Formatting**: Customizable fonts, sizes, and styling options
- **Easy to Use**: Simple interface - just paste a job description and generate
- **Type-Safe**: Built with Pydantic models for data validation

## Prerequisites 📋

- Python 3.14 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

## Installation 🚀

### Using uv (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd cv-generator

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone <your-repo-url>
cd cv-generator

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration ⚙️

### 1. Create Your CV Data File

Create a `cv.json` file in the project root with your personal information:

```json
{
  "full_name": "Your Full Name",
  "email": "your.email@example.com",
  "phone": "+1234567890",
  "links": {
    "LinkedIn": "https://linkedin.com/in/yourprofile",
    "GitHub": "https://github.com/yourusername"
  },
  "descriptions": [
    "Your professional summary or key highlights"
  ],
  "experiences": [
    {
      "position": "Software Engineer",
      "company": "Company Name",
      "location": "City, Country",
      "start_date": "Jan 2020",
      "end_date": "Present",
      "bullets": [
        "Key achievement or responsibility 1",
        "Key achievement or responsibility 2"
      ],
      "skills": ["Python", "JavaScript", "Docker"]
    }
  ],
  "certificates": [
    {
      "name": "Certificate Name",
      "issuer": "Issuing Organization",
      "date": "Jan 2023",
      "link": "https://credential-url.com"
    }
  ],
  "languages": [
    {
      "language": "English",
      "proficiency": "Native"
    }
  ]
}
```

### 2. Configure CV Settings (Optional)

Customize the appearance of your CV by modifying the font and formatting settings in the configuration.

## Usage 💼

1. **Prepare your CV data**: Ensure your `cv.json` file is in the project folder

2. **Run the application**:
   ```bash
   streamlit run main.py
   ```

3. **Generate your CV**:
   - Paste the job description into the interface
   - Click generate
   - Download your tailored PDF CV

## Project Structure 📁

```
cv-generator/
├── main.py              # Main Streamlit application
├── models.py            # Pydantic data models for CV structure
├── cv.json              # Your personal CV data (not tracked in git)
├── cv.example.json      # Example CV structure
├── pyproject.toml       # Project dependencies and metadata
└── README.md            # This file
```

## CV Data Model 📝

The application uses structured Pydantic models to ensure data integrity:

- **CV**: Main model containing all CV information
  - `full_name`, `email`, `phone`: Contact information
  - `links`: Professional profile links (LinkedIn, GitHub, etc.)
  - `descriptions`: Professional summary/highlights
  - `experiences`: Work history with detailed achievements
  - `certificates`: Professional certifications
  - `languages`: Language proficiencies

- **CVSettings**: Formatting configuration
  - Font settings for headers, sections, and body text
  - Page margins and output format options

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

[Add your license information here]

## Support 💬

For questions or issues, please [open an issue](link-to-issues) on GitHub.