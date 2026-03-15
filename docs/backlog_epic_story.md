# Care Plan Backlog (Epic/Story) with Jira Templates

## 1) Epic List

1. E1 Foundation and Architecture
2. E2 Patient/Provider/Case Data Management
3. E3 Validation and Integrity Enforcement
4. E4 Duplicate Detection and Review UX
5. E5 LLM Care Plan Generation Pipeline
6. E6 Care Plan Review, Versioning, and Download
7. E7 Reporting and Export
8. E8 Security, Audit, and Error Handling
9. E9 Automated Testing and CI Readiness
10. E10 API Contract and Frontend Integration

## 2) Story Backlog Table

| Story ID | Epic | Goal | API Impact | Data Model Impact | Validation Rules | Test Cases | Dependencies | Est. | Priority | Acceptance Criteria |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | E1 | Bootstrap modular backend structure (apps/services/repositories) | Add `/health` | None | None | health endpoint test | None | S | P0 | `/health` returns 200 and structure is modular |
| S2 | E1 | Config/env hardening for local + docker | None | None | Required env checks on startup | config load/fail tests | S1 | S | P0 | Missing critical env fails with clear message |
| S3 | E2 | Create Patient CRUD with MRN uniqueness | `POST/GET /api/patients` | `Patient` table, unique `mrn` index | MRN format + required fields | patient create/read/duplicate MRN | S1,S2 | M | P0 | Duplicate MRN blocked; valid patient persists |
| S4 | E2 | Create Provider upsert-by-NPI | `POST/GET /api/providers` | `Provider` table, unique `npi` | NPI must be 10 digits | create provider, reuse on same NPI | S1,S2 | M | P0 | Same NPI never creates duplicate provider |
| S5 | E2 | Create Case/Order intake endpoint | `POST /api/cases` | `Case` table + FK to Patient/Provider | diagnosis + medication required | happy path + missing field errors | S3,S4 | M | P0 | Case created with linked patient/provider |
| S6 | E2 | Persist secondary diagnoses + medication history | expand case payload | child tables or JSON fields | list sanitation, max lengths | list parse/storage tests | S5 | S | P1 | Lists stored and returned consistently |
| S7 | E3 | Implement ICD-10 validator service | used by case endpoints | optional reference table/cache | ICD-10 pattern + dictionary check | valid/invalid ICD tests | S5 | M | P0 | Invalid ICD rejected with clear error |
| S8 | E3 | File intake for records (text/pdf) | `POST /api/cases/{id}/records` | `CaseRecord` metadata | MIME, size, empty-file checks | file accepted/rejected tests | S5 | M | P0 | Valid files saved; invalid blocked safely |
| S9 | E3 | Server-side cross-field rule engine | case create/update enforcement | optional rule config table | at least one diagnosis + medication | cross-field failure tests | S5,S7 | M | P0 | Rules enforced on all write endpoints |
| S10 | E4 | Patient duplicate warning API | `POST /api/duplicate-check/patient` | optional dedupe log table | MRN exact + demographic threshold | TP/FP dedupe tests | S3 | M | P0 | Warning returned without blocking |
| S11 | E4 | Order duplicate warning API | `POST /api/duplicate-check/order` | optional dedupe log table | patient+dx+med+window rule | recent duplicate tests | S5 | M | P0 | Duplicate-like orders flagged correctly |
| S12 | E5 | LLM prompt assembly service | internal service API | `PromptAudit` table | required context completeness | prompt contract tests | S5,S7,S8,S9 | M | P0 | Structured prompt built from case data |
| S13 | E5 | LLM generation endpoint with retries/timeouts | `POST /api/cases/{id}/generate-care-plan` | `CarePlanVersion` table | block generation on missing required data | success/timeout/retry tests | S12 | M | P0 | Draft generated or safe error returned |
| S14 | E5 | Store model metadata and traceability | none public | add model/version/token fields | metadata required on save | metadata persistence tests | S13 | S | P0 | Every generation is auditable |
| S15 | E6 | Pharmacist review/edit/finalize workflow | `PATCH /api/care-plans/{id}` | status machine fields | legal state transitions only | transition guard tests | S13 | M | P0 | Invalid transitions blocked |
| S16 | E6 | TXT download for finalized care plan | `GET /api/care-plans/{id}/download.txt` | None | finalized-only download | content + permission tests | S15 | S | P0 | Finalized plan downloadable as TXT |
| S17 | E7 | Export endpoint for reporting | `GET /api/reports/cases/export` | optional export job table | filter validation | csv export/filter tests | S5,S15 | M | P1 | Export includes required fields |
| S18 | E8 | Error envelope standardization | all endpoints | None | safe non-technical messages | error contract tests | S1 | S | P0 | Uniform error schema everywhere |
| S19 | E8 | Audit logging for critical events | optional admin audit API | `AuditLog` table | PII masking rules | log creation/masking tests | S5,S13,S15 | M | P0 | Critical events are auditable |
| S20 | E8 | Basic authz roles (assistant/pharmacist/admin) | permission checks | role mapping | role-based restrictions | permission matrix tests | S15,S19 | M | P1 | Unauthorized actions denied |
| S21 | E9 | Unit tests for validators and dedupe | none | none | validator and dedupe rules | unit test suite | S7,S9,S10,S11 | M | P0 | Core logic coverage target met |
| S22 | E9 | Integration tests for E2E flow | none | none | E2E assertion set | intake->generate->finalize->download | S3..S16 | M | P0 | Full happy path passes in CI |
| S23 | E9 | CI pipeline with quality gates | none | none | lint/test gate | CI workflow tests | S21,S22 | S | P1 | PR blocked when critical tests fail |
| S24 | E10 | Integrate OpenAPI schema generation (drf-spectacular) | add `/api/schema` and docs URLs | none | schema must build without errors | schema generation tests | S1,S18 | S | P0 | OpenAPI schema and Swagger UI available in dev |
| S25 | E10 | Annotate core endpoints with request/response/error examples | no new business endpoint | none | docs include auth and error envelope | endpoint schema snapshot tests | S24,S3,S4,S5,S8 | M | P0 | Patients/Providers/Cases/Records documented with examples |
| S26 | E10 | Add API versioning and contract governance rules | optional headers/version field | none | breaking changes must be flagged | schema diff checks | S24,S25 | M | P1 | Contract changes are reviewed and tracked |
| S27 | E10 | Add frontend-friendly auth and CORS policy for local integration | auth endpoints/config behavior | none | origin allowlist and auth rules | CORS/auth integration tests | S2,S24 | M | P0 | FE dev server can call backend securely |
| S28 | E10 | Generate typed frontend API client from OpenAPI | none public | none | generated types must match schema | type generation CI test | S25 | S | P1 | FE can consume typed API client without manual DTO drift |
| S29 | E10 | Add OpenAPI build check to CI quality gates | none | none | schema generation required in CI | CI workflow tests for schema | S23,S24 | S | P0 | PR fails when OpenAPI generation fails |

## 3) Sprint 1 Proposal (P0 Only)

### Scope

S1, S2, S3, S4, S5, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S18, S19, S21, S22

### Sequence

1. Phase 1: S1, S2, S18
2. Phase 2: S3, S4, S5
3. Phase 3: S7, S8, S9
4. Phase 4: S10, S11
5. Phase 5: S12, S13, S14
6. Phase 6: S15, S16, S19
7. Phase 7: S21, S22
8. Phase 8: S24, S25, S27, S29 (Swagger + FE contract baseline)
9. Phase 9: S26, S28 (contract governance + typed client)

### Parallelization

1. Track A: S3/S4/S5 (core entities and intake)
2. Track B: S7/S8/S9 (validation and records)
3. Track C: S10/S11 (duplicate detection)
4. Track D: S12/S13/S14 (LLM generation)
5. Track E: S21/S22 (tests) starts as soon as upstream stories land
6. Track F: S24/S25/S27/S29 (API contract and frontend integration)
7. Track G: S26/S28 (contract governance and FE codegen)

## 4) Risks and Open Questions

1. MRN rule conflict: requirement says 6 digits, sample shows 8 digits (`00012345`).
2. ICD-10 source of truth: regex-only vs dictionary/API.
3. LLM latency and retry behavior for clinical workflow SLAs.
4. PHI/PII masking policy boundaries for logs and exports.
5. Role/permission granularity not fully finalized.
6. Export format priority: CSV only vs CSV + XLSX in phase 1.
7. Patient record storage retention and deletion policy pending.
8. API versioning strategy for FE compatibility: URL versioning vs header-based.
9. Swagger availability policy in production: disabled vs protected internal access.

## 5) Jira Templates (Copy/Paste Ready)

### 5.1 Epic Template

Use this when creating an Epic in Jira.

```text
Issue Type: Epic
Summary: [EPIC-ID] [Epic Name]
Epic Name: [Epic Name]
Description:
Background:
- [Why this epic exists]

Scope:
- [In-scope item 1]
- [In-scope item 2]

Out of Scope:
- [Out-of-scope item 1]

Business Value:
- [Compliance/efficiency/revenue impact]

Success Metrics:
- [Metric 1 + target]
- [Metric 2 + target]

Dependencies:
- [Dependency 1]

Risks:
- [Risk 1 + mitigation]

Acceptance Criteria:
- [AC 1]
- [AC 2]
```

### 5.2 Story Template

Use this when creating a Story in Jira.

```text
Issue Type: Story
Summary: [STORY-ID] [Short action-oriented title]
Epic Link: [EPIC-ID]
Priority: [P0/P1/P2]
Estimate: [S/M/L]
Labels: careplan, api, backend

User Story:
As a [role],
I want [capability],
So that [outcome].

Goal:
- [Concrete goal statement]

API Impact:
- Endpoint(s): [e.g., POST /api/cases]
- Request schema changes: [yes/no + detail]
- Response schema changes: [yes/no + detail]
- Error codes: [list]

Data Model Impact:
- Table/Model: [name]
- Fields: [new/updated]
- Constraints/Indexes: [unique, FK, index]
- Migration needed: [yes/no]

Validation Rules:
- [Rule 1]
- [Rule 2]

Dependencies:
- [Story IDs]

Test Cases:
- Unit: [list]
- Integration: [list]
- Negative cases: [list]

Acceptance Criteria:
1. [AC 1]
2. [AC 2]
3. [AC 3]

Definition of Done:
- Code complete
- Tests added and passing
- API docs updated
- Reviewed and merged
```

### 5.3 Sub-task Template

```text
Issue Type: Sub-task
Summary: [STORY-ID] [Implementation slice]
Parent: [STORY-ID]
Description:
- Scope:
  - [item]
- Files/Modules:
  - [path]
- Done when:
  - [condition]
```

## 6) Jira-Ready Examples

### Example Epic

```text
Issue Type: Epic
Summary: [E5] LLM Care Plan Generation Pipeline
Epic Name: LLM Care Plan Generation Pipeline
Description:
Background:
- Automate care plan draft creation from validated clinical inputs to reduce pharmacist documentation time.

Scope:
- Prompt assembly from structured case data
- LLM generation endpoint with retry/timeout handling
- Audit metadata persistence

Out of Scope:
- PDF rendering in phase 1

Business Value:
- Reduce manual documentation burden and compliance backlog.

Success Metrics:
- >=90% generation success rate
- p95 generation latency < 30s

Dependencies:
- S5, S7, S8, S9

Risks:
- External LLM latency variability; mitigate with retries and timeout policy.

Acceptance Criteria:
- Draft generation works for valid case input.
- Failures return safe actionable errors without data loss.
```

### Example Story

```text
Issue Type: Story
Summary: [S4] Provider upsert by NPI with uniqueness guarantee
Epic Link: E2
Priority: P0
Estimate: M
Labels: careplan, api, backend, provider

User Story:
As a medical assistant,
I want provider records to be reused by NPI,
So that duplicate provider entries are prevented.

Goal:
- Ensure one provider record per unique 10-digit NPI.

API Impact:
- Endpoint(s): POST /api/providers, GET /api/providers/{id}
- Request schema changes: provider_name, npi
- Response schema changes: provider id and canonical info
- Error codes: 400 (invalid NPI), 409 (conflict edge-case)

Data Model Impact:
- Table/Model: Provider
- Fields: name, npi
- Constraints/Indexes: unique index on npi
- Migration needed: yes

Validation Rules:
- NPI must be exactly 10 digits.
- Name cannot be blank.

Dependencies:
- S1, S2

Test Cases:
- Unit: NPI validator
- Integration: create provider then re-submit same NPI returns existing
- Negative: invalid NPI rejected

Acceptance Criteria:
1. Submitting existing NPI never creates a second provider.
2. Invalid NPI returns clear validation message.
3. Unique index enforces consistency under concurrent requests.

Definition of Done:
- Code complete
- Tests added and passing
- API docs updated
- Reviewed and merged
```
