---
name: commit
description: Execute `git commit` following conventions
---

# git commit

## Usage Modes

1. Commit recent changes

  When user declares `/commit` slash command, or naturally says "commit recent changes", detect which files and hunks should be committed according to the context.

2. Commit specific files

  When user declares files as arguments, like `/commit <file1> <file2>`, stage and commit ONLY the declared files, ignoring other staged or unstaged changes.

## Steps

1. Determine the files to be committed

  - The files that user specified.
  - Or, run `git status` and analyze the changes correlations to identify the files.

2. Stage the files

  - Run `git add <files>` for the files to be committed.
  - Run `git add -p` to stage the files hunks interactively if necessary.

3. Review changes

  - Run `git diff --staged` to review the changes will be committed, understand the content and purpose according to the context.

4. Generate commit message

5. Commit

  Run `git commit -m "<commit message>"`

## Commit Message Conventions

### Specification

```
<type>[optional scope]: <description>

[optional body]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes only
- `style`: Code style formatting only
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test changes
- `build`: Build system changes
- `ci`: Continuous integration configuration changes
- `chore`: Maintenance tasks
- `revert`: Revert a previous commit

### Scope

A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g., feat(parser): add ability to parse arrays.

### Description

Changes described in the commit message.

### Body

The body is the rest of the commit message, it is optional and is used to provide additional context and information about the changes.

### Specification Points

The key words "MUST", "MUST NOT”, "REQUIRED”, "SHALL”, "SHALL NOT”, "SHOULD”, "SHOULD NOT”, "RECOMMENDED”, "MAY”, and "OPTIONAL” in this document are to be interpreted as described in RFC 2119.

- Commits MUST be prefixed with a type, which consists of a noun, `feat`, `fix`, etc., followed by the OPTIONAL scope, OPTIONAL `!`, and REQUIRED terminal colon and space.
- The type `feat` MUST be used when a commit adds a new feature to your application or library.
- The type `fix` MUST be used when a commit represents a bug fix for your application.
- A scope MAY be provided after a type. A scope MUST consist of a noun describing a section of the codebase surrounded by parenthesis, e.g., `fix(parser):`
- A description MUST immediately follow the colon and space after the type/scope prefix. The description is a short summary of the code changes, e.g., `fix: array parsing issue when multiple spaces were contained in string`.
- A longer commit body MAY be provided after the short description, providing additional contextual information about the code changes. The body MUST begin one blank line after the description.
- A commit body is free-form and MAY consist of any number of newline separated paragraphs.
- If included in the type/scope prefix, breaking changes MUST be indicated by a `!` immediately before the `:`.
- Types other than `feat` and `fix` MAY be used in your commit messages, e.g., `docs: update ref docs`.
- Do NOT add `Co-Authored-By` trailers in commit messages

## Commands to Use

```bash
# Show git status
git status

# Show unstaged changes for a file
git diff <file>

# Show staged changes
git diff --staged

# Stage specific files
git add <file1> <file2>

# Create the commit
git commit -m "<commit message>"
```
