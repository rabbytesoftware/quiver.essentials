# Skills

Agent skills for working with Quiver. Each folder is a self-contained skill in
the open [Agent Skills](https://agentskills.io) layout: a `SKILL.md` with
`name`/`description` frontmatter, plus `references/`, `assets/` and
`scripts/` the agent loads only when it needs them.

| Skill | What the agent can do with it |
|---|---|
| [`quiver-arrow-authoring`](quiver-arrow-authoring/SKILL.md) | Write, fix, validate and test-install arrows (`arrow@v0`) and collections (`collection@v0`) |

## Installing a skill

Copy (or symlink) the skill folder into the directory your agent reads skills
from. The folder name must stay `quiver-arrow-authoring`.

```sh
git clone https://github.com/rabbytesoftware/quiver.essentials
cd quiver.essentials
```

| Agent | For every project | For one project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |
| OpenAI Codex CLI | `~/.agents/skills/` | `<project>/.agents/skills/` |
| Gemini CLI | `~/.agents/skills/` (or `~/.gemini/skills/`) | `<project>/.agents/skills/` (or `.gemini/skills/`) |
| Other agents with Agent Skills support | their skills directory | their project skills directory |

For example, for Claude Code:

```sh
mkdir -p ~/.claude/skills
cp -R skills/quiver-arrow-authoring ~/.claude/skills/
```

`~/.agents/skills/` is shared by Codex and Gemini CLI, so one copy there
serves both. Create the directory first (`mkdir -p`); fresh installs do not
have it. Use `ln -s "$PWD/skills/quiver-arrow-authoring" <dir>/` instead of
`cp -R` to pick up updates with a `git pull`.

The agent picks the skill up on its own when asked to package software for
Quiver ("make an arrow for ripgrep", "add this tool to quiver.essentials").

### Agents that read instructions but not skills

Point the agent's instruction file (`AGENTS.md`, `CLAUDE.md`,
`.github/copilot-instructions.md`, a Cursor rule, ...) at the skill:

```markdown
When writing or editing Quiver manifests (ARROW.md, arrow.yaml, collection.yaml),
first read path/to/quiver-arrow-authoring/SKILL.md and follow it.
```

### Chat assistants (ChatGPT, Grok, Gemini, Claude.ai, ...)

Chat assistants without a shell can still use the knowledge, but not the
scripts. Produce one self-contained file and attach it to the conversation,
or add it to the assistant's project/knowledge files:

```sh
python3 skills/quiver-arrow-authoring/scripts/quiver_arrow.py bundle > quiver-arrow-authoring.md
```

Then ask, e.g.: "Using the attached Quiver arrow-authoring guide, write an
arrow for <software>." The assistant cannot validate there; validate the
result yourself before publishing:

```sh
python3 skills/quiver-arrow-authoring/scripts/quiver_arrow.py validate arrow.yaml
```

## Requirements for the scripts

- Python 3.9+ (standard library only).
- A quiver.core daemon to validate against: on macOS/Linux the local one
  (`~/.quiver/quiver.sock`, running whenever Quiver Desktop or `quiver` is)
  or `QUIVER_SOCKET`; anywhere, a TCP daemon via `QUIVER_API` plus its device
  token in `QUIVER_TOKEN`. Local Windows daemons use a named pipe, which the
  script does not support.
- For sandbox installs: macOS or Linux, and a `quiver` binary (`QUIVER_BIN`,
  `quiver` on `PATH`, or `~/.quiver/self/quiver`).
- Network access for `assets` and `checksum`.

## Keeping a skill in sync with quiver.core

`quiver-arrow-authoring` states the quiver.core commit it was verified
against in its frontmatter (`metadata.quiver-core`) and at the top of every
reference file. When the manifest specs change
(`docs/spec/manifests/v0/` in quiver.core):

1. Re-read the changed spec sections and update the matching reference file.
2. Re-validate every example against a daemon built from the new commit:
   `python3 skills/quiver-arrow-authoring/scripts/quiver_arrow.py validate skills/quiver-arrow-authoring/assets/examples/*.yaml`
3. Re-check the "Behaviours validation does not catch" list in
   `references/validation-and-testing.md` §5: those are runtime facts, and
   fixes in quiver.core change them.
4. Update the commit reference in `SKILL.md` and in each reference file.
