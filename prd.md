# Product Requirements Document (PRD): DataSync Analyst

## 1. Overview
**Product Name**: DataSync Analyst  
**Purpose**: To enable product managers (PMs) with limited data expertise to query BigQuery datasets (reads, write-offs, complaints) using natural language, visualize results, generate PRDs, and search industry regulations, mimicking Gemini’s conversational flow with direct BigQuery integration and context persistence.  
**Target Users**: Product managers at [Company Name], primarily non-technical users needing data insights.  
**Problem Statement**: PMs struggle to query complex BigQuery datasets without SQL knowledge, lack integrated tools for visualization and PRD creation, and need regulatory context for compliance-sensitive data. Existing solutions like Gemini lack direct BigQuery integration and dataset-specific knowledge.  
**Success Metrics**:
- Daily unique PRDs generated (tracked in BigQuery).
- User feedback via stars/comments in UI (implementation TBD).
- Query success rate ≥95% on sample datasets.
- Average session time for hypothesis testing and PRD creation.

## 2. Key Features
### 2.1 ASKA Workflow (Ask, See, Iterate, Run, Analyze)
- **Description**: A chat-based workflow allowing PMs to query datasets in natural language, view generated SQL with explanations, iterate, and execute queries.
- **Requirements**:
  - **Ask**: Users input queries in natural language (e.g., “Show complaints from last quarter joined with reads by account number”).
  - **See**: System generates a BigQuery SQL query with a detailed explanation (high-level logic, line-by-line breakdown, code snippets). If data type issues arise (e.g., mpan as string vs. integer), the system explains limitations and asks for clarification (e.g., “Cast mpan as integer or string?”).
  - **Iterate**: Users refine queries in natural language (e.g., “Add a filter for high-priority complaints”). System maintains context for seamless iteration.
  - **Run**: Execute query on BigQuery, showing results (top 10 rows initially, full results on request).
  - **Analyze**: Users can request visualizations or export results.
- **Technical Notes**:
  - Use LangChain.js with SQLDatabaseToolkit for BigQuery query generation.
  - Implement ReAct (Reason-Act) loop for plan-execute-review-iterate cycle (hidden from user).
  - Store session context in IndexedDB with a 7-day sliding window (e.g., retains 3 days’ context after a week’s break).

### 2.2 Dataset Integration and Knowledge Base
- **Description**: Preloaded datasets (reads, write-offs, complaints) with explanations for PMs to query effectively.
- **Requirements**:
  - Support three domains: reads (e.g., user engagement metrics), write-offs (e.g., financial adjustments), complaints (e.g., customer issues).
  - Store dataset schemas, sample queries, and usage guides in a JSON/YAML knowledge base, embedded in a vector store (e.g., FAISS) for semantic search.
  - Handle joins (e.g., on mpan or account_number), flagging potential issues like data type mismatches.
  - Allow users to query dataset usage (e.g., “How do I join reads and complaints?”) with responses including schema snippets and sample SQL.
- **Technical Notes**:
  - LLM processes schemas, sample queries, and verbal instructions to generate the knowledge base.
  - Use LangChain’s Document loaders for ingestion and RAG for retrieval.

### 2.3 Visualizations
- **Description**: Generate static charts from query results, exportable as CSV or PNG.
- **Requirements**:
  - Support Plotly charts (e.g., bar, line, pie) based on query results (e.g., time-series complaints → line chart).
  - Auto-suggest chart types but allow user overrides (e.g., “Make this a bar chart”).
  - Export options: CSV (via PapaParse) and PNG (via Plotly).
  - Maintain query context for visualization tweaks (e.g., “Change to last month’s data”).
- **Technical Notes**:
  - Use react-plotly.js for rendering in Next.js UI.
  - Cache query results in session state for visualization iterations.

### 2.4 PRD Generation
- **Description**: Generate PRDs based on user queries and session context, following a predefined process.
- **Requirements**:
  - Triggered by user request (e.g., “Create PRD for this analysis”).
  - Routes to Gemini agent, referencing a standalone PRD standards doc (provided internally).
  - Gemini asks clarifying questions in the main chat thread (e.g., “What metrics should the PRD prioritize?”).
  - Generates PRD in Markdown, with versioning (e.g., v1.1 for updates).
  - Users can resume sessions to update PRDs, leveraging 7-day context retention.
- **Technical Notes**:
  - Use LangChain’s ConversationChain for context-aware PRD generation.
  - Store PRDs in BigQuery or local JSON, with export to Markdown/PDF.

### 2.5 Regulatory Search Agent
- **Description**: Search preloaded industry regulation documents to provide compliance context.
- **Requirements**:
  - Support three initial Markdown documents (provided internally).
  - Semantic search for queries (e.g., “Regulations for complaint handling”).
  - Auto-trigger for compliance-sensitive queries (e.g., complaints dataset).
  - Cite document snippets in responses for traceability.
- **Technical Notes**:
  - Use LangChain’s Document loaders and vector store for RAG-based search.
  - Embed documents during setup, refresh as needed.

### 2.6 UI and Interaction
- **Description**: A chat-first interface mimicking Gemini, adhering to OVO design system.
- **Requirements**:
  - Chat interface for natural language queries, with buttons for “Run Query,” “Visualize,” “Create PRD.”
  - Static Plotly visualizations embedded inline.
  - Feedback form for stars/comments per session (stored in BigQuery, TBD).
  - Responsive design using OVO’s React component library (swapped in during vibe coding).
- **Technical Notes**:
  - Build with Next.js and React, using react-chat-ui or similar as placeholder.
  - Follow OVO design system guidelines (internal).

### 2.7 Security and Access
- **Description**: Secure access with Okta and BigQuery IAM integration.
- **Requirements**:
  - Okta SSO for user verification, inheriting BigQuery roles (e.g., read-only for PMs).
  - Row-level security in BigQuery for domain-specific access.
  - Audit logs for queries and PRD generation.
- **Technical Notes**:
  - Use okta-react SDK for authentication.
  - BigQuery client library for secure data access.

## 3. User Flows
1. **Querying Data**:
   - User logs in via Okta, enters chat interface.
   - Inputs natural language query (e.g., “Show complaints by region”).
   - System generates SQL, explains logic (high-level, line-by-line, snippets), and asks for clarification if needed (e.g., data type issues).
   - User iterates (e.g., “Filter for 2025”) or runs query.
   - Views results (top 10 rows, expandable).

2. **Visualizing Results**:
   - User requests visualization (e.g., “Plot complaints as a bar chart”).
   - System suggests chart type, renders static Plotly chart, offers CSV/PNG export.
   - User can tweak visualization via chat (e.g., “Change to line chart”).

3. **Creating PRD**:
   - User requests PRD (e.g., “Create PRD for complaint analysis feature”).
   - System routes to Gemini, asks clarifying questions in chat (e.g., “What’s the target audience?”).
   - Generates PRD in Markdown, saves with version, allows updates in future sessions.

4. **Regulatory Search**:
   - User queries regulations (e.g., “Rules for write-offs”).
   - System retrieves relevant document snippets, cites sources.
   - Auto-triggers for compliance-sensitive queries.

## 4. Non-Functional Requirements
- **Performance**: Query generation <5s, visualization rendering <3s, PRD generation <10s.
- **Scalability**: Handle 100 concurrent users, 1,000 daily queries (BigQuery quotas managed).
- **Availability**: Local dev initially, 99% uptime on internal PaaS later.
- **Security**: Okta SSO, BigQuery IAM, encrypted session storage.
- **Context Retention**: 7-day sliding window for chat history (IndexedDB).

## 5. Constraints
- Must use JavaScript (Next.js/React pending confirmation).
- Local development initially, deploy to internal PaaS later.
- Align with OVO design system (swapped in during vibe coding).
- Deadline: MVP by [TBD, to be specified in `plan.md`].

## 6. Assumptions
- PMs have basic familiarity with natural language queries but no SQL expertise.
- BigQuery datasets (reads, write-offs, complaints) are accessible with schemas provided.
- Three regulatory Markdown documents provided internally.
- OVO design system is React-compatible.
- Gemini API supports required functionality (chat, PRD generation).

## 7. Out of Scope (MVP)
- Dynamic visualizations (e.g., zoom/pan).
- Additional datasets beyond reads, write-offs, complaints.
- Advanced analytics (e.g., predictive modeling).
- External integrations beyond BigQuery, Okta, Gemini.

## 8. Dependencies
- **External**: Gemini API, BigQuery, Okta, Plotly, LangChain.js, react-plotly.js, PapaParse.
- **Internal**: OVO design system, PRD standards doc, dataset schemas, regulatory documents.
- **TBD**: Next.js/React confirmation, feedback implementation details.

## 9. Risks and Mitigations
- **Risk**: BigQuery query errors (e.g., data type mismatches).
  - **Mitigation**: Agent proactively flags issues, asks clarifying questions.
- **Risk**: Context loss in multi-day sessions.
  - **Mitigation**: Robust 7-day sliding context storage.
- **Risk**: Gemini API limitations for PRD generation.
  - **Mitigation**: Predefine PRD template, test with sample queries.