## ✅ Project Overview
This project implements a production-grade Role-Based Access Control (RBAC) system with nested access layers using organizations and departments. It supports secure authentication, fine-grained role permissions, and shareable guest links — inspired by systems like Google Docs.


## 🏗 Architecture & Key Design Decisions
| Component              | Technology / Decision                                                                 |
|------------------------|---------------------------------------------------------------------------------------|
| *Framework*            | Chose *FastAPI/Django/Flask* for its rapid development, async support, and            |
|                        | auto-generated API docs.                                                              |
| *Authentication*       | Used *JWT* for stateless, scalable user sessions. Tokens include user roles and org   |
|                        | context.                                                                              |
| *Entities & Structure* | Designed a hierarchical model with Organizations → Departments → Users with           |
|                        |scoped roles.                                                                          |
| *RBAC Enforcement*     | Role-checking decorators and middleware determine access at the endpoint level.       |
| *Guest Access*         | Implemented a token-based guest link system using scoped JWT or signed tokens.        |
| *Storage & DB*         | Used *PostgreSQL* to maintain relational consistency across organizations, departments| 
|                        | and users.                                                                            |
| *Documentation*        | Used Swagger/OpenAPI or Postman collection for thorough API documentation and testing.|


## 🚧 Challenges Faced

| Area                     | Challenge Description                                                                 |
|--------------------------|---------------------------------------------------------------------------------------|
| *Role Scope Granularity* | Managing roles scoped by org/department required careful DB design and permission     |
|                          | checks.                                                                               |
| *Nested Access Logic*    | Implementing permission inheritance across departments under orgs was                 |
|                          | non-trivial.                                                                          |
| *Guest Token Security*   | Ensuring guest tokens were secure, scoped, and optionally expirable added             |
|                          | complexity.                                                                           |
| *User Experience*        | Designing role assignment flows and permission previews without a full frontend was   |
|                          | limiting during testing.                                                              |
| *Modular RBAC Logic*     | Deciding between hardcoded logic vs. adopting a rules engine like Casbin/             |
|                          | OpenFGA.                                                                              |


## 🧠 Key Learnings
- *RBAC isn't one-size-fits-all* — real-world systems require nested, scoped, and role-overridable logic.
- *Guest access flows* are often overlooked in standard RBAC, but essential for collaboration-focused apps.
- Building APIs that are *developer-friendly* and testable from Postman/Swagger saves debugging effort later.
- Importance of *abstracting permissions logic* into reusable middleware/decorators for maintainability.


## 🚀 Scope for Improvement
| Area                     | Improvement Opportunity                                                               |
|--------------------------|---------------------------------------------------------------------------------------|
| *RBAC Engine*            |Integrate OpenFGA or Casbin to allow dynamic policy evaluation rather than static role |
|                          |checks.                                                                                |
| *Frontend Interface*     |Build a full React/Vue UI to visualize org structure, role assignments, and guest link |
|                          |previews.                                                                              |
| *Audit Logging*          | Add audit logs for actions like role changes, resource updates, and guest accesses.   |
| *Token Revocation*       | Add support for expiring or revoking guest shareable links.                           |
| *OAuth Integration*      | Add OAuth2 (e.g., Google login) for enterprise readiness and identity federation.     |
| *Real-Time Updates*      | Add WebSocket support to notify users of permission changes in real-time.             |


## 📌 Conclusion
This RBAC system balances core access control principles with real-world collaboration needs. By combining org-level roles, nested departments, and guest links, it simulates how modern tools like Google Docs or Notion manage user access. The modularity of the backend allows for rapid enhancements, including rule engines, richer UI, and enterprise integrations.