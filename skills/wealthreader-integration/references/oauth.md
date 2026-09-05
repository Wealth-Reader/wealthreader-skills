# Redirect authentication

Source: [Public OAuth guide](https://www.wealthreader.com/docs/en/oauth-integration-backend/). Checked 2026-09-05. Use for redirect/native onboarding; this is not a generic OAuth SDK recipe.

## Documented wire contract

Register the exact return URL as `domain`, `url_callback`, and later `redirect_uri`, with `access_type=oauth`; registration can use the client area.

Generate three independent cryptographically random 41-character alphanumeric strings. Hex-encode each to create 82-character `nonce`, `state`, and `code_verifier`. Persist them keyed by `nonce`. Compute `challenge_code` as the hexadecimal SHA-256 digest of the encoded verifier. Encode the widget configuration JSON as hexadecimal separately.

Redirect to `https://oauth.wealthreader.com/oauth2/` with URL-encoded query fields:

| Field | Value |
| --- | --- |
| `challenge_code` | Digest above; not `code_challenge` |
| `code_challenge_method` | `S256` |
| `redirect_uri` | Registered return URL |
| `response_type` | `code` |
| `state`, `nonce` | Generated values |
| `wr_conf` | Hex-encoded configuration |

The return GET documents `nonce` and `code`. Recover the verifier using a known nonce. Exchange server-side at `POST https://oauth.wealthreader.com/token/`, form-encoded with `grant_type=authorization_code`, identical `redirect_uri`, returned `code`, and stored `code_verifier`.

The response is financial JSON (`success`, `payload`, `statistics`), not a conventional access-token response. Store aggregation `statistics.token` and `statistics.code` for later reads.

## Application security and unresolved contract

Recommended application controls: bind pending challenges to the initiating user/session, expire them, and reject replay atomically. Keep the verifier server-side. Unknown nonces must not recover another user's connection.

The public return example does not document an echoed `state`; do not claim state validation is implemented by reading a nonexistent field. Verify provider behavior and agree on the production CSRF/session-binding design. Do not silently substitute standard base64url PKCE: its encoding and parameter names differ from this documented flow.

Test encodings and callback rejection locally before requesting any live exchange. Mock responses must not suggest that a missing production security contract has been validated.
