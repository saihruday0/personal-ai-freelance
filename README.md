# Personal AI Freelancing System

A Python-based, AI-assisted system designed to help identify potential freelance clients, analyze their websites, qualify prospects, and manage the freelancing workflow.

## Project Goal

Build a reusable system to help secure the first paying freelance client while developing practical skills in Python development and AI automation.

## Current Capabilities

### 1. Lead Management
- Store prospect information in CSV.
- Track business details, evidence, contact methods, and status.
- Validate lead records.
- Apply basic qualification and risk checks.

### 2. Website Inspection
- Fetch publicly accessible websites.
- Check HTTP responses and content types.
- Extract page titles and meta descriptions.
- Extract headings and page text.
- Identify internal and external links.
- Extract email and phone candidates.

### 3. AI Business Analysis
- Use Ollama with Qwen3:8B for business summaries.
- Identify business type, audience, and products or services.
- Validate the AI-generated output.
- Keep extracted website evidence separate from AI-generated summaries.

### 4. Website Quality Checks
- Detect missing page titles.
- Detect missing meta descriptions.
- Detect missing H1 headings.
- Detect multiple H1 headings.
- Generate structured findings with severity and evidence.

### 5. Report Generation
- Generate Markdown business analysis reports.
- Include extracted website information.
- Include accepted and rejected product or service claims.
- Include website quality findings.
- Highlight limitations and manual review requirements.

## Technology Stack

- Python
- Requests
- BeautifulSoup4
- Ollama
- Qwen3:8B
- Pytest
- Git and GitHub

## Project Structure

```text
personal-ai-freelance/
│
├── data/
│   ├── leads.csv
│   ├── research_results.json
│   ├── audit_results.json
│   └── sample_leads/
│       ├── labeldc_analysis.json
│       └── labeldc_sample.json
│
├── prompts/
│   ├── business_summary_prompt.txt
│   ├── website_analysis_prompt.txt
│   └── lead_research_agent.md
│
├── reports/
│   ├── labeldc_business_report.md
│   ├── lead_review.csv
│   └── lead_validation_report.txt
│
├── scripts/
│   ├── qualify_lead.py
│   ├── validate_leads.py
│   ├── ollama_client.py
│   ├── website_fetcher.py
│   ├── website_parser.py
│   ├── crawl_policy.py
│   ├── url_safety.py
│   ├── website_inspector.py
│   ├── website_analyzer.py
│   ├── analysis_validator.py
│   ├── business_summary_validator.py
│   ├── website_quality_checks.py
│   └── report_generator.py
│
├── templates/
├── tests/
├── COMMANDS.md
└── README.md