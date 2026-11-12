# Checkpoint A - Théo TAVARES (theotavares92600)

## Context

I joined the team during TD05, so I caught up on TD01 to TD04 on my own side
and added my own contributions while keeping my teammates' work intact.

## Evidence

### 01_terminal_python.png

Shows my working environment: Python 3.14.2, Git 2.55.0, and
`python src/main.py` running and printing the MarketPulse output for the
instrument (AAPL) and the benchmark (SP500).

### 02_git_status_log.png

Shows `git status` on my feature branch with a clean working tree, and
`git log --oneline -10` with my own commit on top of the team history.

### 03_branch_merge.png

Shows `git branch --merged` listing `fix/data-path-resolution` as merged into
main, and the Git graph with my commit integrated. The merge was a
fast-forward.

## My contributions

**PR #7** - `TEAM.md`: added myself to the team members, fixed the missing
  Markdown separator line that made the table render as plain text on GitHub,
  and removed the leftover instruction line from `TEAM_TEMPLATE.md`.
**PR #8** - `src/main.py`: fixed `DATA_DIR`, which was a path relative to the
  current directory. `python src/main.py` crashed with `FileNotFoundError`
  when run from anywhere other than the repository root. It is now resolved
  from `__file__`, like the `sys.path` line above it.
**PR #9** - this Checkpoint A evidence folder.

## What I understood

**Why we work on branches.** A branch lets me work on my own change without
touching main. If everyone committed directly to main, we would conflict with
each other constantly. Branches do not remove conflicts, they postpone them to
the merge, when we can deal with them calmly.

**Modified, staged, committed.** When I edit a file it is *modified*.
`git add` moves it to the *staging area*, which lets me choose what goes into
the next commit. `git commit` records it in the project history.

**Fast-forward merge.** My branch sits directly on top of main, because main
did not move after I created the branch. To merge, Git only has to move the
main label forward, so no merge commit is created. If main had moved too, Git
would have to create a merge commit.

**Merge conflicts.** A conflict happens when two branches modify the same lines
of the same file. Git stops because it cannot know which version is the right
one, so a human has to decide. In my case there was no conflict on `TEAM.md`
because nobody else touched that file while I was away.