# Feature: Staff login

## Outcome

Protect the local lead dashboard so only staff with configured demo credentials can view student
leads and conversation history.

## Acceptance criteria

- [ ] Anonymous users are redirected to `/login`; lead list and detail are protected.
- [ ] Correct configured credentials establish a signed session; invalid credentials do not.
- [ ] Logout clears the session; missing auth configuration leaves protected pages inaccessible.
- [ ] Session cookie is HTTP-only, SameSite=Lax, and secure when configured for HTTPS.

## Dependencies and decisions

- Dependencies: FastAPI settings and dashboard routes.
- Decisions: `docs/DECISIONS.md` #8. Single staff credential pair; no user management.

## Implementation slices

- [ ] Add configuration and signed-session middleware.
- [ ] Add login/logout routes and templates; protect dashboard pages.
- [ ] Add app-client tests and setup documentation.

## Verification

- [ ] `uv run pytest tests/test_app.py`
- [ ] Full quality gate: `bash scripts/verify.sh`

## Risks and limitations

- Single-operator credentials and local SQLite sessions are hackathon-demo controls, not production
  identity management or an authorization system.
