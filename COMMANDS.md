# AI Freelancing System — Command Reference

**Environment:** Windows 11 | PowerShell | Python 3.14.4  
**Project:** `C:\personal-ai-freelance`

This file stores frequently used commands for running, testing and maintaining the project.

---

## 1. Environment Setup

```powershell
# Navigate to project directory
cd C:\personal-ai-freelance

# Activate Python virtual environment
.\.venv\Scripts\Activate.ps1

# Check Python version
python --version

# Check installed Python packages
python -m pip list
```

## 2. Install Dependencies

```powershell
# Install Requests for HTTP requests and Ollama communication
python -m pip install requests

# Install BeautifulSoup for HTML parsing
python -m pip install beautifulsoup4

# Install Pandas for data processing
python -m pip install pandas

# Install Pytest for automated testing
python -m pip install pytest
```

## 3. Ollama Commands

```powershell
# Display locally installed Ollama models
ollama list

# Check whether the local Ollama API is responding
Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get

# Run Qwen3:8B interactively
ollama run qwen3:8b

# Check Python Requests installation
python -c "import requests; print(requests.__version__)"
```

## 4. Run Individual Python Modules

```powershell
# Test Python connection to Qwen3:8B
python -m scripts.ollama_client

# Fetch a website
python -m scripts.website_fetcher

# Inspect and extract website information
python -m scripts.website_inspector
```

## 5. Run Automated Tests

```powershell
# Run all project tests
python -m pytest tests/ -v

# Run all tests and display print statements
python -m pytest tests/ -v -s

# Test website parser
python -m pytest tests/test_website_parser.py -v -s

# Test robots.txt policy
python -m pytest tests/test_crawl_policy.py -v -s

# Test website fetcher
python -m pytest tests/test_website_fetcher.py -v -s

# Test complete website inspector
python -m pytest tests/test_website_inspector.py -v -s
```

## 6. Git Commands

```powershell
# Check modified and untracked files
git status

# Stage all changes
git add .

# Commit changes
git commit -m "Describe your changes"

# View recent commits
git log --oneline -10

# Push committed changes to GitHub
git push
```

## 7. Important Project Paths

| Purpose | Path |
|---|---|
| Ollama connection | scripts/ollama_client.py |
| Website fetching | scripts/website_fetcher.py |
| HTML extraction | scripts/website_parser.py |
| Crawling restrictions | scripts/crawl_policy.py |
| Website inspection | scripts/website_inspector.py |
| Automated tests | tests/ |
| Lead database | data/leads.csv |
| Research records | data/research_results.json |
| Audit records | data/audit_results.json |
| Reports | reports/ |

## 8. Development Rules

1. Activate `.venv` before running Python commands.
2. Run tests after modifying a module.
3. Use `python -m scripts.module_name` for project modules.
4. Use `python -m pytest` for tests.
5. Never commit passwords, API keys or private client information.
6. Update this file whenever new frequently used commands are introduced.

## Website Inspection and Analysis

| Command | Purpose |
|---|---|
| `python -m scripts.website_fetcher` | Fetch and test a website |
| `python -m scripts.website_inspector` | Extract website information |
| `python -m scripts.website_analyzer` | Generate and validate a business summary |
| `python -m scripts.report_generator` | Generate a Markdown business report |

## Testing

| Command | Purpose |
|---|---|
| `python -m pytest -v` | Run the complete test suite |
| `python -m pytest tests/test_business_summary_validator.py -v` | Test business summary validation |
| `python -m pytest tests/test_report_generator.py -v` | Test report generation |
| `python -m pytest tests/test_website_quality_checks.py -v` | Test website quality checks |
| `python -m pytest tests/test_website_inspector.py -v` | Test website inspection |
---

**Last updated:** 2026-10-30