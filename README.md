# Blue Harbor Investment Research Agent

> **A production-style Agentic AI learning POC on Databricks for multi-agent investment research across unstructured earnings documents and structured portfolio holdings.**

[![Databricks](https://img.shields.io/badge/Databricks-Agentic%20AI-EF3E2F?logo=databricks&logoColor=white)](https://www.databricks.com/)
[![MLflow](https://img.shields.io/badge/MLflow-GenAI%20Tracing%20%26%20Evaluation-0194E2?logo=mlflow&logoColor=white)](https://mlflow.org/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)](#implementation-roadmap)

---

## Overview

**Blue Harbor Investment Research Agent** is a hands-on Agentic AI proof of concept designed to demonstrate how a modern enterprise AI system can reason across multiple data domains and specialist capabilities.

The system answers investment-research questions that cannot be solved from a single source.

### Flagship business question

> **Which companies lowered their outlook this quarter, and how much do we own of them?**

Answering this requires the system to:

1. Search and interpret **unstructured earnings reports, call transcripts, and analyst notes**.
2. Identify companies whose management **lowered forward guidance**.
3. Query **structured portfolio holdings** for those companies.
4. Coordinate dependent agent and tool calls.
5. Synthesize the results into one grounded response.
6. Return evidence and citations.
7. Produce traces that can be evaluated for routing, retrieval, tool use, correctness, latency, and reliability.

This repository is intentionally built as a **learning-to-production journey** rather than a single notebook demo.

---

## Why This Project?

A basic RAG application can answer:

> “What did NovaChip say about guidance?”

A structured-data assistant can answer:

> “How much NOVA do we own?”

The more interesting enterprise problem is:

> “Which companies lowered guidance, why did they lower it, how much exposure do we have, and which funds are most affected?”

That requires **orchestration across specialist reasoning and governed tools**.

```text
LLM
  ↓
Tool Calling
  ↓
RAG + Structured Analytics
  ↓
Specialist Agents
  ↓
Supervisor / Coordinator
  ↓
Multi-Agent Orchestration
  ↓
MCP
  ↓
State + Memory
  ↓
Guardrails + Governance
  ↓
Tracing + Evaluation
  ↓
CI/CD + Deployment + Monitoring
```

---

## Target Architecture

<img width="1536" height="1024" alt="Target State Architecture" src="https://github.com/user-attachments/assets/a5105585-f978-47a6-a398-164ddd3be361" />


### Runtime responsibility

| Layer | Responsibility |
|---|---|
| **Supervisor / Coordinator** | Intent understanding, planning, routing, delegation, dependency handling, synthesis |
| **Research Agent** | Earnings interpretation, guidance-change classification, evidence extraction, citations |
| **Portfolio Agent** | Holdings, fund exposure, structured analytics |
| **AI Search MCP** | Governed semantic retrieval over research documents |
| **Genie MCP** | Governed natural-language access to structured portfolio data |
| **UC / deterministic tools** | Calculations and operations that should not depend on free-form LLM reasoning |
| **Unity Catalog** | Data and tool permissions, lineage, governed assets |
| **Unity AI Gateway** | Centralized AI/tool governance and controls |
| **MLflow** | Tracing, evaluation, feedback, regression testing, observability |
| **Databricks Apps** | End-user application and deployment surface |

> **Design principle:** not everything should be an agent. Reasoning belongs in agents; deterministic execution belongs in tools; security belongs in policy and permissions; quality belongs in evaluation.

---

## Modern Agentic AI Concepts Covered

### Agent architecture

- Supervisor / coordinator pattern
- Specialist-agent decomposition
- Agent-as-tool orchestration
- Sequential and dependency-aware delegation
- Tool selection and typed tool contracts
- Multi-turn conversation state
- Optional long-term memory
- Controlled clarification and escalation
- Maximum-turn / loop protection
- Retry, timeout, fallback, and partial-result handling

### Knowledge & tools

- Retrieval-Augmented Generation (RAG)
- Document parsing and chunking
- Embeddings and semantic retrieval
- Databricks **AI Search**
- Model Context Protocol (**MCP**)
- Genie for structured analytics
- Unity Catalog Functions
- Deterministic calculation tools
- Metadata filtering and source citations

### AI engineering

- Agent prompts and instructions
- Prompt version management
- Structured outputs
- MLflow Tracing
- Offline evaluation datasets
- LLM-as-a-judge / scorer-based evaluation
- RAG relevance and groundedness evaluation
- Tool-call correctness
- Supervisor routing evaluation
- Multi-turn evaluation
- Human feedback
- Regression testing
- Cost, token, and latency analysis

### Security & governance

- Unity Catalog permissions
- Least-privilege tool access
- Unity AI Gateway
- Authentication / OAuth
- MCP governance
- Prompt-injection defenses
- Indirect prompt-injection testing
- Data-exfiltration boundaries
- Input/output guardrails
- Auditability and lineage

### Production engineering

- Git-based development
- Modular Python package structure
- Unit and integration tests
- CI/CD-ready project layout
- Evaluation quality gates
- Databricks Apps deployment
- Monitoring and feedback loops
- Performance and reliability testing

---

## Two Orchestration Paths We Will Learn

The project intentionally explores **both** approaches.

### 1. Build the coordinator ourselves

The first implementation exposes the orchestration mechanics so we can understand:

```text
User Request
    ↓
Coordinator
    ↓
Intent / Plan
    ↓
Select Specialist
    ↓
Call Agent / Tool
    ↓
Inspect Result
    ↓
Call Dependent Specialist
    ↓
Synthesize
```

This version is useful for learning routing, handoffs, traces, tool contracts, failure handling, and orchestration behavior.

### 2. Compare with Databricks Supervisor Agent

After the mechanics are understood, the same use case can be implemented or compared using the managed **Databricks Supervisor Agent**, which can coordinate specialist agents and governed tools.

This allows the project to demonstrate both:

- **how multi-agent orchestration works**, and
- **how Databricks productizes the pattern**.

---

## Sample Data

All data in this repository is **fictional and synthetic**.

### Research documents

The starter dataset contains Q2 2026 material for five fictional companies:

| Ticker | Company | Sector |
|---|---|---|
| `NOVA` | NovaChip Technologies | Semiconductors |
| `EVRG` | Evergreen Energy Systems | Renewable Energy |
| `APXR` | Apex Retail Group | Consumer Retail |
| `MDHN` | Meridian Health Systems | Healthcare Services |
| `VTXI` | Vertex Industrial Technologies | Industrials |

For each company, the dataset includes:

- Earnings report
- Earnings-call transcript
- Internal analyst research note

The documents deliberately contain a mixture of lowered, maintained, and raised guidance, plus management rationale, financial ranges, and analyst commentary.

### Structured portfolio data

The structured dataset contains:

- `companies`
- `funds`
- `holdings`
- `document_manifest`

The holdings are spread across fictional Blue Harbor funds so the agent must aggregate exposure rather than retrieve a single precomputed answer.

---

## Unity Catalog Design

```text
blue_harbor
│
├── research
│   ├── raw_documents           # UC Volume
│   ├── document_manifest       # Delta table
│   ├── document_chunks         # Delta table - later
│   └── <ai_search_index>       # AI Search - later
│
├── portfolio
│   ├── seed_data               # UC Volume
│   ├── companies               # Delta table
│   ├── funds                   # Delta table
│   └── holdings                # Delta table
│
└── agent
    ├── functions               # UC functions - later
    ├── evaluation_data         # later
    └── operational assets      # later
```

Unity Catalog is treated as part of the application architecture, not merely a storage location.

---

## Repository Structure

```text
blue-harbor-investment-agent/
│
├── README.md
│
├── config/
│   └── ...
│
├── data/
│   ├── documents/
│   │   ├── NOVA_Q2_2026_earnings_report.md
│   │   ├── NOVA_Q2_2026_earnings_call.md
│   │   └── ...
│   │
│   └── seed/
│       ├── companies.csv
│       ├── funds.csv
│       ├── holdings.csv
│       └── documents_manifest.csv
│
├── notebooks/
│   ├── 00_environment_check.py
│   ├── 01_setup_unity_catalog.py
│   ├── 02_load_sample_data.py
│   ├── 03_ingest_documents.py
│   ├── 04_prepare_document_chunks.py
│   ├── 05_build_ai_search.py
│   ├── 06_test_retrieval.py
│   ├── 07_build_research_agent.py
│   ├── 08_build_portfolio_agent.py
│   ├── 09_build_supervisor.py
│   └── 10_evaluate_system.py
│
├── src/
│   └── blue_harbor_agent/
│       ├── __init__.py
│       ├── agents/
│       │   ├── research_agent.py
│       │   ├── portfolio_agent.py
│       │   └── supervisor_agent.py
│       ├── rag/
│       │   ├── chunking.py
│       │   └── retrieval.py
│       ├── tools/
│       │   ├── research_tools.py
│       │   ├── portfolio_tools.py
│       │   └── calculation_tools.py
│       ├── prompts/
│       │   └── ...
│       ├── guardrails/
│       │   └── ...
│       └── utils/
│           └── ...
│
├── evals/
│   ├── evaluation_questions.jsonl
│   └── GROUND_TRUTH_DO_NOT_INDEX.md
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── setup/
│   └── 01_create_catalog.sql
│
├── docs/
│   ├── architecture.md
│   ├── business_problem.md
│   └── decisions/
│
└── app/
    └── ...
```

> The repository will evolve incrementally. Files shown above represent the target structure and are not all expected to exist on day one.

---

## Data Flow

### Unstructured research path

```text
Markdown / Research Documents
            ↓
      UC Raw Volume
            ↓
     Parse + Normalize
            ↓
          Chunk
            ↓
      Delta Chunk Table
            ↓
       Embeddings
            ↓
      Databricks AI Search
            ↓
        AI Search MCP
            ↓
       Research Agent
```

### Structured portfolio path

```text
CSV Seed Data
      ↓
UC Seed Volume
      ↓
Delta Tables
      ↓
Unity Catalog
      ↓
Genie
      ↓
Genie MCP
      ↓
Portfolio Agent
```

### Cross-domain reasoning path

```text
"Which companies lowered their outlook
 and how much do we own?"

                ↓
          Supervisor
                ↓
      ┌─────────┴─────────┐
      │                   │
Research Agent       Portfolio Agent
      │                   ▲
      │ identifies        │ queries exposure
      │ companies         │ for identified names
      └──────────►────────┘
                ↓
         Supervisor
                ↓
      Grounded synthesis
        + citations
```

---

## Evaluation Strategy

A final answer can be correct for the wrong reason, so this project evaluates the **execution path**, not only the response text.

| Layer | Example checks |
|---|---|
| Supervisor | Was the correct specialist selected? |
| Research retrieval | Were the relevant documents/chunks retrieved? |
| Research reasoning | Was guidance classified correctly? |
| Citations | Does the cited evidence actually support the claim? |
| Portfolio agent | Was the structured-data tool used when required? |
| Tool call | Were tool arguments correct? |
| Structured result | Were holdings aggregated correctly? |
| Synthesis | Did the final answer combine both domains correctly? |
| Groundedness | Are all material claims supported by evidence? |
| Reliability | Were failures handled without runaway loops? |
| Operations | What were latency, tokens, tool calls, and errors? |

The repository includes a controlled evaluation dataset and a separate ground-truth file.

> **Never add `evals/GROUND_TRUTH_DO_NOT_INDEX.md` to the RAG corpus or AI Search index.**

---

## Security Test Cases

Security is treated as executable behavior, not an architecture-box label.

The POC will eventually test scenarios such as:

- Prompt injection from the user
- **Indirect prompt injection embedded inside retrieved documents**
- Attempts to invoke unauthorized tools
- Attempts to retrieve data outside permitted scopes
- Malformed tool arguments
- Excessive agent/tool loops
- Sensitive information leakage
- Unsupported claims without evidence

The intended protection model is layered:

```text
User
  ↓
Application Guardrails
  ↓
Supervisor Instructions
  ↓
Authorized Agent / Tool
  ↓
Unity AI Gateway
  ↓
Unity Catalog Permissions
  ↓
Governed Data
```

---

## Getting Started

### Prerequisites

- GitHub account
- Databricks workspace
- Unity Catalog access
- Serverless compute where available
- Access to the AI/agent features required by the implementation phase

This project is designed to be developed in a **Databricks Git folder** backed by this GitHub repository.

> Databricks Free Edition can be used for the learning POC where the required features are available. Preview/Beta availability and usage quotas can vary by workspace.

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd blue-harbor-investment-agent
```

### 2. Connect it to Databricks

Create a **Git folder** in the Databricks workspace and clone this repository.

### 3. Validate the environment

The first implementation step is:

```text
notebooks/00_environment_check.py
```

This validates current identity, catalog access, schemas and volumes, serverless execution, installed packages, model access, AI Search availability, and relevant agent capabilities.

### 4. Create the data foundation

After the environment check passes:

```text
setup/01_create_catalog.sql
```

creates the initial Unity Catalog structure.

### 5. Upload synthetic documents

```text
/Volumes/blue_harbor/research/raw_documents/
```

### 6. Upload seed data

```text
/Volumes/blue_harbor/portfolio/seed_data/
```

### 7. Create Delta tables

Run the sample data loader to create the portfolio and research metadata tables.

From there, the project proceeds incrementally into document ingestion, RAG, AI Search, specialist agents, and orchestration.

---

## Implementation Roadmap

- [ ] **Phase 0 — Environment validation**
  - [ ] GitHub + Databricks Git folder
  - [ ] Workspace capability check
  - [ ] Model / AI feature availability

- [ ] **Phase 1 — Data foundation**
  - [ ] Unity Catalog structure
  - [ ] UC Volumes
  - [ ] Synthetic portfolio Delta tables
  - [ ] Research document ingestion

- [ ] **Phase 2 — RAG**
  - [ ] Parse and normalize documents
  - [ ] Chunking strategy
  - [ ] Embeddings
  - [ ] AI Search index
  - [ ] Retrieval tests
  - [ ] Citation metadata

- [ ] **Phase 3 — Research Agent**
  - [ ] Earnings-specialist prompt
  - [ ] AI Search tool / MCP
  - [ ] Guidance classification
  - [ ] Evidence + citations
  - [ ] MLflow traces

- [ ] **Phase 4 — Structured analytics**
  - [ ] Holdings query contract
  - [ ] Genie configuration
  - [ ] Genie MCP
  - [ ] Structured-data tests

- [ ] **Phase 5 — Portfolio Agent**
  - [ ] Exposure / holdings reasoning
  - [ ] Structured tool calls
  - [ ] Error handling
  - [ ] MLflow traces

- [ ] **Phase 6 — Multi-agent orchestration**
  - [ ] Custom coordinator
  - [ ] Research + Portfolio delegation
  - [ ] Sequential dependency handling
  - [ ] Result synthesis
  - [ ] Loop / turn limits
  - [ ] Compare with Databricks Supervisor Agent

- [ ] **Phase 7 — State & memory**
  - [ ] Multi-turn context
  - [ ] Follow-up references
  - [ ] Optional durable memory

- [ ] **Phase 8 — Security & governance**
  - [ ] Least privilege
  - [ ] Unity AI Gateway
  - [ ] Prompt-injection tests
  - [ ] Tool authorization
  - [ ] Guardrails

- [ ] **Phase 9 — Evaluation**
  - [ ] Golden evaluation dataset
  - [ ] Retrieval evaluation
  - [ ] Groundedness
  - [ ] Tool-call correctness
  - [ ] Routing evaluation
  - [ ] Multi-turn evaluation
  - [ ] Regression suite

- [ ] **Phase 10 — Productionization**
  - [ ] Databricks App
  - [ ] Authentication
  - [ ] CI/CD
  - [ ] Evaluation quality gates
  - [ ] Monitoring
  - [ ] Human feedback
  - [ ] Performance / reliability testing

---

## Engineering Principles

1. **Start simple, then add autonomy.**
2. **Do not create an agent where a deterministic tool is better.**
3. **Make orchestration observable.**
4. **Treat data permissions as part of agent design.**
5. **Require evidence for research claims.**
6. **Evaluate intermediate decisions, not only final answers.**
7. **Version prompts, models, tools, and evaluation datasets.**
8. **Design failures intentionally: retries, timeouts, fallbacks, and limits.**
9. **Keep runtime knowledge separate from evaluation ground truth.**
10. **A notebook working once is not the definition of production readiness.**

---

## Example Questions

```text
Which companies lowered their outlook this quarter,
and how much do we own of them?
```

```text
Why did management lower guidance for those companies?
```

```text
Which Blue Harbor fund has the largest exposure
to companies that reduced guidance?
```

```text
Did Apex Retail lower its outlook?
Show the evidence.
```

```text
Summarize the major guidance changes this quarter
and rank them by portfolio exposure.
```

---

## Current Status

**Status: Active learning POC — implementation in progress.**

The repository currently contains the synthetic data foundation and project structure. Agent, retrieval, orchestration, evaluation, and deployment components are added phase by phase so each design decision can be understood and tested independently.

---

## Technology Stack

| Category | Technology |
|---|---|
| Platform | Databricks |
| Data governance | Unity Catalog |
| Structured data | Delta Lake |
| Unstructured retrieval | Databricks AI Search |
| Structured analytics | Genie |
| Tool protocol | MCP |
| Multi-agent orchestration | Custom coordinator + Databricks Supervisor Agent comparison |
| Agent SDK | OpenAI Agents SDK / compatible Databricks agent interfaces |
| Observability | MLflow Tracing |
| Evaluation | MLflow GenAI Evaluation |
| AI governance | Unity AI Gateway |
| Application | Databricks Apps |
| Source control | GitHub + Databricks Git folders |
| Language | Python / SQL |

---

## Important Notes

- **AI Search** is the current Databricks name for the capability previously known as Vector Search.
- Some Databricks agent, MCP, Genie, and governance capabilities may be Preview/Beta or region/workspace dependent.
- The implementation validates workspace capabilities before depending on a feature.
- The repository uses synthetic data only and contains no real portfolio, employer, customer, or investor information.

---

## License & Disclaimer

This repository is a **learning and demonstration POC**.

All company names, investment funds, research documents, holdings, financial values, and scenarios are synthetic and fictional.

Nothing in this repository constitutes investment advice, financial advice, trading advice, or a recommendation to buy or sell securities.

---

## Project Goal

The objective is not merely to produce a chatbot.

The objective is to understand how to design and engineer a **governed, observable, testable, reliable, multi-agent AI system** on Databricks that can reason across enterprise knowledge and structured business data.

> **Business problem → Data → RAG → Tools → Agents → Orchestration → MCP → Governance → Evaluation → Production.**
