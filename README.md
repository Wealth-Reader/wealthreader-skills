# WealthReader skills

Public, English-language guidance for coding assistants integrating WealthReader financial aggregation. The first skill covers widget onboarding, backend callbacks, redirect authentication, and token-based refresh. It does not implement bank connectors or initiate payments.

## Install and use

Copy `skills/wealthreader-integration/` into the skill directory supported by your coding assistant. For Codex, a manual user-level installation is:

```bash
git clone https://github.com/Wealth-Reader/wealthreader-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
# Check for an existing installation before copying; do not overwrite local edits.
test ! -e "${CODEX_HOME:-$HOME/.codex}/skills/wealthreader-integration" && \
  cp -R wealthreader-skills/skills/wealthreader-integration \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Example request:

> Use $wealthreader-integration to add the WealthReader widget and backend callback to my application. Retrieve accounts and transactions, and test locally without making live banking requests.

The skill contains instructions, not credentials, an SDK, or a hosted service. Live use still requires WealthReader onboarding and application configuration. GitHub publication does not imply listing in a ChatGPT directory or compatibility with every assistant.

## Public provenance and maintenance

All provider-specific guidance was prepared from unauthenticated public documentation, checked on 2026-09-05. No private source code, production credentials, customer records, or HAR files are included. Each reference links its sources:

- [Widget and callback](skills/wealthreader-integration/references/widget.md)
- [Refresh and errors](skills/wealthreader-integration/references/refresh.md)
- [Redirect authentication](skills/wealthreader-integration/references/oauth.md)

Before changing a contract, verify it against the linked public documentation and update the checked date. Keep prose, comments, and examples in English. Use synthetic fixtures, not copied personal-data examples. Keep recommendations distinct from documented provider guarantees; report documentation gaps rather than inventing behavior.

No repository license has been selected yet.

## Validation

With the Codex skill-creator tooling installed:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/wealthreader-integration
```

This checks skill structure, not production connectivity. Also verify relative links, source accuracy, example syntax, and privacy before publishing changes. Test realistic prompts for widget integration, expired-token recovery, and redirect authentication; require the assistant to identify unresolved production security controls. Never run real banking requests as an implicit validation step.
