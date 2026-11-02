I am continuing work on the "$ARGUMENTS" project.

<!-- Made By FALCREB -->

IMPORTANT: this command is read-only. It does not change project files, the working directory or commit history. `git fetch` is allowed only to update remote-tracking references. No other git write operation (pull, merge, stash, commit) is allowed.

1. Read the latest section of `PROGRESS.md`, if it exists.
2. Check the active branch.
3. Review the last 3-5 commits.
4. Check for uncommitted changes.
5. Run `git fetch` and compare the local branch with the remote (behind / ahead / in sync).
6. Run `gh pr list` and check for open PRs and unmerged branches.
7. Count open Dependabot alerts by severity: `gh api "repos/<owner>/<repo>/dependabot/alerts?state=open&per_page=100"`. Name the package and patched version for critical/high.
8. Skim `README.md` and any TODO or known-issue notes.
9. Compare `PROGRESS.md` with the real git state and flag inconsistencies.
10. If `.env.example` exists but `.env` does not, tell me. Do not create it.

Finish with this short summary, without long logs:
- Last environment: [machine and date from PROGRESS.md]
- Last work: [from PROGRESS.md and recent commits]
- Current state: [clean / unfinished changes / out of sync / open PR / .env missing]
- Known issues: [from PROGRESS.md]
- Security alerts: [critical/high/medium/low counts, or "none open"]
- Next action: [from PROGRESS.md, otherwise a sensible suggestion]

If the state is not clean, is out of sync, or `.env` is missing, highlight it and ask how to proceed.

If the local branch is BEHIND the remote, say so clearly and ask whether to pull. Pull only after my explicit approval, as a separate step, and remind me first about any uncommitted changes.
