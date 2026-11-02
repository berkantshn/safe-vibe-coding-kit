Upload or update the "$ARGUMENTS" project on GitHub.

<!-- Made By FALCREB -->

If $ARGUMENTS is empty: do not start; say the repository name is missing and stop.

$ARGUMENTS is the GitHub repository name. The current directory holds the project files; the two names may differ.

## 0. Detect the mode
- No `.git`, no remote, or no GitHub repository with this name: FIRST UPLOAD.
- `.git` and the GitHub repository exist: UPDATE.

If `origin` points to an unexpected repository, STOP. Do not change it; explain and ask. Tell me which mode you entered.

## FIRST UPLOAD
1. `git init`, unless `.git` already exists.
2. Scan for secrets, including `git status` and `git diff --cached`. Move real secrets to `.env`. If unsure, do not change anything; tell me what and where.
3. `.gitignore`: keep existing rules and add what is missing from the base list in CLAUDE.md. If a `.env.*` file (other than `.env.example`) was already committed, adding it to `.gitignore` is not enough; tell me.
4. Add `.gitattributes` with `* text=auto eol=lf`.
5. Warn about staged files over 50 MB; do not commit them without approval.
6. Create `README.md`: purpose, setup, run commands, technologies.
7. Create `PROGRESS.md` from the template in CLAUDE.md, with "first upload, no commit".
8. Create `CHANGELOG.md` in Keep a Changelog format.
9. Detect the package manager; use pnpm only for a new JS/Node project without one.
10. Run tests and lint if present. If tests fail, stop. If none exist, say so and continue.
11. Commit and publish. This first commit goes directly to main:
    - Write the conventional commit message from the diff and show only the message.
    - If the repository does not exist, create it as **private**. If it exists, use it and tell me.
    - `git fetch`, then push.
    - Add a short description and topics.
    - Enable Dependabot alerts: `gh api -X PUT repos/<owner>/$ARGUMENTS/vulnerability-alerts`
    - Add the "Protect default branch" ruleset: deletion + non_fast_forward + pull_request, 0 approvals, target `~DEFAULT_BRANCH`: `gh api -X POST repos/<owner>/$ARGUMENTS/rulesets --input <ruleset.json>`

## UPDATE
0. If `README.md`, `PROGRESS.md`, `CHANGELOG.md`, `.gitattributes`, or `.env.example` (when `.env` exists) is missing, create it. Add a description and topics if empty.
1. If the working tree is clean and there are no unpushed commits or open PRs, say so and stop. Otherwise continue. Apply the same careful secret check to new changes. Never commit my unfinished work as a safety step without approval.
2. Check for files over 50 MB; ask if there are any.
3. Update `README.md` for new features, commands or dependencies.
4. Add a section to `PROGRESS.md` using the template. "Last commit" is HEAD before this commit.
5. Add 1-2 plain sentences to `[Unreleased]` in `CHANGELOG.md`.
6. Run tests and lint. If tests fail, stop.
7. Git and pull request:
   - On main: create a suitable prefixed branch; uncommitted changes move with it. On a work branch: use it. If changes cover unrelated topics, ask how to split them.
   - Write the commit message from the diff, show only the message, and commit.
   - `git fetch`. If the remote has unexpected commits, do not rebase, merge, force or pull; explain and ask.
   - Push and open a PR, or reuse the open PR for this branch.
   - If tests and lint passed: `gh pr merge --merge`. If merge fails, leave the PR open, stop and tell me.
   - After merging: delete the remote and local branch, switch to main, then `git fetch` + `git merge --ff-only origin/main`. If that fails, stop and ask.

## Final report
Report each separately:
- Git commit: success / failure
- GitHub push: success / failure
- Pull request: merged / left open (why) / failed, with link ("first upload, no PR" on first upload)

If something failed, say what succeeded and what is missing. Share the repository link.
