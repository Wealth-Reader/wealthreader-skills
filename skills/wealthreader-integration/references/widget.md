# Widget and callback

Provider contracts: [Frontend](https://www.wealthreader.com/docs/en/iframe-integration-1-of-2-frontend/), [Backend](https://www.wealthreader.com/docs/en/iframe-integration-2-of-2-backend/), [Flow](https://www.wealthreader.com/docs/en/flow/). Checked 2026-09-05.

## Browser

Authorize the frontend domain and associate its callback and API key in the client area. Keep the API key off the page.

Minimal embedding structure (add application-specific handlers and operation ownership):

```html
<script>
  const wr_conf = {
    operation_id: crypto.randomUUID(),
    entities_to_display: [],
    wait_full_response: true
  };
</script>
<iframe id="wr-iframe" title="WealthReader connection"
  width="100%" referrerpolicy="origin"></iframe>
<script src="https://widget.wealthreader.com/js/load.js"></script>
```

Define `wr_conf` before loading the script; preserve its browser-global visibility when adapting modules or frameworks. The loader sizes the iframe to the viewport, so provide sufficient room.

Install the message listener before loading the widget. Check `event.origin` against `https://widget.wealthreader.com`; additionally check `event.source` against the iframe's `contentWindow`. Handle the exact string `flow completed` separately from JSON-string errors. Ignore malformed or unrelated messages.

Empty `entities_to_display` shows permitted institutions. Keep `wait_full_response: true` for transactions; `false` returns products only. Set `date_from` explicitly when history matters: omission means yesterday, not full history. Long ranges may require extra authentication. Consult the frontend source for other filters rather than guessing names.

## Server

Accept HTTPS JSON POST callbacks. The envelope matches the aggregation response: `success`, `payload`, and `statistics`. Read these nested fields:

| Field under `statistics` | Use |
| --- | --- |
| `operation_id` | Correlation and idempotency |
| `token` | Subsequent reads when tokenization is enabled |
| `code` | Institution identifier |
| `SESSION` | Support diagnostics |
| `warnings` | Non-fatal read caveats |

Persist required results before returning HTTP 200 with `{"status":"ok"}`. Other acknowledgments prevent frontend completion. Product keys depend on requested types and actual holdings; do not assume every array exists.

The callback precedes `flow completed`; the browser message contains no financial payload. Authentication challenges and login errors are handled in the widget, not mistaken for callback success.

Provider test usernames, with any password: `MOCKDATA` for success, `MOCKOTP` for a challenge, `MOCKLOGINKO` for login failure without a callback. These are provider simulations, not an offline sandbox; obtain authorization before running them.

## Production gate

The public guide does not specify callback authentication or delivery retry guarantees. The `operation_id` is visible to the browser and must not be treated as a secret. Request the supported authenticity mechanism from WealthReader; leave production acceptance explicitly blocked until it is resolved. Local synthetic callback tests can proceed independently.
