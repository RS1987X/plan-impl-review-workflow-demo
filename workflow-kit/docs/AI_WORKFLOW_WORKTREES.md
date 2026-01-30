# AI Workflow: Planner / Implementer / Reviewer (Git worktrees)

This doc is a **portable workflow** you can copy to any repo.

## Roles

- **Planner:** writes specs/plans/docs only.
- **Implementer:** writes code + tests, runs verification.
- **Reviewer:** reviews diffs and reruns checks in a clean checkout.

## Why worktrees

Git worktrees let you have multiple working directories backed by the same repo:
- fast (shared object database)
- clean role separation (each worktree == one branch)

## Directory layout

From a base repo `~/projects/MyRepo`, create sibling worktrees:
- `~/projects/MyRepo-plan` (branch `plan-<feature>`)
- `~/projects/MyRepo-impl` (branch `feat-<feature>`)
- `~/projects/MyRepo-review` (branch `review-<feature>`)

## Create worktrees

From the base repo directory:

```bash
./scripts/create-worktrees.sh <feature>
```

### Parallel feature development (multiple lanes)

If you want to work on **multiple features at the same time** without reusing the same `...-plan/impl/review` directories, use `--parallel`.

This creates feature-scoped worktree directories:

```text
../<repo>-worktrees/<feature>/{plan,impl,review}
```

Create a lane:

```bash
./scripts/create-worktrees.sh <feature> --parallel
```

Sync a lane:

```bash
./scripts/sync-worktrees.sh <feature> --parallel
```

Remove a lane:

```bash
./scripts/remove-worktrees.sh <feature> --parallel
```

## Role responsibilities

### Planner

- Create a plan doc under `docs/plans/` (one doc per feature).
- Commit it so it’s durable and visible to implementers.

Optional enforcement:

```bash
chmod -R a-w src tests 2>/dev/null || true
chmod -R u+rwX docs
```

### Implementer

- Implement only the scoped slice.
- Add/adjust tests.
- Run checks locally.

### Reviewer

- Sync and merge into the review worktree.
- Run checks in a clean checkout.
- Record review outcome (must-fix vs suggestions).

#### Clean reviewer checkout (recommended routine)

The reviewer worktree should contain **only committed content** (no local edits). Syncing via `fetch` + `merge` is fine; hand edits in the review worktree are what break “clean-room” review.

After syncing, always verify:

```bash
git status
```

You want: `working tree clean`.

If you previously ran tests/builds and want a truly fresh run (removes caches/artifacts like `__pycache__`, `.pytest_cache`, `dist/`):

```bash
git clean -fdx
```

Then run the project verification commands.

## Sync rule (merge-based)

If you avoid rebase and want predictable history:

- Implementer: merge `origin/main` into `feat-*`
- Reviewer: merge `origin/feat-*` (or `origin/copilot/*`) into `review-*`

Helper:

```bash
./scripts/sync-worktrees.sh <feature> [origin/<implementer-branch>]
```

## PR-based loop (recommended)

1) Planner writes/commits plan
2) Implementer opens PR (or Coding Agent does)
3) Reviewer runs checks, writes review
4) Fix loop until approved
5) Merge to `main`, remove worktrees

## Maintainability audit trail (recommended)

Keep these lightweight artifacts so the project stays easy to evolve:

- `docs/templates/ARCHITECTURE.md` (maintainer map)
- `docs/decisions/` (ADRs for key decisions)
- `docs/templates/FOLLOW_UPS.md` (deferred review items)

Suggested PR “Definition of Done” add-on:
- [ ] Plan doc linked
- [ ] Tests updated; all pass
- [ ] Architecture updated if structure/state changed
- [ ] ADR added if a key decision was made
- [ ] Deferred review items tracked
