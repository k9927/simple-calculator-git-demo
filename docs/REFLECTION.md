# Reflective note: an intentional merge conflict

## What I built

I built a small command-line calculator in Python (`calculator.py`) with four operations, a README and seven
unit tests. The program was deliberately simple so that the focus stayed on Git. I used `main` as the stable
branch and created two feature branches from the same commit (`16bb21b`):

- `feature/divide-by-zero` made `divide()` raise a clear `ValueError` instead of crashing with
  `ZeroDivisionError`.
- `feature/round-results` made `divide()` round its result to two decimal places.

Both branches also rewrote the same "Division" line in `README.md`.

## What caused the conflict

Git merges with a three-way comparison. For every file it looks at the common ancestor (the merge base,
`16bb21b`), the current branch (`main`, called "ours" or `HEAD`) and the branch being merged in ("theirs").
If only one side changed a region, Git takes that change automatically. If both sides changed the same
region in different ways, Git cannot know which version is correct, so it stops and asks a person.

The first merge (`feature/divide-by-zero` into `main`) went through cleanly, because `main` had not changed
since the branch was created. After that merge, `main` contained a new version of `divide()`. When I then
merged `feature/round-results`, both sides had changed the same lines: the docstring and the `return a / b`
line in `calculator.py`, and line 9 of `README.md`. Git reported `CONFLICT (content)` for those two files
and wrote both versions into each file between `<<<<<<< HEAD`, `=======` and `>>>>>>> feature/round-results`
markers.

The test file is a useful contrast. Both branches added a new test to `test_calculator.py`, but in different
places, so Git merged it without any help. A conflict is not caused by two people editing the same file. It is
caused by two people editing the same lines.

## How I resolved it

1. `git status` showed the merge state: `README.md` and `calculator.py` were "both modified" (unmerged),
   while `test_calculator.py` was already staged.
2. `git diff` showed a combined diff with both versions side by side. `git log --merge --oneline` listed the
   two commits responsible (`7704173` and `2fef1da`), which told me exactly which changes clashed.
3. I opened each file and decided what the code should do. Neither version was wrong; they solved different
   problems. The correct result keeps both: check for zero first, then return the rounded value. I deleted the
   three marker lines and wrote that combined version. For the README I wrote one line describing both features.
4. I ran `git diff` again to review my resolution, then `git add calculator.py README.md` to mark the files as
   resolved. `git status` confirmed "All conflicts fixed but you are still merging."
5. Before committing I ran the tests: all 7 passed, including one test from each branch. A quick manual run gave
   `Result: 3.33` for `10 / 3` and `Error: Cannot divide by zero` for `8 / 0`.
6. `git commit` created the merge commit `fc233f4`, and `git log --oneline --graph --all` showed both branches
   joining `main`.

I knew I had a way out at every step: `git merge --abort` would have returned `main` to its state before the
merge, and `git restore --merge <file>` would have brought the markers back if I had made a mistake while editing.

## What I learned about distributed version control

- **Every copy is a full repository.** My laptop holds the complete history. I committed, branched and merged
  with no network connection; GitHub is just another copy that I synchronise with using `push` and `pull`.
- **Branches are cheap, and merging is where the real work is.** Creating a branch took one command. The
  cost of parallel work appears later, at merge time, so the longer two branches live apart, the more likely a
  conflict becomes.
- **A conflict is a question, not an error.** Git did all the safe work itself and stopped only where human
  judgement was needed. Choosing "ours" or "theirs" blindly would have lost a feature; understanding both
  changes gave a better result than either branch on its own.
- **Verify after resolving.** Removing the markers is not enough: code can be free of markers and still be
  broken. Running the tests before committing the merge is what proved the resolution was correct.
- **Habits that reduce conflicts:** small focused commits, pulling from `main` often, keeping branches short
  lived, and telling teammates when you are changing shared code such as a core function.
- **History is documentation.** Using `--no-ff` and clear commit messages means anyone can read
  `git log --graph` and see what happened and why.
