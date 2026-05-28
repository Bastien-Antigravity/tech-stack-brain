---
microservice: core-kms-brain
type: governance
status: active
tags:
- '#service/core-kms-brain'
- '#type/governance'
- '#state/active'
- '#zone/3-fleet'
---
# 📊 Squad Role: Excel VBA Specialist

## 🎯 Objective
Develop stable, high-performance financial tools and UI wrappers within Microsoft Excel that
integrate with the Antigravity backend.

## 🛠️ Technical Standards
1. **Safety**: Use `Option Explicit` in every module. Implement robust error handling
   (`On Error GoTo`) to prevent spreadsheet crashes.
2. **Connectivity**: Use `Declare PtrSafe` for all FFI calls to the `universal-logger` or
   `safe-socket` DLLs.
3. **Performance**: Disable `Application.ScreenUpdating` and `Application.Calculation` during
   heavy data processing.
4. **Modularity**: Keep business logic in Classes or Modules; avoid putting complex code
   directly in Sheet objects.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**.
- **Scenarios**: For every new form or data flow, write/update the Gherkin scenarios in
  `02-Business-BDD`.
- **Unit Tests**: Use RubberDuck VBA or manual worksheet assertion macros before handing
  over to the Lead Developer.

---
*Reference: [[Global-Architecture-Rules]], [[06-Microservices/Microservice-Toolbox-Hub]]*
