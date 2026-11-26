# Exact steps taken

Environment: Windows 11, Git Bash (MINGW64), Git 2.47.1, Python 3.12.
Every command below was run in this order. Commit hashes are the real ones in this repository.

## 1. Create the repository and the first commits

```bash
git init -b main
# created calculator.py (add, subtract, multiply, divide), README.md, .gitignore
git status
git add .
git commit -m "Initial commit: calculator with add, subtract, multiply, divide"   # 4287697
# created test_calculator.py
git add test_calculator.py
git commit -m "Add unit tests for the four operations"                            # 16bb21b
git log --oneline
```

Screenshot: `screenshots/01-init-and-first-commits.png`

## 2. Two feature branches change the same lines

Both branches start from commit `16bb21b`.

```bash
git switch -c feature/divide-by-zero
# calculator.py: divide() now checks "if b == 0" and raises ValueError("Cannot divide by zero")
# README.md:     "- Division: ..." line -> "shows a clear error message when dividing by zero"
# test_calculator.py: added test_divide_by_zero_raises_error
git add calculator.py README.md test_calculator.py
git commit -m "Raise a clear error when dividing by zero"                         # 7704173

git switch main
git switch -c feature/round-results
# calculator.py: the SAME divide() lines now "return round(a / b, 2)"
# README.md:     the SAME "- Division: ..." line -> "results are rounded to 2 decimal places"
# test_calculator.py: added test_divide_rounds_to_two_decimals (in a different place)
git commit -am "Round division results to 2 decimal places"                       # 2fef1da
git log --oneline --graph --all
```

Screenshot: `screenshots/02-two-feature-branches.png`

## 3. Merge the first branch into main (succeeds)

```bash
git switch main
git merge --no-ff feature/divide-by-zero -m "Merge branch 'feature/divide-by-zero' into main"   # 0d1ac6e
git log --oneline --graph --all
```

`--no-ff` keeps a merge commit so the branch stays visible in the history.

Screenshot: `screenshots/03-first-merge-succeeds.png`

## 4. Merge the second branch (conflict)

```bash
git merge feature/round-results
# Auto-merging README.md
# CONFLICT (content): Merge conflict in README.md
# Auto-merging calculator.py
# CONFLICT (content): Merge conflict in calculator.py
# Auto-merging test_calculator.py
# Automatic merge failed; fix conflicts and then commit the result.

git status                              # "both modified: README.md, calculator.py"
git diff                                # combined diff showing the conflict markers
git log --merge --oneline               # the two commits that clash: 2fef1da and 7704173
git diff --name-only --diff-filter=U    # only the conflicted files
cat README.md                           # markers in the Features list
sed -n '22,34p' calculator.py           # markers inside divide()
```

`test_calculator.py` merged automatically because the two branches added tests in different places.

Screenshots: `04-merge-conflict.png`, `05-conflict-diff.png`, `06-conflict-markers.png`

## 5. Resolve the conflict by hand

I opened both files in the editor, deleted the `<<<<<<< HEAD`, `=======` and `>>>>>>> feature/round-results`
lines, and wrote one version that keeps both features.

```python
def divide(a, b):
    """Return a divided by b, rounded to 2 decimal places.

    Raises ValueError with a friendly message when b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return round(a / b, 2)
```

README line: `- Division: results are rounded to 2 decimal places, and dividing by zero shows a clear error message`

```bash
git diff                                # check the resolution before staging it
git add calculator.py README.md         # mark both files as resolved
git status                              # "All conflicts fixed but you are still merging."
python -m unittest -v                   # 7 tests, all OK
printf '10 / 3\n8 / 0\nq\n' | python calculator.py   # Result: 3.33 / Error: Cannot divide by zero
git commit -m "Merge branch 'feature/round-results': keep zero check and rounding in divide()"   # fc233f4
git log --oneline --graph --all
```

Screenshots: `07-conflict-resolved.png`, `08-tests-pass.png`, `09-merge-commit.png`

Safety commands I could have used if the resolution went wrong (not needed this time):

- `git merge --abort` cancels the merge and returns main to `0d1ac6e`.
- `git restore --merge calculator.py` brings the conflict markers back into a file before it is staged.
- `git checkout --conflict=diff3 calculator.py` re-creates the markers and also shows the common base version.

## 6. Publish to GitHub, then push and pull

```bash
git remote add origin https://github.com/<your-username>/simple-calculator-git-demo.git
git remote -v
git push -u origin main
git push origin feature/divide-by-zero feature/round-results
git pull
```
