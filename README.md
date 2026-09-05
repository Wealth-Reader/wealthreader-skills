# WealthReader skills

Public, English-language guidance for AI coding assistants integrating WealthReader financial aggregation. The `wealthreader-integration` skill covers widget onboarding, backend callbacks, redirect authentication, and token-based refresh. It does not implement bank connectors or initiate payments.

The skill follows the open [Agent Skills](https://agentskills.io/specification) format, so the same folder works in Claude Code, Codex, Cursor, Antigravity, Gemini CLI, GitHub Copilot, Grok Build, Windsurf, OpenCode, Amp, Cline, Roo Code, Kiro, and any other assistant that reads `SKILL.md`.

## Quick install

Pick whichever fits your setup. Each command installs the same skill folder; only the destination changes.

```bash
# Any assistant, interactive picker (Skills CLI)
npx skills add Wealth-Reader/wealthreader-skills

# One assistant, no prompts (example: Claude Code, user scope)
npx skills add Wealth-Reader/wealthreader-skills --skill wealthreader-integration -a claude-code -g -y

# GitHub CLI
gh skill install Wealth-Reader/wealthreader-skills wealthreader-integration --agent claude-code --scope user

# Gemini CLI
gemini skills install https://github.com/Wealth-Reader/wealthreader-skills.git --consent

# Amp
amp skill add https://github.com/Wealth-Reader/wealthreader-skills --global
```

Manual install works everywhere: copy `skills/wealthreader-integration/` into the directory your assistant reads, then start a new session.

```bash
git clone https://github.com/Wealth-Reader/wealthreader-skills.git
DEST="$HOME/.agents/skills"   # pick the path for your assistant from the table below
mkdir -p "$DEST"
# Check for an existing installation before copying; do not overwrite local edits.
test ! -e "$DEST/wealthreader-integration" && \
  cp -R wealthreader-skills/skills/wealthreader-integration "$DEST/"
```

## Where each assistant looks

`.agents/skills/` (project) and `~/.agents/skills/` (user) are the shared cross-agent locations. Committing the skill to `.agents/skills/` in your application repository covers most assistants at once. Claude Code, Cline, and Kiro read only their own directories, so add a second copy or a symlink for them.

| Assistant | Project directory | User directory | Invoke |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/wealthreader-integration` or automatic |
| Codex (CLI, IDE, ChatGPT) | `.agents/skills/` | `~/.agents/skills/` | `$wealthreader-integration` or `/skills` |
| Cursor | `.agents/skills/` or `.cursor/skills/` | `~/.agents/skills/` or `~/.cursor/skills/` | `/` picker or automatic |
| Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` | Mention the skill by name |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/` | `~/.agents/skills/` or `~/.gemini/skills/` | Automatic; `/skills list` |
| GitHub Copilot | `.agents/skills/` or `.github/skills/` | `~/.agents/skills/` or `~/.copilot/skills/` | Automatic |
| Grok Build | `.grok/skills/` (also reads `.claude/skills/`) | `~/.grok/skills/` or `~/.agents/skills/` | `/wealthreader-integration` |
| Windsurf | `.agents/skills/` or `.windsurf/skills/` | `~/.agents/skills/` or `~/.codeium/windsurf/skills/` | `@wealthreader-integration` |
| OpenCode | `.agents/skills/` or `.opencode/skills/` | `~/.agents/skills/` or `~/.config/opencode/skills/` | Automatic |
| Amp | `.agents/skills/` | `~/.agents/skills/` or `~/.config/agents/skills/` | Automatic |
| Cline | `.cline/skills/` (also reads `.claude/skills/`) | `~/.cline/skills/` | `/wealthreader-integration` |
| Roo Code | `.agents/skills/` or `.roo/skills/` | `~/.agents/skills/` or `~/.roo/skills/` | Automatic |
| Kiro | `.kiro/skills/` | `~/.kiro/skills/` | `/wealthreader-integration` |

Paths were checked against each vendor's public documentation on 2026-09-05. Assistants not listed usually accept `.agents/skills/` or a `<tool>/skills/` folder; check its documentation for the exact path. If your assistant has no skill support, reference the file from its instructions file (`AGENTS.md`, `CLAUDE.md`, or equivalent) or paste `SKILL.md` into the conversation.

## Use it

Ask for the integration in your application's own stack. Example:

> Use the wealthreader-integration skill to add the WealthReader widget and backend callback to my application. Retrieve accounts and transactions, and test locally without making live banking requests.

The skill contains instructions, not credentials, an SDK, or a hosted service. Live use still requires WealthReader onboarding and application configuration. Listing in any assistant's skill directory or marketplace is out of scope for this repository.

## Repository layout

```
skills/wealthreader-integration/
├── SKILL.md              # Entry point: flow selection, security boundary, verification
├── references/
│   ├── widget.md         # Embedded widget and backend callback
│   ├── refresh.md        # Token-based refresh and error handling
│   └── oauth.md          # Redirect authentication for native or non-embedded apps
└── agents/openai.yaml    # Optional display metadata for Codex and ChatGPT; other assistants ignore it
scripts/validate_skills.py  # Offline structural check
```

## Public provenance and maintenance

All provider-specific guidance was prepared from unauthenticated public documentation, checked on 2026-09-05. No private source code, production credentials, customer records, or HAR files are included. Each reference links its sources:

- [Widget and callback](skills/wealthreader-integration/references/widget.md)
- [Refresh and errors](skills/wealthreader-integration/references/refresh.md)
- [Redirect authentication](skills/wealthreader-integration/references/oauth.md)

Before changing a contract, verify it against the linked public documentation and update the checked date. Keep prose, comments, and examples in English. Use synthetic fixtures, not copied personal-data examples. Keep recommendations distinct from documented provider guarantees; report documentation gaps rather than inventing behavior.

Repository materials are available under the [MIT License](LICENSE). Access to the WealthReader API and services remains subject to separate terms.

## Validation

Run the offline structural check before publishing changes. It needs only Python 3 and verifies frontmatter, naming rules, the SKILL.md line budget, and relative links.

```bash
python3 scripts/validate_skills.py
```

The optional [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) reference validator checks the same frontmatter against the Agent Skills specification:

```bash
skills-ref validate skills/wealthreader-integration
```

These checks cover structure, not production connectivity. Also verify source accuracy, example syntax, and privacy. Test realistic prompts for widget integration, expired-token recovery, and redirect authentication; require the assistant to identify unresolved production security controls. Never run real banking requests as an implicit validation step.
