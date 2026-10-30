# SEO AI Studio — Multi-Agent SEO Content Generator

An AI-powered SEO content generation application built with **Microsoft AutoGen, OpenAI, Python, and Streamlit**.

SEO AI Studio uses four specialized AI agents to research topics, generate articles, optimize content for search engines, and review editorial quality. Articles that do not pass the review can be revised automatically.

## Features

- Four specialized AutoGen AI agents
- Web research using DuckDuckGo
- SEO-friendly article generation
- Keyword, heading, and metadata optimization
- AI editorial quality assessment across five categories
- Automatic revision and re-review (up to two revisions)
- Live workflow progress monitoring
- Streamlit dashboard with a dark-themed interface
- Editorial scorecard and review history
- Markdown content downloads
- Execution time and article word count tracking

## Multi-Agent Architecture

```text
User Input (Streamlit)
         |
         v
  Research Agent
  - Web research
  - Keywords
  - Content outline
         |
         v
  Content Writer Agent
  - Article generation
         |
         v
  SEO Optimization Agent
  - SEO title
  - Meta description
  - Heading optimization
  - Keyword placement
         |
         v
  Content Reviewer Agent
  - Quality evaluation
  - Score out of 100
         |
         +---- APPROVED ----> Final Article
         |
         +---- REVISION_REQUIRED
                     |
                     v
             SEO Optimization Agent
                     |
                     v
             Content Reviewer Agent
                     |
                Repeat up to
                2 revisions
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Microsoft AutoGen | Multi-agent orchestration |
| OpenAI GPT-4o-mini | AI model |
| Streamlit | Web interface |
| DuckDuckGo (`ddgs`) | Web research |
| python-dotenv | Environment configuration |

## Project Structure

```text
autogen-seo-agent/
├── agents/
│   ├── research_agent.py
│   ├── writer_agent.py
│   ├── seo_agent.py
│   └── reviewer_agent.py
├── tools/
│   └── web_search.py
├── workflows/
│   └── seo_workflow.py
├── .streamlit/
│   └── config.toml
├── app.py
├── test_research.py
├── test_writer.py
├── test_seo.py
├── test_workflow.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd autogen-seo-agent
```

Replace `<your-repository-url>` with your GitHub repository URL.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

Then activate the environment again.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
MODEL=gpt-4o-mini
```

Never commit `.env` or API keys to GitHub.

### 5. Start the application

```powershell
python -m streamlit run app.py
```

Open:

http://localhost:8501

## How to Use

1. Enter an article topic.
2. Specify the target audience.
3. Select the desired article length.
4. Click **Generate SEO Content**.
5. Watch the four agents execute.
6. Review the optimized article, editorial scores, and revision history.
7. Download the generated Markdown content.

## Editorial Review

The Reviewer Agent evaluates content across five categories, each worth 20 points:

| Category | Maximum Score |
|---|---:|
| Content Quality | 20 |
| SEO Optimization | 20 |
| Readability | 20 |
| Accuracy | 20 |
| Structure and Engagement | 20 |
| **Total** | **100** |

The configured approval threshold is **85/100**, provided there are no critical issues.

If the article requires improvements, the SEO Optimization Agent revises it using reviewer feedback. The Reviewer Agent then evaluates the revised article again.

The workflow supports a maximum of two automatic revisions.

**Note:** Editorial scores are AI-generated assessments, not Google search ranking scores or guarantees of factual accuracy. Human editorial review is recommended before publication.

## Testing

Run individual agent tests:

```powershell
python test_research.py
python test_writer.py
python test_seo.py
```

Run the complete workflow test:

```powershell
python test_workflow.py
```

Some tests make live API or search requests and may incur usage costs.

## Future Enhancements

- Docker containerization
- Deployment to a VPS
- Article export to additional formats
- Persistent generation history
- SEO keyword analytics
- WordPress publishing integration

## Security

- Keep API credentials in environment variables.
- Exclude `.env` and `.venv` from Git.
- Review generated articles before publishing.
- Apply appropriate API usage limits in production.

## License

No license has been specified yet.

---

Built as a practical multi-agent AI application using Microsoft AutoGen and Streamlit.