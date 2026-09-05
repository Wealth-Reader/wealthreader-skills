---
name: wealthreader-integration
description: Integrate or troubleshoot WealthReader financial aggregation using its widget, backend callbacks, redirect authentication, and token-based refresh. Use for applications consuming WealthReader, not bank-connector implementation or payment initiation.
---

# WealthReader integration

Build the requested integration in the application's existing stack. Use public provider contracts, not assumptions from similarly named banking or OAuth APIs.

## Start with the relevant flow

- Embedded web onboarding: read [Widget and callback](references/widget.md).
- Scheduled refresh, data mapping, or failed reads: read [Refresh and errors](references/refresh.md).
- Native application or redirect onboarding: read [Redirect authentication](references/oauth.md).

Check the selected reference's public sources before generating contract-sensitive code. The references were checked on 2026-09-05; they are navigation aids, not a frozen API specification. If a source cannot be fetched, name the unverified detail and avoid silently filling it in. Report conflicting contracts rather than choosing whichever is easiest to implement.

Confirm only missing product choices that change implementation: embedding versus redirect, desired products/history, and whether recurring refresh is needed. Do not require private WealthReader source code, internal tooling, HAR captures, or a specific framework.

## Protect the integration boundary

These are integration recommendations, not claims of undocumented provider features:

- Keep the client API key and stored refresh tokens in server-side secret storage. Do not request secrets in chat or place them in frontend configuration, logs, fixtures, URLs, or commits. The documented widget reauthentication token is a deliberate, narrowly scoped exception: expose it only to its authorized user's flow.
- Bind each pending operation to the authenticated application user before opening authentication. Enforce tenant ownership when displaying results or refreshing a connection. A random operation identifier provides correlation, not callback authentication.
- Do not invent callback signature headers, shared secrets, source-IP ranges, retry schedules, or token lifetimes. Resolve undocumented production controls with WealthReader support before treating a callback as trusted.
- Use synthetic data in generated fixtures. Never forward real callback bodies to public request-inspection services.
- Code generation does not authorize domain registration, live banking reads, or deployment. Ask before actions involving credentials, external state, real accounts, or potential charges.

## Verify behavior, not only syntax

Use local mocks first; adapt the checks to the selected flow:

- Unknown message origins and unrelated windows cannot complete widget operations.
- Backend persistence failure cannot acknowledge success; duplicate callbacks cannot duplicate records.
- Unknown operation IDs and cross-user reads are rejected; missing optional product arrays are handled.
- Invalid credentials do not enter a retry loop; reauthentication has an explicit user path.
- Redirect challenges match the documented encoding; unknown, expired, or consumed pending sessions are rejected.

Separate checks actually executed from proposed provider tests. Finish with changed files, verified scenarios, and remaining configuration or documentation blockers. A passing local test is not proof that a live bank connection works.
