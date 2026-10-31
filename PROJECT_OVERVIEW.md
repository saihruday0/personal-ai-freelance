# Project Overview — Personal AI Freelancing System

## Goal
Build a practical, reusable AI-assisted freelancing workflow and secure the first paying freelance client. The system should support prospect research, qualification, website analysis, outreach preparation, client discovery, project delivery, and review.

## Service Direction
Initial service hypothesis: a combination of website development and business automation.

Potential services:
- Responsive landing pages and business/creator websites
- Enquiry forms and lead organization
- Notifications and simple workflow automations
- Reports and small business process improvements

Initial audience hypothesis: online businesses and creators. This niche and offer are not yet validated; use prospect evidence and real conversations to refine them.

## Constraints
- Work time: approximately 2–3 hours per day.
- Budget cap: ₹1,000 for the 30-day plan.
- Prefer free tools and existing AI accounts.
- No paid API, subscription, domain, or other purchase without explicit approval.
- Human approval required before sending client messages, agreeing to scope/prices/contracts/deadlines, spending money, deploying/publishing, or handling sensitive client data.
- No mass outreach, no bypassing website rate limits, and no prohibited scraping.
- Keep evidence, AI-generated claims, and human decisions distinguishable.

## Working Preferences
- Give concise, direct instructions.
- Work one task at a time.
- Provide exact Windows paths, complete code when code changes are needed, and exact commands.
- Wait for the user's result before moving to the next task.
- Avoid unnecessary diagnostics, narration, repeated work, and speculative changes.
- Do not assume a task is complete until the user confirms it.

## Environment
- OS: Windows 11
- Editor: VS Code
- Python: 3.14.4
- Git: 2.54.0.windows.1
- Project root: `C:\personal-ai-freelance`
- Virtual environment: `.venv`
- Activate with: `\.venv\Scripts\Activate.ps1`
- Local Ollama API: `http://localhost:11434`
- Primary local model: `qwen3:8b`
- Other installed models previously reported: `gemma4:12b`, `mytutor:latest`
- Python packages: requests, beautifulsoup4, pandas, pytest

## 30-Day Roadmap
- Days 1–7: foundation, prospect research, lead qualification, website inspection, and report generation.
- Days 8–14: outreach preparation and supervised sending, reply tracking, requirements gathering, proposal/demo, and offer refinement.
- Days 15–21: client folders, project specification, implementation workflow, automation workflow, testing, backups, and delivery rehearsal.
- Days 22–30: prospect follow-up, discovery, proposals, scope/pricing/payment terms, implementation if a project is secured, delivery, feedback, and final review.

The roadmap is a working plan, not a guarantee of obtaining a client or income.

## Current Technical Capabilities
- CSV-based lead tracking and validation.
- Basic lead qualification and risk/completeness checks.
- Website fetching with HTTP handling, redirect limits, URL safety checks, and crawl-policy checks.
- HTML extraction of title, meta description, headings, page text, links, email candidates, and phone candidates.
- Local Qwen-based business summary generation.
- Structural validation of generated business summaries.
- Deterministic website quality checks:
  - WQ001: missing page title
  - WQ002: missing meta description
  - WQ003: no non-empty H1 detected
  - WQ004: multiple H1 headings detected
- Markdown business report generation including quality findings.
- Pytest automated test suite.

## Important Technical Caveats
- The website quality checks detect observable extraction results; they do not prove lost sales, poor conversion, or business performance.
- The business-summary validator checks structure and selected exact-match claims; it does not semantically prove every AI statement.
- Qwen may hallucinate or over-infer. Human review remains mandatory.
- URL safety and crawling controls are basic safeguards, not a guarantee against every SSRF or DNS-rebinding scenario.
- Label DC returned HTTP 429 after repeated requests. Do not retry or bypass the restriction; use the saved fixture for development.

## Key Project Paths
- `data/leads.csv`
- `data/research_results.json`
- `data/audit_results.json`
- `data/sample_leads/labeldc_sample.json`
- `data/sample_leads/labeldc_analysis.json`
- `reports/labeldc_business_report.md`
- `reports/lead_review.csv`
- `reports/lead_validation_report.txt`
- `scripts/`
- `tests/`
- `prompts/`
- `templates/`
