# Vera Secure Browser 🛡️

**Vera** is a specialized, high-security browser core designed from the ground up for environments that demand strict data privacy, zero footprint, and absolute administrative control—primarily **educational institutions (schools/exam halls)** and **military facilities**.

---

## 🚀 Key Architectural Pillars

### 1. Stateless & Ephemeral Mode (Zero-Trace Architecture)
* **No Local Persistence:** Vera leaves absolutely no trace on the physical device. 
* **RAM-Only Sessions:** All browsing data, cookies, cache, and history are dynamically handled within an isolated in-memory environment. 
* **Automatic Purging:** The moment the browser session terminates or an administrator triggers a kill-switch, all temporary session files are completely wiped from memory and storage.

### 2. Centralized Policy Engine (`vera_policy.json`)
* **Dynamic Access Control:** Administrators can easily enforce strict browsing rules via centralized configuration files or remote policy endpoints.
* **Blacklist & Whitelist Modes:** Effortlessly block unauthorized distractions (social media, gaming portals, streaming platforms) or lock down the browser to strictly approved educational/official domains (`*.edu.tr`, `meb.gov.tr`, `msb.gov.tr`).

### 3. Hardened Security & Anti-Leak Controls
* **Built-in Password Manager Disabled:** Completely strips out form auto-fill and password-saving capabilities to prevent credential leakage on shared public terminals.
* **Sandbox Enforcement:** Leverages strict isolation flags to contain web processes and block unauthorized developer tools or system introspection.

---

## 📂 Project Structure

```text
vera_browser/
│
├── vera_policy.json         # Centralized security policies, rules, and blacklists
├── policy_engine.py         # Core URL validation and policy enforcement module
├── ephemeral_storage.py     # RAM-based memory isolation and secure purge handler
└── README.md                # Project documentation and architecture guide
