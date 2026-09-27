# Problem Statement

## Problem Statement

Manually deciding which tasks to prioritize when every task has a
deadline and a different value/profit is error-prone and rarely
optimal — people tend to work on whatever feels urgent rather than
whatever maximizes overall value. This project builds a scheduler that
applies the **Greedy Job Sequencing with Deadlines** algorithm to
automatically select and order a subset of tasks that maximizes total
profit, given that:

- Every task occupies exactly one discrete time slot.
- A task is only "worth" its profit if it is completed at or before
  its deadline.
- At most one task can run per time slot.

## Scope of the Project

**In scope:**
- Single-machine, single-slot-per-unit-time scheduling (one task per
  time slot; no task splitting or parallel execution).
- Deadlines and profits are known upfront (offline scheduling, not
  real-time/online scheduling).
- A command-line interface for data entry, scheduling, and reporting.
- Local JSON persistence and file-based logging.

**Out of scope:**
- Multi-resource / multi-machine scheduling.
- Tasks with variable durations (this model assumes unit-time tasks,
  the standard formulation of the Job Sequencing problem).
- A graphical or web front-end (may be a future enhancement).
- Real-time re-scheduling as new tasks arrive mid-execution.

## Target Users

- Students and professionals who want to understand and apply greedy
  algorithms to a practical scheduling problem.
- Anyone managing a short list of deadline-bound tasks (e.g. a daily
  to-do list) who wants a value-maximizing order, not just a
  deadline-sorted order.
- Evaluators/reviewers assessing correct application of Data
  Structures & Algorithms concepts (sorting, greedy strategy, Union-Find).

## High-Level Features

1. **Task Input Manager** — add, edit, remove, list, and validate
   tasks; persist to/load from JSON.
2. **Scheduling Engine** — Greedy Job Sequencing with Deadlines,
   implemented both as a naive O(n²) version and an optimized
   O(n log n) Union-Find version, for direct performance comparison.
3. **Analytics & Reporting** — schedule summary, Gantt-style timeline,
   success rate, rejected-task breakdown.

See `README.md` for setup/run instructions and the full project report
(submitted as PDF on the portal) for detailed requirements,
architecture, UML diagrams, and design rationale.
