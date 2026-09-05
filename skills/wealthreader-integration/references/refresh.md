# Refresh and errors

Sources: [API reference](https://www.wealthreader.com/api-reference/en/), [Backend refresh](https://www.wealthreader.com/docs/en/iframe-integration-2-of-2-backend/), [Error catalog](https://api.wealthreader.com/error-codes/?lang=en). Checked 2026-09-05.

## Request contract

Refresh server-side with `POST https://api.wealthreader.com/entities/`, encoded as `application/x-www-form-urlencoded`, not JSON or a guessed Bearer scheme. Supply `api_key`, the stored institution `code`, and its callback `token`; `product_types` is comma-separated.

Illustrative form body, deliberately non-executable:

```text
api_key=YOUR_SERVER_API_KEY&code=YOUR_INSTITUTION_CODE&token=YOUR_STORED_TOKEN&product_types=accounts
```

Use the language's form encoder, not string concatenation. Read secrets from server storage at runtime; never print the completed request.

`only_balances` defaults to false. API `date_from` uses `YYYY-MM-DD` before today. `date_to` is for future-date restrictions on loan and confirming products, not a general transaction end date. Fetch the current schema for product-specific fields. Extended transaction details increase request cost/time and require a dedicated environment.

## Failure policy

Evaluate both transport status and the response envelope. Consult the current English error catalog before assigning numeric codes to actions; distinguish warnings from failures. Do not infer retryability from an HTTP code alone.

- Invalid credentials: stop; do not resend unchanged credentials.
- Expired/invalid reusable credentials or renewed authentication: reopen the widget with `wr_conf.token` for the authorized user.
- Maintenance: bounded retries may be appropriate. Backoff, maximum attempts, and user-visible failure handling are application choices, not documented provider guarantees.
- Unknown outcomes: preserve prior data, report uncertainty, and avoid unlimited polling.

Do not add advanced credential or OTP orchestration to a standard widget integration without an explicit requirement and a verified contract. Do not present the stored aggregation token as a generic OAuth access or refresh token.
