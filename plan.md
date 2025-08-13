# Development Plan: DataSync Analyst

## 1. Overview
This development plan outlines the vibe coding approach for DataSync Analyst, a solo LLM-driven project using JavaScript (Next.js/React assumed, pending confirmation), LangChain.js, and BigQuery. It emphasizes a super lightweight MVP with tight iterations, building and testing features incrementally to meet the PRD requirements (artifact_id: 5286925d-5984-466f-99d8-0d90bd74a479). Each iteration delivers a testable feature, with comprehensive unit, integration, and end-to-end (E2E) testing to ensure stability.

## 2. Development Approach
- **Vibe Coding**: Solo development using LLM (e.g., via VSCode plugins like Cursor or GitHub Copilot) for code generation, debugging, and reviews. LLM prompts will be used for code, tests, and documentation.
- **Environments**:
  - **Dev**: Local Node.js setup with Docker for BigQuery emulator and IndexedDB for session storage (7-day sliding context window).
  - **Test**: Local testing with Jest (unit/integration) and Cypress (E2E).
  - **Prod**: Local initially, deploy to internal PaaS post-MVP (TBD).
- **Testing**:
  - Unit tests: Cover core functions (e.g., query generation, context storage).
  - Integration tests: Validate feature flows (e.g., ASKA query cycle).
  - E2E tests: Simulate user journeys (e.g., login → query → result).
  - Live testing: Run sample queries after each iteration using provided dataset schemas.
- **CI/CD**: GitHub Actions for automated testing (local initially).
- **Iteration Cycle**: Each iteration (1-2 days) delivers a feature, tests, and documentation, with LLM-driven code reviews to catch errors early.

## 3. Milestones and Iterations
### Phase 1: Super Lightweight MVP (Basic ASKA for Reads Dataset)
**Goal**: Enable natural language querying for the reads dataset with minimal UI and BigQuery integration.  
**Duration**: 5-7 days (assuming 1-2 days per iteration).  
**Iterations**:
1. **Iteration 1: Setup and Authentication (1-2 days)**  
   - **Feature**: Local Next.js app with Okta SSO and basic chat UI.  
   - **Tasks**:  
     - Scaffold Next.js project with React.  
     - Integrate okta-react SDK for SSO, inheriting BigQuery IAM roles.  
     - Create placeholder chat UI (react-chat-ui or basic input/output).  
     - LLM Prompt: “Generate a Next.js app with Okta SSO and a simple chat interface.”  
   - **Test Cases**:  
     - Unit: Okta auth redirects correctly.  
     - E2E: User logs in, sees chat input.  
   - **Deliverables**: Runnable app with login and empty chat UI.  
2. **Iteration 2: Basic Query Generation (1-2 days)**  
   - **Feature**: Translate natural language queries to BigQuery SQL for reads dataset.  
   - **Tasks**:  
     - Integrate LangChain.js with SQLDatabaseToolkit and BigQuery client.  
     - Process provided reads schema (internal) into a JSON knowledge base.  
     - Generate SQL for simple queries (e.g., “Show reads by user”).  
     - LLM Prompt: “Given a BigQuery schema [insert schema], generate SQL for [user query] with a JSON structure: {sql: string, explanation: {high_level: string, line_by_line: string[]}}.”  
   - **Test Cases**:  
     - Unit: SQL generation for 5 sample queries.  
     - Integration: Query executes on BigQuery emulator, returns results.  
   - **Deliverables**: Query agent for reads dataset, JSON knowledge base.  
3. **Iteration 3: Query Explanation and Results (1-2 days)**  
   - **Feature**: Display SQL with detailed explanation and query results.  
   - **Tasks**:  
     - Enhance agent to output high-level logic, line-by-line breakdown, and snippets.  
     - Show top 10 rows of results in chat UI.  
     - LLM Prompt: “For SQL [insert query], generate explanation: high-level logic, line-by-line breakdown, and Python pandas equivalent snippet.”  
   - **Test Cases**:  
     - Unit: Explanations cover all query components.  
     - E2E: User inputs query, sees SQL, explanation, and results.  
   - **Deliverables**: ASKA “Ask” and “See” steps for reads dataset.  
4. **Iteration 4: Context Persistence (1-2 days)**  
   - **Feature**: Store chat history for 7-day sliding window.  
   - **Tasks**:  
     - Implement IndexedDB for session storage (keyed by Okta user ID).  
     - Retain query context for iteration (e.g., “Add filter for 2025”).  
     - LLM Prompt: “Generate IndexedDB schema and queries for storing chat history with a 7-day sliding window.”  
   - **Test Cases**:  
     - Unit: Context persists across mock sessions.  
     - Integration: User resumes session, iterates on previous query.  
   - **Deliverables**: Persistent chat context.  

**MVP Success Criteria**:  
- Query success rate ≥95% for 10 sample read queries.  
- User can log in, query reads dataset, see explanation/results, and resume session within 7 days.  
- Tests cover 90% of code (Jest/Cypress).

### Phase 2: Incremental Feature Additions
**Goal**: Add iteration, visualization, additional datasets, PRD generation, and regulatory search.  
**Duration**: 3-4 weeks (1-2 days per iteration).  
**Iterations**:  
5. **Iteration 5: Query Iteration (1-2 days)**  
   - **Feature**: Allow users to refine queries in natural language.  
   - **Tasks**:  
     - Implement LangChain ReAct loop for iteration (plan-execute-review-iterate).  
     - Handle data type issues (e.g., “Cast mpan as integer or string?” with limitations).  
     - LLM Prompt: “Given query history [insert context], refine SQL for [new user input].”  
   - **Test Cases**:  
     - Integration: 5 iterative queries succeed (e.g., add filters, joins).  
     - E2E: User iterates query, sees updated results.  
6. **Iteration 6: Visualizations (1-2 days)**  
   - **Feature**: Static Plotly charts with CSV/PNG export.  
   - **Tasks**:  
     - Integrate react-plotly.js for bar/line/pie charts.  
     - Auto-suggest chart types based on results.  
     - Add export via PapaParse (CSV) and Plotly (PNG).  
     - LLM Prompt: “Generate Plotly.js code for [query results] with chart type suggestion.”  
   - **Test Cases**:  
     - Unit: Charts render for 5 sample results.  
     - E2E: User requests chart, exports CSV/PNG.  
7. **Iteration 7: Write-offs Dataset (1-2 days)**  
   - **Feature**: Extend ASKA to write-offs dataset.  
   - **Tasks**:  
     - Process write-offs schema into knowledge base.  
     - Support joins (e.g., on account_number).  
     - LLM Prompt: Same as Iteration 2 for write-offs.  
   - **Test Cases**:  
     - Integration: Queries succeed for write-offs, including joins with reads.  
     - E2E: User queries write-offs, sees results.  
8. **Iteration 8: Complaints Dataset (1-2 days)**  
   - **Feature**: Extend ASKA to complaints dataset.  
   - **Tasks**: Same as Iteration 7 for complaints.  
   - **Test Cases**: Same as Iteration 7, including joins (e.g., on mpan).  
9. **Iteration 9: Regulatory Search (1-2 days)**  
   - **Feature**: Semantic search for three regulatory Markdown documents.  
   - **Tasks**:  
     - Use LangChain Document loaders to embed documents in vector store (FAISS).  
     - Support queries (e.g., “Rules for complaints”).  
     - Auto-trigger for compliance-sensitive queries.  
     - LLM Prompt: “Embed [Markdown doc] into FAISS and generate search function for [query].”  
   - **Test Cases**:  
     - Unit: Search returns relevant snippets with citations.  
     - E2E: User queries regs, sees cited response.  
10. **Iteration 10: PRD Generation (1-2 days)**  
    - **Feature**: Generate PRDs via Gemini API.  
    - **Tasks**:  
      - Route PRD requests to Gemini with chat history and PRD standards doc (internal).  
      - Interleave clarifying questions in chat.  
      - Save PRDs in IndexedDB with versioning.  
      - LLM Prompt: “Using [PRD standards], generate Markdown PRD for [user request] with clarifying questions.”  
    - **Test Cases**:  
      - Integration: PRD matches standards, includes clarifications.  
      - E2E: User generates PRD, updates it in new session.  
11. **Iteration 11: Feedback Form (1-2 days)**  
    - **Feature**: Stars/comments form for user feedback.  
    - **Tasks**:  
      - Add form to UI (stars 1-5, text input).  
      - Store feedback in BigQuery.  
      - LLM Prompt: “Generate React form for stars/comments, with BigQuery storage.”  
    - **Test Cases**:  
      - Unit: Feedback saves correctly.  
      - E2E: User submits feedback, sees confirmation.  
12. **Iteration 12: OVO Design System (1-2 days)**  
    - **Feature**: Swap placeholder UI with OVO design system components.  
    - **Tasks**:  
      - Replace react-chat-ui with OVO React library (internal).  
      - Ensure UI consistency.  
      - LLM Prompt: “Adapt [React UI code] to use [OVO component placeholders].”  
    - **Test Cases**:  
      - E2E: UI renders correctly with OVO components.  

**Phase 2 Success Criteria**:  
- Full ASKA workflow for all datasets, with visualizations, PRD generation, and regulatory search.  
- Tests cover 95% of code (unit), 80% E2E.  
- Feedback logged for analysis.

### Phase 3: Deployment and Polish
**Goal**: Deploy to internal PaaS, finalize metrics.  
**Duration**: 3-5 days.  
**Iterations**:  
13. **Iteration 13: PaaS Deployment (2-3 days)**  
    - **Feature**: Deploy to internal PaaS.  
    - **Tasks**:  
      - Configure PaaS environment (TBD).  
      - Add audit logs for queries/PRDs.  
      - LLM Prompt: “Generate PaaS config for [Next.js app] with BigQuery/Okta.”  
    - **Test Cases**:  
      - E2E: App runs on PaaS with 99% uptime.  
14. **Iteration 14: Metrics and Polish (1-2 days)**  
    - **Feature**: Track daily unique PRDs, finalize feedback.  
    - **Tasks**:  
      - Log PRD generation to BigQuery.  
      - Analyze feedback (stars/comments, TBD).  
      - LLM Prompt: “Generate BigQuery schema for PRD metrics and feedback analysis.”  
    - **Test Cases**:  
      - Integration: Metrics logged correctly.  
      - E2E: Feedback analytics queryable.

## 4. Dataset Processing Guidance
- **Input**: Schemas, sample queries, verbal instructions (provided internally).  
- **LLM Prompt for Knowledge Base**:  
  ```
  Given BigQuery schema [insert schema], sample queries [insert queries], and verbal instructions [insert instructions] for [reads/write-offs/complaints], generate a JSON file:
  - Schema: {tables: [{name, columns: [{name, type}]}]}.
  - Joins: [{columns, datasets, notes}].
  - Usage: [tips, e.g., "Cast mpan as string to avoid nulls"].
  - Samples: [{query, explanation}].
  Embeddable in FAISS for semantic search.
  ```
- **LLM Prompt for Query Generation**:  
  ```
  Translate [user query] into BigQuery SQL using [knowledge base JSON].
  Output:
  - SQL: [query string].
  - Explanation: {high_level: string, line_by_line: string[], snippets: string[]}.
  - If data type issue (e.g., mpan), ask: "Cast as [type]? [Type] may [limitation]."
  ```

## 5. Dependencies
- **External**: Next.js, React, LangChain.js, BigQuery client, react-plotly.js, PapaParse, okta-react, IndexedDB, FAISS, Gemini API.  
- **Internal**: OVO design system, PRD standards doc, dataset schemas, three regulatory Markdown docs.  
- **LLM**: Gemini for chat, PRD generation, code assistance.

## 6. Risks and Mitigations
- **Risk**: LLM code errors in vibe coding.  
  - **Mitigation**: Test-driven development, LLM code reviews per iteration.  
- **Risk**: BigQuery query costs.  
  - **Mitigation**: Preview results (top 10 rows), set quotas.  
- **Risk**: Context storage overflow.  
  - **Mitigation**: Limit 7-day window to 100 queries/session.  

## 7. Timeline
- **MVP (Phase 1)**: 5-7 days (start August 12, 2025).  
- **Full Product (Phase 2)**: 3-4 weeks (by mid-September 2025).  
- **Deployment (Phase 3)**: 3-5 days (by late September 2025).  
- **Note**: Assumes 4-6 hours daily vibe coding; adjust based on pace.