# Operational workflow evaluation: four synthetic, isolated tasks

This is an **opt-in evaluator** for workflow changes, not a research stage or a new
permission. The task package is synthetic, not a research dataset. Do not run the
Agent, train, download, render figures, or access SEALED data from CI.

## Usage

Create a **new, separate** workspace **outside** the PD-RW checkout:

    python -m evals.operational list
    python -m evals.operational prepare --case OP-RESEARCH --workspace /tmp/op-research
    python -m evals.operational grade --case OP-RESEARCH --workspace /tmp/op-research

Available cases: \`OP-RESEARCH\` (valid Run + confound), \`OP-OUTLOOK\`
(ambitious but conditional critical-review roadmap, outline only),
\`OP-EDIT\` (exact scoped manuscript correction), and \`OP-PERMISSION\`
(DEV-only data vs synthetic SEALED canary).

**Actual blind isolation** requires that the tested Agent can access **only the
exported workspace** and its approved tools. The grader checkout, hidden reference
code, repository history, grading tests and any real project sources must not be
mounted or retrievable by that Agent. Merely calling \`blind\` or putting a file in
a separate directory does **not** enforce filesystem or network isolation; the
external executor must supply that boundary.

Do not pass \`evals/\`, \`.git/\`, or scoring references into the Agent context.
The package includes the task text, synthetic input files and a public manifest,
never the grader's private scoring code. Any previous workspace is refused rather
than overwritten. Output belongs under \`outputs/\`.

## What is actually scored?

- Artifact tests independently verify fixture inputs stayed unchanged, no extra
  files were written, and submitted output satisfies the synthetic contract.
- Outlook validation checks **structure only**, not originality or scientific
  merit; a human reviewer must inspect vision, testability and evidence honesty.
- \`OP-EDIT\` requires a single exact synthetic correction; no rephrasing elsewhere.
- \`OP-PERMISSION\` contains a **fake canary**, no real SEALED data. Absence of
  canary in output does **not** prove the Agent did not read it.
- Optional \`--trace TRACE.json\` checks declared read/write paths from an
  independently instrumented execution. It checks **reported** events, not
  completeness or authentic origin. Without a genuine external tool interceptor,
  access compliance remains **NOT_CERTIFIED** even if the trace is clean.
- Never count these fixture tests as a real Agent run, Q2 result, or proven
  Token efficiency gain. Actual A/B requires matched model/authorization/budget,
  external usage telemetry, and reviewed scientific deliverables.

A synthetic trace example is:

    {"format":"pdrw-operational-trace-v1",
     "case_id":"OP-PERMISSION","capture_source":"EXTERNAL_INSTRUMENTED",
     "events":[{"type":"READ_FILE","path":"inputs/DEV.csv"}]}

Keep the true external trace outside the Agent-writable workspace, and grade it
from the evaluator side. Trace authenticity cannot be established by this file
format alone. Rules in [EVALUATION_POLICY.md](EVALUATION_POLICY.md) govern interpretation.
