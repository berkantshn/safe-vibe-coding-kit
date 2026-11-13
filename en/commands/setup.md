Set up or re-sync the Safe Vibe Coding Kit plugins on this computer.

<!-- Made By FALCREB -->

1. Start your reply by showing this banner exactly as it is, inside a code block:

```text
███╗   ███╗ █████╗ ██████╗ ███████╗    ██████╗ ██╗   ██╗
████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝
██╔████╔██║███████║██║  ██║█████╗      ██████╔╝ ╚████╔╝
██║╚██╔╝██║██╔══██║██║  ██║██╔══╝      ██╔══██╗  ╚██╔╝
██║ ╚═╝ ██║██║  ██║██████╔╝███████╗    ██████╔╝   ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═════╝    ╚═╝

███████╗ █████╗ ██╗      ██████╗██████╗ ███████╗██████╗
██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝██╔══██╗
█████╗  ███████║██║     ██║     ██████╔╝█████╗  ██████╔╝
██╔══╝  ██╔══██║██║     ██║     ██╔══██╗██╔══╝  ██╔══██╗
██║     ██║  ██║███████╗╚██████╗██║  ██║███████╗██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝
```

2. If `~/.claude/scripts/kit_settings.json` does not exist or has no `lsp` value, ask me whether I write TypeScript/JavaScript or PHP (that decides whether language servers are installed). Otherwise keep the saved choice.
3. See the current state first, without changing anything:
   `python ~/.claude/scripts/install.py --check --lang en`
4. If something is missing, list it briefly and run the setup:
   `python ~/.claude/scripts/install.py --lang en --lsp <yes|no>`
   - If a required program (node, gh, etc.) is MISSING, do not install it yourself; tell me where to get it.
   - If the git identity is MISSING, tell me how to set it with my own name and GitHub email; do not invent values.
   - If NEWER VERSION is reported for an npm tool, only tell me; do not upgrade it.
5. If anything was installed, remind me to restart Claude Code.

Finish with a short summary: what was already in place, what was installed, and what failed or needs me. No long logs.
