# 🏗️ Tech Stack Brain

Welcome to the **Tech Stack Brain**. This repository is Tier 2 of the 3-Tier AI-KMS Architecture.

This repository serves as the **Rulebook** for your specific technological stack. It defines *how* software is built, what coding standards are enforced, and how deployments are orchestrated in your ecosystem.

## 📦 What's Inside?

- **`02-Project-Architecture/`**: Core architectural paradigms (e.g., Facade patterns, Interface decoupling) and Architecture Decision Records (ADRs).
- **`03-Project-Coding/`**: The language-specific idioms (Go, Rust, Python) and documentation requirements.
- **`04-Project-Deployment/`**: Infrastructure rules, Docker strategies, and CI/CD lifecycles.
- **`05-Project-Scripts/`**: Universal automation scripts (e.g., modular build wrappers and repo validators).

## 🔗 How it connects to the Ecosystem

This repository is completely devoid of specific business logic or active AI workflows. It is meant to be injected as a **Git Submodule** into a master `obsidian-brain` project.

When an AI Agent (like the Developer or DevOps role) processes a task, it reads the rules defined in this repository to ensure the code it generates perfectly aligns with your engineering standards.

For detailed instructions on modifying and extending this stack, please read the **[[User-Manual.md]]**.
