# Codebase Task Proposals

## 1) Typo fix task
**Title:** Remove stray backslash before `<!DOCTYPE html>` in `index.html`.

**Why:** The first line is `\<!DOCTYPE html>` instead of `<!DOCTYPE html>`, which is a literal typo and can prevent standards mode parsing in some browsers/tools.

**Suggested acceptance criteria:**
- First line of `index.html` is exactly `<!DOCTYPE html>`.
- HTML validation no longer flags the malformed doctype.

---

## 2) Bug fix task
**Title:** Define missing CSS variables used by buttons and pricing text.

**Why:** `style.css` references `var(--ink)` and `var(--accent)`, but neither variable is defined in `:root`. This can cause unintended fallback rendering for primary buttons and price text.

**Suggested acceptance criteria:**
- Add `--ink` and `--accent` variables in `:root` (or replace the references with existing variables).
- Verify `.button--dark` and `.price` render with intended colors in browser.

---

## 3) Documentation/comment discrepancy task
**Title:** Update README to match this repository’s actual site and deployment details.

**Why:** `README.md` is currently generic GitHub Pages guidance and does not document this project’s concrete URL/configuration, while `index.html` already hardcodes the production URL in structured data (`https://papakaffey.github.io/Lostlegendsmetaldetect/`).

**Suggested acceptance criteria:**
- README includes project-specific deployment info (repo URL, expected Pages URL, branch/folder used).
- README includes a quick local preview instruction for maintainers.

---

## 4) Test improvement task
**Title:** Add lightweight automated checks for HTML/CSS validity in CI.

**Why:** The repo has no automated tests/checks; issues like malformed doctype and undefined CSS custom properties were not caught.

**Suggested acceptance criteria:**
- Add a CI workflow that runs on pull requests.
- Include at least one HTML validator/linter and one CSS linter (or custom property check).
- CI fails on malformed doctype and undefined CSS variables.
