# Global Rules

<!-- Made By FALCREB -->

## Communication
- I am not a software developer. Explain things plainly, with everyday analogies when useful.
- Do not avoid real terms (commit, branch, merge, dependency, deploy). Define each one briefly the first time it appears, so I learn the subject as we work. Do not redefine the same term every time.

## Package manager
- Default to pnpm for new JS/Node projects. Never change the package manager of an existing project.

## Security
- Never put API keys, passwords or tokens in code. Use `.env`.
- Never commit `.env`. Confirm it is in `.gitignore` before every commit.
- If something looks like a secret: move it to `.env` when you are sure it is real. If unsure (test fixture, example value), do not change it; tell me and let me decide.
- If a secret was committed, deleting it in a new commit is not enough:
  1. Revoke or rotate it in the service panel immediately.
  2. Clean the history with `git filter-repo` or BFG Repo-Cleaner.
  3. Ask me before any force push.
- Consider known vulnerabilities when adding a dependency.

## .env
- Whenever you create `.env`, also create `.env.example` with variable names only.
- Keep `.env.example` current and remove unused variables.

## Line endings
- On first upload add `.gitattributes` containing `* text=auto eol=lf`, to avoid false changes between Windows and other machines.

## Session continuity
Update `PROGRESS.md` on every `/ship`, using this exact template so `/resume` can read it reliably:

```
### [Date - Hostname]
- **Done & decisions:**
- **Last commit:** (hash + message of HEAD before this /ship creates its commit; never guess the new hash. "first upload, no commit" if none)
- **Active branch:**
- **Next action:**
- **Known issues / watch out:**
```

- Get the hostname from the `hostname` command; never invent it.
- Start each new session with `/resume`.
- Commit `PROGRESS.md`; it must never contain secrets.

## Changelog
- On every `/ship`, add 1-2 plain sentences to `[Unreleased]` in `CHANGELOG.md`.
- When a semver tag is created, move `[Unreleased]` under that version.

## Commits
- Commit messages are in English, using conventional commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`).
- Do not ask me for the message; write it from the diff.
- One logical change per commit.
- Keep any `Co-Authored-By: Claude ...` line.
- If `git config --global user.name/user.email` is missing, or the email is not linked to my GitHub account, tell me before committing. GitHub's `...@users.noreply.github.com` address is recommended for privacy.
- Projects use the global identity. If a project has a local `user.name/user.email`, remove it before committing and tell me briefly.

## Branches and pull requests
- Use the prefixes `feature/`, `fix/`, `chore/`, `docs/`.
- Each logical unit of work goes on its own branch and enters the default branch through a pull request (PR). Never commit directly to the default branch, including during `/ship`.
- Only exception: the very first upload of a repository.
- The default branch is protected on GitHub by a ruleset named "Protect default branch": no direct push, no force push, no deletion, PR required, 0 approvals so I can merge my own PRs. Add it right after the first push of a new repository. Private repositories need a paid plan for this; if it is unavailable, this PR rule still applies.
- Never split work artificially to increase the PR count; each PR must be real and meaningful.
- PR titles use conventional commits; descriptions are short. Never put secrets in a PR.
- After tests and lint pass, merge with `gh pr merge --merge`. If the merge conflicts or fails, leave the PR open, stop and tell me.
- Delete merged branches (remote and local) without asking. Never delete unmerged branches without approval.
- After merging, update local main only by fast-forward: `git fetch` + `git merge --ff-only origin/main`. If that is not possible, stop and ask.

## Before pushing
- Check that the code runs.
- Run tests if they exist. If tests fail, stop and tell me. If there are no tests, say so and continue; do not confuse the two cases.
- Run lint/format tools if the project has them.
- Do not commit logs, caches or temporary files.
- Always `git fetch` first. If the remote has unexpected commits, do not rebase, merge, force or pull automatically; explain and ask. The only automatic update is the fast-forward after your own merged PR.

## Dependencies
- Choose actively maintained versions. Always commit the lock file.
- For security fixes prefer a safe version within the current major version; do not blindly jump to latest.
- Tell me about unused dependencies.
- Keep Dependabot alerts enabled (`gh api -X PUT repos/<owner>/<repo>/vulnerability-alerts`). Report open critical/high alerts, and fix them on a separate `fix/` branch and PR.

## .gitignore
- Review an existing `.gitignore` and keep its rules; only add what is missing, and do not remove rules without approval.
- Base list: `node_modules/`, `__pycache__/`, `.venv/`, `dist/`, `build/`, `*.log`, `.DS_Store`, `.env`, `.env.*`, `!.env.example`

## Versioning
- Suggest a semver tag at important milestones, with a short changelog entry.

## Undoing safely
- Before a risky change, never commit my uncommitted work on your own; it may be unfinished. You may propose a safety branch or tag, with my approval.

## Large files
- Warn me before adding files over 50 MB; suggest `.gitignore` or Git LFS.

## Way of working
- For big changes, summarize the plan first, then apply it.
- Do not change behaviour that works unless asked. If a change would break something working, tell me first.

## Reporting
- End each task with a short bullet summary, results rather than logs.
- State failures clearly; never continue silently.
- At the end of `/ship`, report commit, push and PR status separately; never say "done" if one failed.

## Always ask first (hard or impossible to undo)
- Force push on any branch
- Commands that can destroy uncommitted work: `git reset --hard`, `git clean -fd`, `git checkout .`, `git restore .`
- Changing the origin URL of an existing repository
- Changing repository visibility
- Deleting or transferring a repository
- Deleting files or folders (merged branches excepted)
- Never commit `.env` or files with secrets, even with approval
