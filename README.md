# Nexa

## AI-Powered Natural Language Data Analyst

Nexa is an AI-powered data intelligence platform that turns natural-language business questions into safe, executable SQL queries over structured company data.

Instead of requiring users to understand database schemas or SQL, Nexa uses a semantic layer to understand the meaning of datasets and columns, retrieve the relevant business concepts, plan the query, generate SQL, validate it, and optionally execute it against the database.

---

## What Nexa Does

A user can ask a question such as:

> Show the total revenue by country.

Nexa processes the request through the following flow:

```
Natural-language question
        ↓
Query Understanding
        ↓
Semantic Retrieval
        ↓
JEV Selection
        ↓
Semantic Resolution
        ↓
Query Planning
        ↓
Join Planning
        ↓
Execution Planning
        ↓
SQL Generation
        ↓
SQL Validation
        ↓
SQL Execution
        ↓
Result
```

The goal is to make database analysis accessible through natural language while keeping the generated SQL grounded in the approved semantic model and actual database schema.

---

## Architecture

Nexa currently has two major pipelines.

### 1. Data & Semantic Preparation Pipeline

The preparation pipeline converts raw CSV datasets into a structured semantic representation.

```
CSV datasets
    ↓
Generic CSV ingestion
    ↓
Dataset profiling
    ↓
SQLite data loading
    ↓
Semantic interpretation
    ↓
Semantic registry
    ↓
Human approval
    ↓
Relationship discovery
    ↓
Relationship interpretation
    ↓
Human approval
    ↓
Registry persistence
    ↓
Semantic embedding generation
    ↓
Semantic catalog
```

### 2. Natural Language Query Pipeline

The query pipeline converts a natural-language question into validated SQL and can optionally execute it.

```
User question
    ↓
Query Understanding
    ↓
Semantic Retrieval
    ↓
JEV Selection
    ↓
Semantic Resolution
    ↓
Query Planning
    ↓
Join Planning
    ↓
Execution Planning
    ↓
SQL Generation
    ↓
SQL Validation
    ↓
Optional SQL Execution
```

---

## Semantic Layer

A core part of Nexa is its semantic layer.

Instead of relying only on raw database column names, Nexa creates semantic interpretations for columns and datasets.

For example:

```
source column:
    revenue

approved meaning:
    Revenue generated from a customer transaction
```

These approved meanings form the semantic knowledge used during natural-language query retrieval.

### Semantic Registry

The registry stores:

- Dataset information
- Column semantic interpretations
- Semantic IDs
- Confidence scores
- Evidence
- Approval status
- Discovered relationships
- Relationship confidence and evidence

Only approved semantic interpretations are used for semantic retrieval.

---

## Semantic Embeddings

Nexa uses Jina embeddings for semantic retrieval.

Approved column meanings are embedded during the ingestion process and stored in SQLite.

```
Approved semantic meaning
        ↓
Jina Embeddings
        ↓
semantic_embeddings table
        ↓
Stored vector
```

At query time, Nexa embeds only the user's relevant query phrase and compares it against the precomputed semantic vectors.

This avoids repeatedly generating embeddings for every catalog entry on every query.

### Retrieval Flow

```
User query
    ↓
Query understanding
    ↓
Query phrase embedding
    ↓
Precomputed semantic embeddings
    ↓
Cosine similarity
    ↓
Top semantic candidates
    ↓
JEV selection
```

---

## Database

Nexa currently uses SQLite for persistence.

The database stores:

- Dataset metadata
- Column metadata
- Semantic registry information
- Discovered relationships
- Precomputed semantic embeddings
- The ingested datasets themselves

The internal `semantic_embeddings` table is treated as metadata and is excluded from the schema exposed to SQL generation.

---

## SQL Safety

Generated SQL is not executed immediately.

Nexa first validates the generated SQL against the known database schema and execution plan.

The validation layer checks things such as:

- SQL is present and valid
- Only a single statement is allowed
- The statement is a `SELECT`
- Destructive SQL operations are rejected
- Referenced tables exist
- Referenced columns exist
- Planned datasets and columns are represented
- Planned joins are represented
- Planned metrics and dimensions are represented

Only validated SQL can reach the execution layer.

---

## Example

Question:

```text
Show the total revenue by country.
```

Generated SQL:

```sql
SELECT cf.country,
       SUM(cf.revenue) AS total_revenue
FROM customer_features cf
GROUP BY cf.country;
```

The query can then be validated and optionally executed against the SQLite database.

Example result:

```text
Australia       6990.0
Canada          8157.0
Germany         7722.0
India           50019.0
Singapore       3800.0
United Kingdom  11574.0
United States   32355.0
```

---

## Current Datasets

The current development dataset contains:

- `customers`
- `customer_features`
- `customer_feedback`
- `product_activity`
- `sales_leads`
- `support_tickets`
- `transactions`

Nexa is designed around generic CSV ingestion rather than hard-coding the query system to a single dataset.

---

## Project Structure

The project is organized around separate data, semantic, query, LLM, and embedding components.

```
src/
├── data/
│   ├── ingestion/
│   ├── profiling/
│   ├── database/
│   └── semantic/
│
├── embeddings/
│   └── models/
│
├── llm/
│   └── schemas/
│
├── query/
│   ├── understanding/
│   ├── retrieval/
│   ├── resolution/
│   ├── planning/
│   └── sql/
│
└── jev/
```

---

## Key Components

### Data Layer

Responsible for:

- CSV ingestion
- Dataset profiling
- Loading data into SQLite
- Database schema introspection
- Registry persistence
- Embedding persistence

### Semantic Layer

Responsible for:

- Semantic interpretation
- Semantic registry construction
- Relationship discovery
- Human approval
- Semantic catalog construction
- Embedding generation

### Query Layer

Responsible for:

- Query understanding
- Semantic retrieval
- JEV selection
- Semantic resolution
- Query planning
- Join planning
- Execution planning
- SQL generation
- SQL validation
- SQL execution

### LLM Layer

LLMs are used for tasks that require language understanding or structured reasoning, while deterministic components handle database planning, validation, and execution.

---

## Development Principles

Nexa is being developed incrementally with an emphasis on:

1. Semantic grounding
2. Human approval of semantic interpretations
3. Separation between language understanding and deterministic database operations
4. Safe SQL generation
5. Schema-aware validation
6. Reusable precomputed semantic embeddings
7. Testable individual components
8. End-to-end pipeline validation

---

## Current Status

🚧 **Active development**

The current implementation includes:

- Generic CSV ingestion
- Dataset profiling
- SQLite persistence
- Semantic registry
- Human approval flow
- Relationship discovery
- Semantic catalog
- Precomputed semantic embeddings
- Semantic retrieval
- JEV selection
- Query planning
- Join planning
- Execution planning
- SQL generation
- SQL validation
- SQL execution
- End-to-end query pipeline

The current focus is improving the reliability, performance, and intelligence of the natural-language-to-SQL system before expanding into broader AI analyst capabilities.

---

## Development Roadmap

The broader Nexa roadmap is being developed incrementally:

1. Data and semantic foundation
2. Natural-language analytics
3. Classical machine learning
4. NLP capabilities
5. Deep learning
6. Advanced semantic search
7. Retrieval-Augmented Generation
8. AI Analyst
9. Backend and API
10. Frontend
11. Integrations
12. Evaluation and monitoring
13. Deployment

---

## Vision

The long-term goal of Nexa is to become an AI analyst that can understand a company's data, answer business questions, investigate patterns, explain results, and eventually support deeper analytical workflows.

The foundation is a reliable semantic layer that connects natural language with real business data.
