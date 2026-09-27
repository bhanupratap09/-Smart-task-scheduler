import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

output_text = """$ python main.py

============================
 SMART TASK SCHEDULER (CLI)
============================
1. Add task            6. Run scheduler (Greedy)
2. Edit task           7. Compare naive vs optimized
3. Remove task         8. Save tasks to file
4. List tasks          9. Load tasks from file
5. Load sample data    0. Exit
----------------------------
Choose an option: 6

==================================================
SCHEDULE SUMMARY
==================================================
Total tasks submitted : 6
Tasks scheduled       : 3
Tasks rejected        : 3
Success rate          : 50.0%
Total profit earned   : 370.00
==================================================

--------------------------------------------------
TIMELINE (Gantt view)
--------------------------------------------------
Slot 1: [T2] Fix critical bug      (profit 190.00)
Slot 2: [T1] Write report          (profit 100.00)
Slot 3: [T5] Deploy release        (profit 80.00)
--------------------------------------------------
"""

fig, ax = plt.subplots(figsize=(9, 6.5))
fig.patch.set_facecolor("#1e1e1e")
ax.set_facecolor("#1e1e1e")
ax.axis("off")
ax.text(0.02, 0.98, output_text, transform=ax.transAxes, fontfamily="monospace",
        fontsize=9.5, color="#d4d4d4", va="top", ha="left")

plt.tight_layout()
plt.savefig("cli_demo.png", dpi=150, facecolor="#1e1e1e")
print("Screenshot saved.")
