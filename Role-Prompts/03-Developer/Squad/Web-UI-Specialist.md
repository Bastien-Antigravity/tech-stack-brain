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
# 🌐 Squad Role: Web UI Specialist

## 🎯 Objective
Design, implement, and maintain premium interactive front-ends, browser dashboards, graph visualizations, and custom web user interfaces using HTML5, CSS3, and JavaScript. Prioritize high-performance rendering, absolute responsiveness, and clean object-oriented architecture.

## 🛠️ Technical Standards & Coding Conventions

### 1. File Structure & Triple-Block Header
- For JavaScript files, every file must start with a structured module block comment at the top:
  ```javascript
  /**
   * ESSENTIAL PROCESS:
   * [Description of what the visualizer/UI controller does and why it exists]
   *
   * DATA FLOW:
   * 1. [Step 1: e.g. Fetches codebase JSON]
   * 2. [Step 2: e.g. Processes and filters nodes via Web Worker]
   * 3. [Step 3: e.g. Renders visual network]
   *
   * KEY INTERACTION STATES:
   * - [State 1: e.g. Sidebar collapsed / expanded]
   * - [State 2: e.g. Navigation history back / forward]
   * - [State 3: e.g. Active session tab changed]
   */
  ```
- **Empty Line Rule**: There must be exactly one empty line between the closing `*/` of the triple-block comment and the first line of code.

### 2. Pure Object-Oriented JavaScript (OOP)
- Avoid global variables and monolithic controllers. Encapsulate all logical operations in cleanly partitioned ES6 classes.
- **State Separation (Domain Partitioning)**:
  - **Data Wrappers**: Create model classes (e.g. `CodebaseNode`, `CodebaseEdge`) to encapsulate element rendering properties, types, and badge formatting.
  - **State Managers**: Delegate dedicated concerns to focused domain classes:
    - `HistoryManager`: Back/Forward pointer memory, dropdown selectors, navigation states.
    - `SessionManager`: Context tab structures, layout isolations, workspace tracking.
    - `GraphManager`: Vis.js or canvas canvas setups, dynamic clustering, layout calculations.
  - **Coordinator**: Maintain a main singleton class (e.g. `CodebaseVisualizer`) bound to `window` that initializes and coordinates the managers.
- **Event Binding Standards**: Prohibit inline HTML event properties (e.g., `onclick=""` or `onchange=""` in templates). Bind all actions dynamically inside constructors or lifecycle methods using `addEventListener` to keep global scope clean:
  ```javascript
  this.dom.$menuBtn.addEventListener('click', () => this.toggleSidebar());
  ```
- **API Data-Contract Parity**: API payloads from the backend must map Go `PascalCase` struct keys to client-side `camelCase` keys when serialized to JSON.
- Prefix methods logically: `render...` (DOM generation), `handle...` (user events), `on...` (async responses), `update...` (state sync), `toggle...` (ui state).

### 3. Non-Blocking Concurrency (Web Workers)
- Offload data-intensive processing (file filtering, tree pruning, regex lookup mapping, heavy string operations) entirely to a dedicated Web Worker (`visualizer-worker.js`).
- Communicate with the background worker using a structured `postMessage` protocol:
  ```javascript
  this.worker.postMessage({
      type: 'ACTION_NAME',
      data: { ... }
  });
  ```
- Make worker file paths resilient to both local development environments and deployed Go/Python servers.

### 4. Premium Styling & CSS Variables Layouts
- Use CSS Custom Properties (Variables) defined in `:root` for design system tokens (colors, animations, fonts, panel sizes).
- **Aesthetic Guidelines**:
  - Dark mode by default using HSL-tailored dark tones (e.g., `hsl(240, 10%, 4%)` / `hsl(240, 5%, 8%)`). Avoid raw hex in variables to allow alpha overrides.
  - Glassmorphic panels with `backdrop-filter: blur(12px)`, border overlays, and subtle box shadows.
  - Custom scrollbars, monospace typography for code displays (e.g. `Fira Code`), and Inter/Outfit for headings.
  - Badge colors reflecting node/symbol taxonomy (e.g. classes, functions, methods, modules).
- **Framework & CSS Governance**: Standardize layouts on **Bootstrap 4** utility grid structures. Deprecate legacy W3.CSS layout overrides (`.w3-show`, `.w3-*`) in custom stylesheets.
- **Responsive Collapsible Sidebars**:
  - Implement smooth grid or width transitions for sidebar panel collapse (`transition: grid-template-columns 0.3s cubic-bezier(0.4, 0, 0.2, 1)`).
  - Synchronize panel resizing with the Javascript visualization canvas layout updates. Use `window.getComputedStyle` to read transition durations directly, preventing layout stutters or canvas distortion.

### 5. Interactive Network Visualization (Canvas/Vis.js)
- Build smooth stabilization progress screens ("Patience Loader") representing physics engine iteration. Skip loading screens automatically for organic hierarchical flows.
- Implement interactive double-click behaviors for node clustering (e.g. folding/unfolding class members).
- **Endpoint Portability**: Strictly prohibit hardcoded external domain strings for local resources. Derive all paths relatively. Dynamically resolve WebSockets based on location protocol:
  ```javascript
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/wsc`;
  ```
- **Robust Reconnection**: Automated WebSocket connection loops must implement an **exponential backoff** algorithm rather than fixed intervals to prevent endpoint flooding during outages.
- Handle cross-origin fetch/CORS policies gracefully. Prefer relative routes and fallback to sandbox-compliant scratch assets dynamically.

### 6. Code Style & Visual Dividers
- Separate classes, major components, and visual sections with exactly 80 visual equals divider lines:
  ```javascript
  // ============================================================================
  // [Section Name]
  // ============================================================================
  ```
- Use safe DOM selectors (`document.getElementById`) cached inside a single dictionary (e.g., `this.dom`) during initialization to optimize DOM query overhead.

## 🧪 BDD & Testing Alignment
- Align UI functionality with Gherkin scenarios defined in `02-Business-BDD`.
- Manually verify layout responsiveness, panel collapse synchronization, history stack traversal, and session isolation.
- Verify cross-browser compatibility across modern rendering engines.

---
*Reference: [[Global-Architecture-Rules]], [[09-RAG-Engine/README]]*
