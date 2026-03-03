# Instance 3 — GitHub Collaboration Setup

This workspace is version-controlled with Git. You and your brother can push/pull changes.

---

## First Time Only: Connect to GitHub

### 1. Create a private GitHub repo

Go to https://github.com/new and create a **private** repository named something like:
- `openclaw-instance3`
- `ai-stack-instance3`
- whatever you prefer

**Don't** initialize it with README or .gitignore — we have those already.

Copy the repo URL (looks like `https://github.com/yourusername/openclaw-instance3.git`).

### 2. Add GitHub as the remote

```bash
cd /Volumes/ai-stack/openclaw-data-3/workspace
git remote add origin https://github.com/yourusername/openclaw-instance3.git
```

### 3. Rename the default branch (optional but recommended)

```bash
git branch -M main
```

### 4. Push to GitHub

```bash
git push -u origin main
```

You'll be prompted for your GitHub password or personal access token. 
- **Easier:** Create a [personal access token](https://github.com/settings/tokens) and use that as the password.
- **Better:** Set up [SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

## Daily Workflow: You & Your Brother

### Pulling updates

Before you start working, pull any changes your brother has made:

```bash
cd /Volumes/ai-stack/openclaw-data-3/workspace
git pull
```

### Making commits

```bash
# Edit files in the workspace (AGENTS.md, SOUL.md, etc.)

# Stage your changes
git add .

# Commit
git commit -m "Describe what you changed"

# Push to GitHub
git push
```

### Handling conflicts

If you both edit the same file:

```bash
git pull
# Resolve conflicts in the file
git add .
git commit -m "Resolve merge conflict in AGENTS.md"
git push
```

---

## Useful Commands

```bash
# Check status
git status

# See commit history
git log --oneline

# See what changed since last push
git log origin/main..HEAD

# Undo last commit (before push)
git reset --soft HEAD~1
```

---

## Tips

- **Pull before starting work** — always check for your brother's changes first
- **Commit frequently** — small, focused commits are easier to review
- **Write clear commit messages** — future-you will thank you 
- **Use branches for big changes** — `git checkout -b feature/new-thing`
- **Keep `.gitignore` updated** — add any generated files that shouldn't be tracked

---

## Troubleshooting

**"Permission denied" when pushing:**
- Use a personal access token instead of password: https://github.com/settings/tokens
- Or set up SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

**"Merge conflict":**
```bash
# See which files are in conflict
git status

# Edit the files, remove conflict markers (<<<<<<, ======, >>>>>> lines)
# Then:
git add .
git commit -m "Resolve conflicts"
git push
```

**"Need to undo a push":**
```bash
git reset --hard HEAD~1
git push -f  # dangerous! only if your brother hasn't pulled that commit
```

**"Want to see what your brother changed":**
```bash
git log --all --graph --oneline
git diff main origin/main  # differences between your local and remote
```

---

## Current Status

```
Repo: /Volumes/ai-stack/openclaw-data-3/workspace
Remote: (not yet configured — follow steps above)
Branch: main
Files tracked: AGENTS.md, SOUL.md, BOOTSTRAP.md, IDENTITY.md, HEARTBEAT.md, TOOLS.md, USER.md, README.md, .openclaw/workspace-state.json
```
