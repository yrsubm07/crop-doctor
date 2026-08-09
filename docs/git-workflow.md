# Team Git workflow

## Permanent branches

- `main`: stable, demo-ready code only.
- `develop`: shared integration branch. Feature work is merged here first.

## Feature branches

- Member 1: `feature/frontend`
- Member 2: `feature/backend`
- Member 3: `feature/ml`
- Member 4: `feature/testing-docs`
- Member 5: `feature/integration-deployment`

## Daily workflow

1. Start from the latest `develop` branch.
2. Work only on your own feature branch.
3. Make a small, descriptive commit.
4. Push your branch to GitHub.
5. Open a pull request into `develop`.
6. Ask one teammate to review before merging.
7. Member 5 periodically tests `develop`; only a tested version moves to `main`.

## Commands

```powershell
# Get the latest shared work
git switch develop
git pull origin develop

# Create a feature branch once
git switch -c feature/frontend

# Check and save a focused change
git status
git add frontend/src
git commit -m "feat: add crop image upload interface"
git push -u origin feature/frontend
```

## Rules that prevent merge conflicts

1. Do not edit another member's area without discussing it first.
2. Pull from `develop` before starting work each day.
3. Keep commits small and focused on one change.
4. Never commit `node_modules`, `.venv`, uploaded images, datasets, secrets, or model files.
5. Do not use `git push --force` on shared branches.
6. If a merge conflict appears, stop and ask Member 5 before guessing.
