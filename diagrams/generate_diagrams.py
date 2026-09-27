"""
Generates all design diagrams for the project report as PNG files:
    - architecture.png     (System Architecture Diagram)
    - workflow.png         (Process Flow / Workflow Diagram)
    - usecase.png          (Use Case Diagram)
    - class_diagram.png    (Class Diagram)
    - sequence.png         (Sequence Diagram)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D

OUT_DIR = "."

BOX_STYLE = dict(boxstyle="round,pad=0.4", linewidth=1.5)


def box(ax, x, y, w, h, text, fc="#dbe9ff", ec="#2b5fad", fontsize=10, fontweight="normal"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                        linewidth=1.5, edgecolor=ec, facecolor=fc)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, wrap=True)


def arrow(ax, x1, y1, x2, y2, text=None, style="-|>", color="#333333", connectionstyle=None):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=15,
                         color=color, linewidth=1.3,
                         connectionstyle=connectionstyle)
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.15, text, ha="center", fontsize=8, color="#333333")


def new_fig(w=10, h=7):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------- #
# 1. System Architecture Diagram
# ---------------------------------------------------------------- #
def architecture_diagram():
    fig, ax = new_fig(10, 8.2)
    ax.set_title("System Architecture — Smart Task Scheduler", fontsize=13, fontweight="bold")

    box(ax, 3.5, 7.0, 3, 0.8, "User (CLI)", fc="#fff2cc", ec="#d6b656")
    box(ax, 3.5, 5.7, 3, 0.8, "main.py\n(CLI Controller)", fc="#e1d5e7", ec="#9673a6")

    box(ax, 0.3, 4.1, 2.7, 1.0, "Module 1\nTask Manager\n(task_manager.py)", fc="#dbe9ff", ec="#2b5fad")
    box(ax, 3.65, 4.1, 2.7, 1.0, "Module 2\nScheduling Engine\n(scheduler_engine.py)", fc="#dbe9ff", ec="#2b5fad")
    box(ax, 7.0, 4.1, 2.7, 1.0, "Module 3\nAnalytics/Reporting\n(analytics.py)", fc="#dbe9ff", ec="#2b5fad")

    box(ax, 0.3, 2.7, 9.4, 0.8,
        "Shared utilities:  validators.py   |   exceptions.py   |   logger_config.py",
        fc="#d5e8d4", ec="#82b366", fontsize=9)

    box(ax, 0.6, 1.3, 4.0, 0.8, "data/tasks.json\n(persisted task data)", fc="#f8cecc", ec="#b85450", fontsize=9)
    box(ax, 5.4, 1.3, 4.0, 0.8, "data/scheduler.log\n(rotating log file)", fc="#f8cecc", ec="#b85450", fontsize=9)

    ax.text(5, 0.4, "All three modules validate input and raise/handle exceptions via the shared utilities layer.",
            ha="center", fontsize=8, style="italic", color="#555555")

    arrow(ax, 5, 7.0, 5, 6.5)
    arrow(ax, 5, 5.7, 1.65, 5.1)
    arrow(ax, 5, 5.7, 5, 5.1)
    arrow(ax, 5, 5.7, 8.35, 5.1)
    arrow(ax, 1.65, 4.1, 2.5, 3.5)
    arrow(ax, 5, 4.1, 5, 3.5)
    arrow(ax, 8.35, 4.1, 7.5, 3.5)
    arrow(ax, 2.6, 2.7, 2.6, 2.1)
    arrow(ax, 7.4, 2.7, 7.4, 2.1)

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/architecture.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------- #
# 2. Workflow / Process Flow Diagram
# ---------------------------------------------------------------- #
def workflow_diagram():
    fig, ax = new_fig(10, 8.5)
    ax.set_title("Process Flow — Running the Scheduler", fontsize=13, fontweight="bold")

    steps = [
        ("Start CLI", 6.5),
        ("Add / load tasks\n(Module 1)", 5.6),
        ("Validate task data", 4.7),
        ("Invalid?\n→ show error, retry", 3.8),
        ("Run Greedy scheduling\nalgorithm (Module 2)", 2.9),
        ("Generate report\n(Module 3)", 2.0),
        ("Display summary,\ntimeline, rejected list", 1.1),
        ("Save results / exit", 0.2),
    ]
    for text, y in steps:
        box(ax, 3, y, 4, 0.75, text, fc="#dbe9ff", ec="#2b5fad", fontsize=9)

    for i in range(len(steps) - 1):
        y1 = steps[i][1]
        y2 = steps[i + 1][1] + 0.75
        arrow(ax, 5, y1, 5, y2)

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/workflow.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------- #
# 3. Use Case Diagram
# ---------------------------------------------------------------- #
def usecase_diagram():
    fig, ax = new_fig(10, 7)
    ax.set_title("Use Case Diagram — Smart Task Scheduler", fontsize=13, fontweight="bold")

    # Actor (stick figure, simplified)
    ax.plot([1.2], [5.3], marker="o", markersize=18, color="black", fillstyle="none")
    ax.plot([1.2, 1.2], [5.05, 4.3], color="black")
    ax.plot([0.8, 1.6], [4.8, 4.8], color="black")
    ax.plot([1.2, 0.8], [4.3, 3.8], color="black")
    ax.plot([1.2, 1.6], [4.3, 3.8], color="black")
    ax.text(1.2, 3.5, "User", ha="center", fontsize=10, fontweight="bold")

    use_cases = [
        ("Add Task", 5.9),
        ("Edit Task", 5.0),
        ("Remove Task", 4.1),
        ("List Tasks", 3.2),
        ("Run Scheduler", 2.3),
        ("View Report /\nAnalytics", 1.4),
        ("Save / Load\nTask Data", 0.5),
    ]
    for text, y in use_cases:
        e = Ellipse((6.2, y + 0.3), 3.6, 0.75, facecolor="#d5e8d4", edgecolor="#82b366", linewidth=1.5)
        ax.add_patch(e)
        ax.text(6.2, y + 0.3, text, ha="center", va="center", fontsize=9)
        arrow(ax, 1.9, 4.6, 4.4, y + 0.3, color="#888888")

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/usecase.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------- #
# 4. Class Diagram
# ---------------------------------------------------------------- #
def class_box(ax, x, y, w, h, title, attrs, methods):
    box(ax, x, y, w, h, "", fc="white", ec="#333333")
    title_h = 0.4
    ax.plot([x, x + w], [y + h - title_h, y + h - title_h], color="#333333", linewidth=1)
    body_split = y + h - title_h - (0.22 * len(attrs)) - 0.15
    ax.plot([x, x + w], [body_split, body_split], color="#333333", linewidth=1)

    ax.text(x + w / 2, y + h - title_h / 2, title, ha="center", va="center", fontsize=10, fontweight="bold")
    for i, a in enumerate(attrs):
        ax.text(x + 0.15, y + h - title_h - 0.15 - i * 0.22, a, ha="left", va="top", fontsize=7.5, family="monospace")
    for i, m in enumerate(methods):
        ax.text(x + 0.15, body_split - 0.15 - i * 0.22, m, ha="left", va="top", fontsize=7.5, family="monospace")


def class_diagram():
    fig, ax = new_fig(13, 8)
    ax.set_title("Class Diagram — Smart Task Scheduler", fontsize=13, fontweight="bold")

    class_box(ax, 0.5, 5.5, 3.0, 2.0, "Task",
              ["task_id: str", "name: str", "deadline: int", "profit: float"],
              ["__post_init__()"])

    class_box(ax, 4.5, 4.8, 3.6, 2.7, "TaskManager",
              ["_tasks: Dict[str, Task]"],
              ["add_task()", "edit_task()", "remove_task()",
               "list_tasks()", "save_to_file()", "load_from_file()",
               "load_sample_data()"])

    class_box(ax, 9.0, 5.5, 3.5, 2.0, "ScheduleResult",
              ["scheduled: List[Task]", "rejected: List[Task]",
               "slot_assignment: List"],
              ["total_profit", "success_rate"])

    class_box(ax, 4.5, 1.6, 3.6, 2.4, "SchedulerEngine\n(module functions)",
              [],
              ["schedule_naive(tasks)", "schedule_optimized(tasks)", "_DisjointSet"])

    class_box(ax, 9.0, 1.6, 3.5, 2.4, "Analytics\n(module functions)",
              [],
              ["summary_stats()", "format_summary()",
               "format_gantt()", "format_rejected()", "full_report()"])

    class_box(ax, 0.5, 1.6, 3.0, 2.0, "Exceptions",
              [],
              ["SchedulerError", "DuplicateTaskError", "TaskNotFoundError",
               "InvalidTaskDataError", "EmptyTaskListError"])

    arrow(ax, 3.5, 6.3, 4.5, 6.3, "uses")
    arrow(ax, 6.3, 4.8, 6.3, 4.0, "produces")
    arrow(ax, 8.1, 5.9, 9.0, 6.0, "returns")
    arrow(ax, 6.3, 1.6, 2.0, 2.0, "raises", connectionstyle="arc3,rad=-0.3")
    arrow(ax, 8.1, 2.8, 9.0, 2.8, "reads")

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/class_diagram.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------- #
# 5. Sequence Diagram
# ---------------------------------------------------------------- #
def sequence_diagram():
    fig, ax = new_fig(11, 7)
    ax.set_title("Sequence Diagram — Run Scheduler Flow", fontsize=13, fontweight="bold")

    actors = [
        ("User", 1),
        ("main.py", 3.3),
        ("TaskManager", 5.6),
        ("SchedulerEngine", 8.0),
        ("Analytics", 10.3),
    ]
    for name, x in actors:
        box(ax, x - 0.9, 6.2, 1.8, 0.6, name, fc="#e1d5e7", ec="#9673a6", fontsize=9)
        ax.plot([x, x], [0.3, 6.2], color="#999999", linestyle="--", linewidth=1)

    messages = [
        (1, 3.3, 5.6, "select 'Run scheduler'"),
        (3.3, 5.6, 5.2, "list_tasks()"),
        (5.6, 3.3, 4.8, "return List[Task]"),
        (3.3, 8.0, 4.4, "schedule_optimized(tasks)"),
        (8.0, 3.3, 4.0, "return ScheduleResult"),
        (3.3, 10.3, 3.6, "full_report(result)"),
        (10.3, 3.3, 3.2, "return formatted report"),
        (3.3, 1, 2.8, "display report"),
    ]
    for x1, x2, y, label in messages:
        arrow(ax, x1, y, x2, y, label, color="#333333")

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/sequence.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    architecture_diagram()
    workflow_diagram()
    usecase_diagram()
    class_diagram()
    sequence_diagram()
    print("All diagrams generated.")
