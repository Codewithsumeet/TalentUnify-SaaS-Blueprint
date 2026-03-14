<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# serach for github repo and n8n automation workflow , langflow langchain huggingface models or agents across all internet of lama and lang's for this problem statement

Here’s a curated list of ready-made building blocks (GitHub repos, n8n workflows, LangFlow/LangChain projects, and Hugging Face models) you can mine for your unified AI recruitment platform.

***

## n8n workflows for resume intake \& scoring

- **Pragnakalp – “Parse Resumes from Gmail to Google Sheets”**
Full n8n workflow: Gmail trigger → LLM classification (is this a resume?) → parse resumes (Docsaar/API) → log to Google Sheets → Slack/Telegram alerts.[^1]
Use it as a template for: Gmail ingestion, attachment handling, basic AI-based filtering, and pushing candidates into your unified DB.
- **Community workflow – Gmail → parse resumes → score → notify HR**
n8n community post where a user built: Gmail trigger → PDF parsing → scoring against required skills in code node → log to ATS sheet → send Slack notification and auto-reply to candidate.[^2]
Good pattern for: automated scoring and notifications you can adapt to your semantic search platform.
- **Official n8n template – “AI resume processing and GitHub analysis with VLM run”**
Template that monitors Gmail, parses resumes via an AI document parser (VLM Run), analyzes GitHub profiles, writes profiles to Sheets, and sends notifications.[^3]
Useful for: end-to-end candidate profile enrichment (resume + GitHub) and showing judges multi-source intelligence.

***

## LangChain / LangGraph GitHub repos for resumes \& screening

- **Resume Semantic Search with BERT** – `KarthikAlagarsamy/Resume-Semantic-Search`
Uses Hugging Face BERT embeddings + Gradio for semantic search over resumes given a job description or query.[^4]
Good for: reference implementation of semantic ranking over multiple resumes.
- **LLM-powered Resume Parser (JSON output)** – `Sajjad-Amjad/Resume-Parser`
“Get structured output (JSON) from resumes using GPT and LangChain.”[^5]
Good for: seeing how to structure parsing prompts + LangChain pipelines to emit clean JSON candidate objects.
- **Advanced Resume Parsing and Candidate Matching** – `honeyvig/Advanced-Resume-Parsing-and-Candidate-Matching`
Scope: parse resumes (PDF/Word) into structured fields, then do AI-based matching to job descriptions using BERT-style models.[^6]
Good for: full flow design from parsing → matching engine.
- **LangGraph Based Resume Screener** – `Ajithbalakrishnan/LangGraph_Based_Resume_Screener`
LangGraph + LangChain chatbot POC that does RAG over resumes and job descriptions to screen candidates.[^7]
Good for: graph-based agent flow to answer recruiter-style questions over a pool of resumes.
- **ResumeGPT – Resume Auto Analysis** – `CodingLucasLi/GPT_Resume_analysing`
Uses LangChain + OpenAI to vectorize resumes, store in Faiss, extract structured info, and generate a matching score per candidate vs a job description.[^8]
Good for: scoring logic and FAISS-based vector search design.
- **SmartHire CV with RAG** – `cv-smart-hire` repo/site (AI resume analysis for recruiters)
Streamlit app using LangChain RAG, AWS Bedrock embeddings, MongoDB Atlas vector search, and GPT for resume QA and summary.[^9]
Good for: seeing a recruiter-facing UI + RAG pipeline similar to what you’re building.
- **JobMatcher – Intelligent Job Matching System** – `Ammar-Abdelhady-ai/JobMatcher-Intelligent-Job-Matching-System`
Scrapes jobs from LinkedIn/Indeed/Bayt/Wuzzuf, summarizes CVs with transformers, and matches via cosine similarity; FastAPI + Streamlit.[^10]
Good for: ideas on JD scraping and job–candidate matching logic.
- **Resume Matcher** – `srbhr/Resume-Matcher`
Tool to improve resumes vs job descriptions with keyword suggestions and analysis.[^11]
Good for: JD–CV comparison features you can expose to recruiters.

***

## LangFlow examples \& repos

- **Official LangFlow repo** – `langflow-ai/langflow`
Visual orchestrator for LangChain-style graphs and agents.[^12][^13]
Use it as: the base platform if you want a visual builder for your RAG/agent flows.
- **ResumAI with LangFlow + Astra DB + OpenAI** (tutorial \& code)
Blog and example app: parses resume PDFs, vectorizes into Astra DB, runs vector similarity vs job descriptions, and builds a Streamlit UI, all wired via LangFlow.[^14][^15]
Good for: copying the overall architecture for your recruiter use case (swap candidate vs job perspective).
- **LangFlow MCP High ATS Resume Creator** – `Vinayaks439/LangFlow-MCP-High-ATS-Resume-creator`
LangFlow-exported JSON for a multi-agent flow that parses a user’s resume + LinkedIn job post and generates a high-ATS score resume.[^16]
Good for: seeing a complex multi-agent LangFlow design and learning from its parsing and summarization subflows.

***

## Hugging Face models / spaces for resume parsing \& job matching

These are plug-and-play components you can call via API from your backend or LangChain:

- **Agentic Resume Parser (HF Space)** – `csccorner/Agentic-Resume-Parser`
HF Space that takes PDF/DOCX resumes and outputs structured JSON (name, contact, experience, education, skills) using layout-aware transformers, NER, and zero-shot classification.[^17]
Good for: off‑the‑shelf resume → JSON service; you can replicate or wrap it in your own API.
- **Resume NER BERT v2** – `yashpwr/resume-ner-bert-v2`
BERT token-classification model fine-tuned specifically for resumes (25 entity types, ~90.9% F1) – personal info, work experience, education, skills, etc.[^18]
Good for: high-accuracy structured extraction in your own pipeline.
- **Llama-based CV–JD matching LoRA** – `LlamaFactoryAI/cv-job-description-matching`
LoRA fine-tuned Llama 3.1 model for scoring and analyzing compatibility between a CV and a job description, producing scores and detailed reasoning.[^19]
Good for: “LLama + Lang” part – agent that deeply evaluates candidate vs role.
- **JobBERT-v3** – `TechWolf/JobBERT-v3` (HF model in paper)
Contrastive model for multilingual job title matching and skill ranking; good for job-title normalization and skill suggestions.[^20]
- **spaCy Job Recommendation model** – `AventIQ-AI/spacy-job-recommendation`
HF-linked model doing resume parsing, skill extraction, and job recommendation ranking using cosine similarity and graph analysis.[^21]
- Plus general discussions and guides on resume parsers using HF/transformers (e.g., NER-based parsers, T5/Flan few-shot approaches).[^22][^23][^24]

***

## How to stitch these into your Breach hackathon build

For Team Nexus, a pragmatic combo:

- **Ingestion \& automation (n8n):**
Start from the Gmail → resume parsing → sheets/Slack workflows and replace Google Sheets with your API that writes into your unified candidate DB.[^1][^2][^3]
- **Parsing \& normalization (LangChain/HF):**
Use `Resume-Parser` + `resume-ner-bert-v2` or the Agentic Resume Parser flow as your parsing core, emitting a normalized candidate schema.[^5][^17][^18]
- **Matching \& search (LangChain / LLaMA / BERT):**
Use ResumeGPT / Resume Semantic Search / LangGraph-based screener for semantic similarity patterns, and optionally LlamaFactory’s CV–JD matching model for explainable scores.[^4][^7][^8][^19]
- **Flow orchestration (LangFlow):**
Copy ideas from ResumAI and the High-ATS LangFlow project to design a recruiter-friendly flow you can run behind your UI.[^14][^16]

If you tell me your preferred stack (Node vs Python, LangFlow vs pure code, which cloud from Student Pack), I can pick 3–4 of these and outline an exact architecture and integration plan around them.
<span style="display:none">[^25][^26][^27][^28][^29][^30]</span>

<div align="center">⁂</div>

[^1]: https://www.pragnakalp.com/n8n-workflow-automation-to-parse-resumes-from-gmail-and-store-in-google-sheets/

[^2]: https://community.n8n.io/t/i-built-an-n8n-workflow-that-parses-resumes-from-gmail-scores-candidates-automatically-and-notifies-hr-on-slack-free-ats-for-small-teams/274438

[^3]: https://n8n.io/workflows/5306-ai-resume-processing-and-github-analysis-with-vlm-run/

[^4]: https://github.com/KarthikAlagarsamy/Resume-Semantic-Search

[^5]: https://github.com/Sajjad-Amjad/Resume-Parser

[^6]: https://github.com/honeyvig/Advanced-Resume-Parsing-and-Candidate-Matching

[^7]: https://github.com/Ajithbalakrishnan/LangGraph_Based_Resume_Screener

[^8]: https://github.com/CodingLucasLi/GPT_Resume_analysing

[^9]: https://yacine-mekideche.github.io/cv-smart-hire/

[^10]: https://github.com/Ammar-Abdelhady-ai/JobMatcher-Intelligent-Job-Matching-System

[^11]: https://github.com/srbhr/Resume-Matcher

[^12]: https://github.com/langflow-ai/langflow

[^13]: https://github.com/langflow-ai

[^14]: https://www.langflow.org/blog/building-resumai-langflow-astra-db-openai

[^15]: https://www.youtube.com/watch?v=UJDZHMRHeoY

[^16]: https://github.com/Vinayaks439/LangFlow-MCP-High-ATS-Resume-creator

[^17]: https://www.c-sharpcorner.com/article/resume-parser-with-hugging-face-spaces-agenticresumeparser/

[^18]: https://huggingface.co/yashpwr/resume-ner-bert-v2

[^19]: https://huggingface.co/LlamaFactoryAI/cv-job-description-matching

[^20]: https://papers.cool/arxiv/2507.21609

[^21]: https://www.promptlayer.com/models/spacy-job-recommendation

[^22]: https://www.ijirset.com/upload/2024/march/223_Resume.pdf

[^23]: https://discuss.huggingface.co/t/is-it-possible-to-create-a-resume-parser-using-a-huggingface-model/2840

[^24]: https://stackoverflow.com/questions/79180131/how-to-parse-a-resume-with-few-shot-method-using-the-specified-models-from-huggi

[^25]: https://www.youtube.com/watch?v=1RLJLhPGFoE

[^26]: https://www.youtube.com/watch?v=muIPEPsX5FA

[^27]: https://www.youtube.com/watch?v=sQl48dsEH8A

[^28]: https://github.com/topics/ai-resume-analyzer-github

[^29]: https://www.youtube.com/watch?v=_MN8XMzhi2M

[^30]: https://openreview.net/pdf?id=NKeobAGKiA

