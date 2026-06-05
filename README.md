# AI-Compiler-Studio


![Status](https://img.shields.io/badge/status-stable-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-web%20%7C%20cli-lightgrey)

**AI Compiler Studio** is an intelligent tool that transforms natural language application descriptions into complete full-stack architecture specifications. It generates database schemas, API endpoints, UI components, authentication rules, and business logic — all from a simple prompt.

---

## Features

- **Natural Language Processing** — Describe your app in plain English; get technical specifications instantly
- **Split-Panel Interface** — Left side for input, right side with tabbed views (Overview, Schema, Endpoints, Components, Rules, JSON)
- **Multi-Stage Pipeline** — Sequential generation, validation, and auto-repair of application blueprints
- **Auto-Repair Engine** — Automatically fixes missing fields and validates schema integrity
- **Quality Modes** — Choose between Balanced, Precise, Creative, or Fast generation profiles
- **Export Options** — Copy JSON to clipboard or download as configuration file
- **Example Prompts** — One-click templates for common application types
- **Python CLI** — Command-line interface for batch processing and automation

---

## How It Works

1. Enter your application idea in natural language
2. Select quality mode
3. Click Generate
4. View results across 6 tabs
5. Copy or export the configuration

---

## Getting Started

### Web Interface

Clone the repository and open `index.html` in any modern browser. No build steps, no dependencies.

### Python CLI

```bash
# Setup
mkdir -p ai_compiler/{src,tests,outputs}
cd ai_compiler
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"

# Usage
python main.py --prompt "Build a CRM with login and contacts"
python main.py --prompt "E-commerce platform" --quality high
python main.py --evaluate
Example Prompts
Category	Example
CRM	Build a CRM with user authentication, contact management, deal tracking, and role-based access
E-commerce	E-commerce platform with product catalog, shopping cart, payment integration, order history
Task Manager	Task manager with projects, subtasks, due dates, team assignments and comments
Social Media	Social media app with posts, likes, comments, follow system, notifications
Project Management	Project management tool with sprints, backlog, time tracking, and reports
Quality Modes
Mode	Best For
Balanced (GPT-4)	General purpose — good mix of speed and detail
Precise	Enterprise/technical accuracy, audit trails
Creative	Innovative UI components, micro-interactions
Fast	Quick drafts, lightweight specs
Output Structure
Generated specifications include:

Database — Engine type and models with fields

API — REST endpoints with methods and descriptions

UI — Component hierarchy and descriptions

Auth — Authentication type and role definitions

Rules — Business logic and validation rules

Use Cases
Rapid prototyping for full-stack applications

Educational tool for learning architecture patterns

Boilerplate generation for developers

Requirement gathering and documentation

Team alignment on technical specifications

Project Structure
text
ai_compiler/
├── index.html          # Web interface (single file)
├── main.py             # Python CLI entry point
├── src/                # Core modules (compiler, validator, repair_engine)
├── tests/              # Test suite
├── outputs/            # Generated JSON specifications
└── requirements.txt    # Python dependencies
Requirements
Web Interface: Any modern browser (Chrome, Firefox, Safari, Edge)

Python CLI:

Python 3.8+

OpenAI API key

Dependencies: openai, pydantic, click, python-dotenv, pytest

Commands Reference
Command	Description
python main.py --prompt "..."	Generate spec from prompt
python main.py --prompt "..." --quality high	Generate with high quality mode
python main.py --prompt "..." --quality fast	Generate with fast mode
python main.py --evaluate	Run evaluation on example prompts
python main.py --validate --file spec.json	Validate existing spec file
Auto-Repair Engine
The system automatically detects and fixes common issues:

Missing database models → Adds default User model

Empty endpoints array → Creates health check endpoint

Missing UI components → Adds base AppShell component

Undefined business rules → Applies default validations

License
MIT License — free for personal and commercial use.


Support
If this project helped you, please give it a star ⭐ on GitHub!
