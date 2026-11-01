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


## 30-Day Roadmap — Revised Execution Strategy

### Phase 1 — Foundation (Days 1–7)
- Project setup and lead qualification.
- Prospect research and verification.
- Website inspection and analysis.
- Automated quality checks and reporting.
- Demonstration projects.

### Phase 3 — AI-Assisted Project Delivery System (Days 8–21)
Bring forward the development infrastructure.

- Days 8–10: Project orchestration and requirements analysis.
- Days 11–14: AI-assisted website development workflow.
- Days 15–17: AI-assisted automation development workflow.
- Days 18–19: Automated testing and quality assurance.
- Days 20–21: Project documentation, backups and delivery workflow.

Build a minimum working system first. Improve it through practical projects.

### Phase 2 — Outreach and Client Discovery (Days 11–21)
Run alongside Phase 3 once a credible demonstration is available.

- Prepare personalized outreach.
- Contact qualified prospects with user approval.
- Track replies and follow-ups.
- Gather client requirements.
- Refine service offerings using actual feedback.

### Final Phase — Client Acquisition and Delivery (Days 22–30)
- Continue prospect follow-ups.
- Conduct client discovery.
- Prepare proposals and project specifications.
- Agree on scope, pricing and deadlines only with approval.
- Implement and test secured projects.
- Review progress and identify improvements.

### Execution Principles
- Getting the first paying client remains the primary objective.
- Build reusable workflows instead of repeatedly building from scratch.
- Prioritize working software over complex agent architectures.
- Use free tools and existing AI accounts wherever possible.
- Maintain human approval checkpoints.
- Never send outreach, spend money or deploy without approval.
- The revised sequence does not guarantee client acquisition or income.


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
