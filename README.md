# Cyber Escalation Chain Reaction Simulator

> A simulation model exploring how a single AI-induced cyber incident can spiral into cascading infrastructure failures — triggering civilian unrest and potential cyber warfare.

---

## Project Overview

This simulator models a **domino effect of failures** across AI-controlled civilian infrastructure when a cyber event (e.g., a water utility hack) disrupts one system and puts pressure on others.

Inspired by real-world incidents and hypothetical cyber war scenarios, the simulator demonstrates the **systemic risks of autonomous AI systems**, particularly when failure in one critical domain (like water, power, or hospitals) spreads to others.

This project supports the research titled:

**“Risk of AI Inducing Civilian Unrest and Cyber War”**

---

## Core Objectives

- Show how **AI-driven systems** can cause unexpected chain reactions during a failure
- Visualize **interdependency** of infrastructure (e.g., water → hospitals → power grid)
- Quantify **civilian impact**, system downtime, and time to failure
- Provide a **graphical simulation** for research posters, papers, and presentations

---

## What It Simulates

- **AI-managed infrastructure** like power grids, water utilities, hospitals, and finance
- A **trigger event** (cyberattack or AI glitch) starts a failure in one node
- Other systems fail over time due to dependencies and overload
- Tracks how long each system takes to fail and visualizes results

---

## Technologies Used

| Library       | Purpose                                  |
|---------------|-------------------------------------------|
| `SimPy`       | Discrete-event simulation (time modeling) |
| `NetworkX`    | Dependency graph of infrastructure        |
| `Matplotlib`  | Bar charts showing failure timelines      |

---

##  Example Scenario

```text
Initial trigger: AI system in water utility is hacked →
Hospitals that depend on clean water begin failing →
Electric grid faces overload from panic and reroutes →
Finance and transportation systems start to collapse
