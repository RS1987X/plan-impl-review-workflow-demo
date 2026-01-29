# AI Workflow: Planner / Implementer / Reviewer (Git worktrees)

This repo can be worked on using **multiple parallel “roles”** in separate working directories backed by **Git worktrees**.

The goal is to reduce context switching and waiting time:
- **Planner** window: writes *plans/specs/docs* only.
- **Implementer** window: writes code/tests and runs verification.
- **Reviewer** window: reviews diffs and runs checks in a clean checkout.

This document is designed to be **portable**: you can copy it to other repos.

---

## Why worktrees

A Git worktree is a separate working directory attached to a branch.
- Worktrees **are branches** (each worktree checks out a branch).
- All worktrees share the same underlying Git object database (fast, space-efficient).

Compared to “multiple clones”, worktrees keep fetch/object storage unified.

---

## Directory layout (example)

Assume your main repo is:
- `~/projects/Thesys`

Create sibling worktrees:
- `~/projects/Thesys-plan`
- `~/projects/Thesys-impl`
- `~/projects/Thesys-review`

Open each folder in a separate window.

---

## 1) Create worktrees

From the primary repo directory (use `main` as the base):

```bash
cd ~/projects/Thesys
git switch main
git pull

# Naming convention: plan-*, feat-*, review-* (customize as needed)
FEATURE=portfolio-phase1

git worktree add ../Thesys-plan   -b plan-$FEATURE
git worktree add ../Thesys-impl   -b feat-$FEATURE
git worktree add ../Thesys-review -b review-$FEATURE
```

Open:

```bash
code ~/projects/Thesys-plan
code ~/projects/Thesys-impl
code ~/projects/Thesys-review
```

---

## 2) Role responsibilities

### Planner role (docs/spec only)

What you do:
- Write the plan/spec (scope, acceptance criteria, UI notes, edge cases, test plan).
- Record known trade-offs in `docs/KNOWN_LIMITATIONS.md` when relevant.

What you avoid:
- Editing `src/` or `tests/`.

Optional enforcement (recommended): make code read-only in planner worktree.

```bash
cd ~/projects/Thesys-plan
chmod -R a-w src tests
# (Optional) lock entry points
chmod a-w run.py
```

Undo (if you need to edit later):

```bash
cd ~/projects/Thesys-plan
chmod -R u+w src tests
chmod u+w run.py
```

### Implementer role (code + tests)

What you do:
- Implement the planned slice (Phase 1 only, etc.).
- Add/update tests.
- Run verification commands.
- Keep diffs minimal unless refactors are required.

**Thesys-specific constraints:**
- Heavy computation must not run on the GUI thread. Use `QThread` workers in `src/thesys/gui/threads.py`.
- Follow existing logging patterns.

### Reviewer role (clean checkout review)

What you do:
- Merge in implementer branch for review.
- Run tests in an isolated worktree.
- Provide feedback / request changes.

What you avoid:
- Doing substantial edits here (optional, but helps keep roles clean).

---

## 3) The “sync” rule (merge-based, no rebase)

If you prefer merge over rebase (to keep history safe/predictable):

### Update implementer with latest `main`

```bash
cd ~/projects/Thesys-impl
git fetch origin
git merge origin/main
```

### Update reviewer with implementer branch

```bash
cd ~/projects/Thesys-review
git fetch origin
git merge origin/feat-$FEATURE
```

Notes:
- This is the main “manual sync” pain point: you must repeat it per worktree.
- It’s predictable and avoids rebase pitfalls.

---

## 4) Implementer prompt: what to give Copilot Coding Agent

Even if you wrote a full planner doc, the implementer still needs a short **work order** so it doesn’t drift.

### Minimal, high-signal implementer prompt (template)

Copy/paste and fill in the placeholders:

```text
Read and follow: docs/<PLAN_DOC>.md

Implement: <PHASE/SCOPE> only. Do not implement later phases.

Hard constraints:
- Do not block the GUI thread; heavy computation must run in QThread workers (src/thesys/gui/threads.py).
- Keep the diff minimal; no refactors unless required.

Definition of done:
1) <user-visible behavior>
2) <correctness constraints / edge cases>
3) Tests added/updated for <core logic>
4) All tests pass

Verification (run from repo root):
- source .venv/bin/activate && PYTHONPATH=$(pwd) pytest tests/unit/
- source .venv/bin/activate && PYTHONPATH=$(pwd) pytest tests/

If anything is ambiguous, ask clarifying questions before editing.
```

---

## 5) Reviewer checklist

Suggested review checklist:
- Scope matches the plan (no Phase 2+ creep)
- No GUI blocking introduced (threading is correct)
- Tests cover core logic + edge cases
- Logging is reasonable (no prints)
- CSV/export format remains stable (if applicable)

Useful commands:

```bash
cd ~/projects/Thesys-review

git diff origin/main...HEAD
source .venv/bin/activate && PYTHONPATH=$(pwd) pytest tests/
```

---

## 6) Finish the work

### Keep planner docs permanently

To ensure the planner doc persists after removing the planner worktree:
- commit it, push it, and merge it into `main` (or cherry-pick onto `main`).

### Merge feature to `main`

One approach (from implementer worktree):

```bash
cd ~/projects/Thesys-impl

git push -u origin feat-$FEATURE

git switch main
git fetch origin
git merge origin/main

git merge feat-$FEATURE

git push origin main
```

### Remove worktrees

```bash
cd ~/projects/Thesys

git worktree remove ../Thesys-plan
git worktree remove ../Thesys-review
git worktree remove ../Thesys-impl
```

Important: removing a worktree deletes the directory checkout, **not** committed history.

---

## 7) Common pitfalls

- Editing in the wrong window: name windows/workspaces with the role.
- Forgetting to sync: establish a habit (`fetch` + `merge origin/main`) at start of each session.
- Planner doc not committed: uncommitted docs can be lost when removing the worktree.

---

## 8) Optional automation ideas

If manual syncing becomes annoying, consider a tiny script/Make target to:
- `git fetch origin` once
- for each worktree: `git -C <path> merge origin/main` (or merge the feature branch)

Keep it simple and transparent; avoid hiding complex merge behavior.