# MATCS Class Group Report Output

This directory contains the Software Engineering class report rewritten using the visual/template structure of the previous Blockchain report.

## Main deliverable

- `report.tex` — MATCS report in Indonesian with English abstract.
- `arxiv.sty` — copied visual/template support file.
- `logo_ui.png` — copied title-page asset.

The complete source code, tests, experiment runner, documentation, UML sources, and this report are maintained at [github.com/sammtan/MATCS](https://github.com/sammtan/MATCS).

## Included content

- Current MATCS implementation and phases.
- Fixed-time and queue-aware controller design.
- Safety boundary and simulation-only scope.
- Project Plan and milestones.
- Five UML fundamentals plus supplementary UML views.
- Draft academic MoU.
- COCOMO estimation with assumptions.
- Function Point Analysis with assumptions.
- Automated test evidence.
- 80-run CSV/JSON experiment evidence and interpretation.

The Blockchain paper templates were not copied or modified. The original Blockchain report source was used only as a visual reference.

## Build

From this directory, with a LaTeX distribution installed:

```powershell
pdflatex -interaction=nonstopmode report.tex
pdflatex -interaction=nonstopmode report.tex
```

The report intentionally uses assumptions for MoU, COCOMO, and FPA that must be reviewed by the team and lecturer before formal submission.
