# Debugging Log

This log records practical problems encountered while rebuilding my
computational research foundations. The purpose is not simply to document
errors, but to record how each problem was diagnosed, fixed, and verified.

---

## Case 1: `return` placed inside a loop

### Problem

While writing functions to process environmental observations, the function
returned before all observations had been processed.

### What I expected

The function should iterate through the complete dataset and return the final
result only after processing all records.

### What went wrong

`return` was placed inside the `for` loop. Python therefore exited the
function during the first relevant iteration.

### Diagnosis

I compared the intended workflow with the indentation structure and noticed
that the function terminated before the loop had completed.

### Fix

Moved `return` outside the loop.

### Verification

The function processed all observations and produced the expected output.

### Lesson

Indentation affects program logic, not just formatting. In particular,
`return` immediately terminates a function.

---

## Case 2: Execution order and stale variables

### Problem

A regression result was inconsistent even though the formula appeared
correct.

### What I expected

The intercept and predictions should reflect the slope calculated from the
current dataset.

### What went wrong

A variable from an earlier execution remained in memory and was used before
the updated slope calculation had been rerun.

### Diagnosis

I traced the dependency chain:

`data → means → slope → intercept → predictions → residuals → RMSE`

and identified that the calculations had not been rerun in the correct order.

### Fix

Reran the analysis from the beginning in dependency order.

### Verification

The intercept, predictions, residuals, and RMSE became internally consistent.

### Lesson

Interactive environments can preserve hidden state. Reproducible analysis
should not depend on previously executed cells or stale variables.

---

## Case 3: Missing Python dependency

### Problem

Running the analysis script produced:

`ModuleNotFoundError: No module named 'matplotlib'`

### What I expected

The script should generate plots using Matplotlib.

### What went wrong

The virtual environment existed, but Matplotlib had not yet been installed
inside that environment.

### Diagnosis

The error showed that Python could run the script but could not import the
required package.

### Fix

Installed Matplotlib inside the active `.venv`.

### Verification

The script imported Matplotlib successfully and generated the plots.

### Lesson

Source code alone is not enough for reproducibility. The software environment
and package dependencies must also be recorded.

---

## Case 4: Empty CSV file

### Problem

`pd.read_csv()` produced:

`pandas.errors.EmptyDataError: No columns to parse from file`

### What I expected

The CSV file should load into a pandas DataFrame.

### What went wrong

The file existed at the correct path but had been created without saved
content.

### Diagnosis

The error was `EmptyDataError` rather than `FileNotFoundError`, indicating
that pandas had found the file. I used the shell command `cat` to inspect the
file contents.

### Fix

Added the CSV data and saved the file before running the script again.

### Verification

`pd.read_csv()` successfully loaded the dataset and returned the expected
rows and columns.

### Lesson

A valid file path does not guarantee valid input data. File existence and
file contents are separate things to check.

---

## Case 5: Git commit author incorrectly configured

### Problem

Git initially recorded the local machine identity rather than my intended
name and email.

### What I expected

Commits should be attributed to my chosen Git identity.

### What went wrong

Git automatically used the computer's local username and hostname because
global identity settings had not been configured.

### Diagnosis

I inspected the commit author information and noticed that it did not match
the identity I wanted to use.

### Fix

Configured:

`git config --global user.name`

and

`git config --global user.email`

and amended the commit before pushing.

### Verification

The updated commit showed the intended author information.

### Lesson

Version-control metadata is part of research reproducibility and professional
project documentation.

---

## Case 6: GitHub password authentication failed

### Problem

A Git push over HTTPS could not be authenticated using an account password.

### What I expected

Git should authenticate and push the repository to GitHub.

### What went wrong

GitHub does not support normal account-password authentication for Git
operations over HTTPS.

### Diagnosis

The failure occurred during remote authentication rather than during the Git
commit process.

### Fix

Installed GitHub CLI, authenticated through the browser, and connected Git to
the GitHub account.

### Verification

`git push` completed successfully and the commit appeared in the remote
repository.

### Lesson

Local Git and remote GitHub authentication are separate parts of the
workflow.

---

## Case 7: README edited in the wrong directory

### Problem

Project-specific data documentation was accidentally added to the repository
root `README.md`.

### What I expected

The data description should belong to
`environmental-trend-analysis/README.md`.

### What went wrong

I edited a file with the correct name but at the wrong directory level.

### Diagnosis

`git diff README.md` showed that the changes were being made to the root
README.

### Fix

Used:

`git restore README.md`

to restore the root file, then added the documentation to the project-level
README.

### Verification

`git status` showed the intended project README as modified while the root
README was clean.

### Lesson

`git diff` is useful not only for reviewing changes, but also for detecting
changes made in the wrong location.

---

## Case 8: Changes existed but were not staged

### Problem

Git reported:

`no changes added to commit`

even though new files had been created.

### What I expected

The new analysis files and datasets should be included in the next commit.

### What went wrong

The files existed in the working directory but had not yet been added to the
staging area.

### Diagnosis

`git status` showed the distinction between untracked or modified files and
files under `Changes to be committed`.

### Fix

Used `git add` to stage the intended project files.

### Verification

`git status` and `git diff --staged --stat` showed the correct files ready
for commit.

### Lesson

Git has separate working-directory, staging, and committed states. A file can
exist locally without being part of the next commit.

---

## Case 9: Git diff opened in a pager

### Problem

After running `git diff`, the terminal displayed `(END)` or `...skipping...`
and appeared to stop responding normally.

### What I expected

The command should print the diff and return directly to the shell.

### What went wrong

Git opened the output in a pager because the diff was longer than the
terminal window.

### Diagnosis

The `(END)` marker indicated that the output was being viewed inside a pager
rather than that Git had crashed.

### Fix

Pressed `q` to exit the pager.

### Verification

The normal shell prompt returned.

### Lesson

Some command-line tools use pagers for long output. Understanding the shell
interface is part of effective debugging.

---

## Case 10: New project folder created at the wrong directory level

### Problem

`environmental-multivariable-analysis` was accidentally created inside
`environmental-trend-analysis`.

### What I expected

The two projects should be sibling directories under the repository root.

### What went wrong

The new directory was created while the wrong folder was selected.

### Diagnosis

The VS Code Explorer showed the new project nested inside the earlier
project.

### Fix

Moved the directory from the terminal using:

`mv environmental-trend-analysis/environmental-multivariable-analysis .`

### Verification

`ls` showed:

- `environmental-trend-analysis`
- `environmental-multivariable-analysis`

at the same directory level.

### Lesson

Understanding relative paths and the current working directory reduces file
organization errors.

---

## Emerging debugging workflow

Across these cases, a useful general process is:

1. Read the exact error message.
2. Identify which layer failed: code, data, environment, path, Git, or remote
   authentication.
3. Inspect the relevant state rather than guessing.
4. Make the smallest justified change.
5. Rerun the affected step.
6. Verify that the result is correct.
7. Record the cause and lesson if the issue is likely to recur.