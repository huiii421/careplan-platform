# PRD: Swagger/OpenAPI for Frontend-Backend Integration

## 1. Purpose
- Build a reliable API contract layer between backend and frontend.
- Enable fast manual testing, mock generation, typed client generation, and regression checks.
- Reduce communication cost and contract mismatch bugs during multi-agent parallel work.

## 2. Why Swagger/OpenAPI Is Needed
### 2.1 Current pain points
- DRF browsable API is useful for quick manual checks, but it is not a strong contract artifact for FE collaboration.
- Frontend needs stable request/response schema and error model.
- Without a machine-readable contract, API changes can silently break FE.

### 2.2 Value
- Single source of truth: OpenAPI spec.
- Human readable docs: Swagger UI.
- Machine readable contract: JSON/YAML for codegen and contract tests.
- Better onboarding: FE, QA, and new agents can start quickly.

## 3. Scope
### In Scope
- Add OpenAPI schema generation and Swagger UI in backend.
- Standardize authentication docs, error envelope docs, and upload endpoint docs.
- Export schema artifact for CI checks and FE typed client generation.
- Create FE integration playbook and environment rules.

### Out of Scope (Phase 1)
- Full API gateway.
- Public internet exposure of Swagger in production without auth controls.

## 4. Architecture Decisions
### 4.1 Tooling choice
- Use `drf-spectacular` as OpenAPI generator.
- Use built-in Swagger UI and Redoc views.

### 4.2 Contract standard
- OpenAPI 3.x
- Keep API prefix under `/api/`
- Keep error envelope shape from S18:
```json
{
  "success": false,
  "error": {
    "code": "validation_error",
    "message": "Request data is invalid.",
    "details": {}
  }
}
```

## 5. Detailed Implementation Plan
### Step 1: Install dependencies
- Add package:
- `drf-spectacular`

### Step 2: Update Django settings
- In `REST_FRAMEWORK`:
- `DEFAULT_SCHEMA_CLASS = "drf_spectacular.openapi.AutoSchema"`
- Add `SPECTACULAR_SETTINGS`:
- Title, description, version
- `SERVE_INCLUDE_SCHEMA=False` for UI endpoint behavior
- tags and auth scheme metadata

### Step 3: Add schema and docs routes
- In `config/urls.py` add:
- `/api/schema/` for raw OpenAPI schema
- `/api/docs/swagger/` for Swagger UI
- `/api/docs/redoc/` for Redoc

### Step 4: Annotate critical endpoints
- Add `@extend_schema` and `@extend_schema_view` on:
- Patient/Provider/Case endpoints
- File upload endpoint (`POST /api/cases/{id}/records/`)
- Explicit request examples and error responses
- Mark auth requirement clearly

### Step 5: Auth and CORS strategy for FE
- Short term:
- Session auth for local manual tests
- Long term:
- Add token/JWT auth for SPA frontend
- Add CORS policy for FE local domain (for example `http://localhost:5173`)

### Step 6: Generate schema artifact in CI
- Command:
- `python manage.py spectacular --file openapi.yaml`
- Add CI check:
- schema generation must pass
- optional diff gate for breaking changes

### Step 7: Frontend typed client generation
- Options:
- `openapi-typescript`
- `orval`
- `openapi-generator-cli`
- Output:
- typed API client and models consumed by FE app

## 6. Frontend Integration Blueprint
### 6.1 FE integration flow
1. FE reads API docs at `/api/docs/swagger/`.
2. FE imports generated typed client.
3. FE handles standard error envelope once, globally.
4. FE builds forms using schema examples and validations aligned with backend.

### 6.2 Recommended FE architecture
- API layer:
- `src/api/client.ts` (HTTP base instance)
- `src/api/generated/*` (codegen output)
- Error handling:
- `src/lib/http-error.ts` parse standard envelope
- Auth:
- `src/auth/session.ts` or JWT token store

## 7. DRF Browsable API vs Swagger (Decision)
- DRF Browsable API:
- Best for backend developer quick manual testing.
- Swagger:
- Best for FE integration, contract sharing, QA, and automation.
- Decision:
- Keep both. Swagger is the contract, DRF UI is a convenience tool.

## 8. Security and Environment Rules
- Dev:
- Swagger enabled.
- Staging:
- Swagger enabled with auth.
- Prod:
- Either disabled or protected (admin/staff only, VPN, or SSO).
- Never expose sensitive example data.

## 9. Acceptance Criteria
1. `/api/schema/` returns valid OpenAPI schema.
2. `/api/docs/swagger/` is accessible in dev.
3. Core endpoints include request/response/error docs.
4. Upload endpoint shows multipart schema in docs.
5. FE can generate typed client from schema.
6. CI fails when schema generation fails.

## 10. Rollout Plan
### Phase A (1-2 days)
- Install and configure drf-spectacular.
- Add routes and basic schema output.

### Phase B (2-3 days)
- Annotate endpoints and examples.
- Add CI schema generation.

### Phase C (2-3 days)
- FE client codegen integration.
- Add contract test and breakage alerts.

## 11. Multi-Agent Execution Plan
### Agent A: Backend Docs Infrastructure
- Setup drf-spectacular, settings, routes.

### Agent B: Endpoint Annotation
- Add schema annotations for apps: patients/providers/cases/core.

### Agent C: CI and Contract Governance
- Add `openapi.yaml` generation and CI checks.

### Agent D: Frontend API Layer
- Integrate typed client generation and error handling.

### Merge policy
- A merges first.
- B and C parallel after A.
- D starts when first stable schema is available.

## 12. Risks and Mitigations
- Risk: docs drift from actual behavior.
- Mitigation: schema generation in CI + integration tests.
- Risk: breaking API changes.
- Mitigation: schema diff check and versioning policy.
- Risk: auth confusion during FE dev.
- Mitigation: explicit auth section in Swagger + sample login flow.

## 13. Deliverables
- New Swagger/OpenAPI routes in backend.
- Stable `openapi.yaml`.
- Annotated endpoints with examples and error models.
- FE typed API client integration guide.
- Updated backlog epic/stories for tracking.

