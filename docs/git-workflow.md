# Git Workflow Documentation

## Branching Strategy

This project follows a simple Git workflow:

- `main` - stable and release-ready code
- `dev` - development branch
- `feature/*` - branches for individual changes

## Workflow

```text
feature branch
      ↓
   commit
      ↓
    push
      ↓
 Pull Request
      ↓
     dev
      ↓
 Pull Request
      ↓
    main