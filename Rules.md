PROJECT RULES

1. Do not invent requirements.
2. Do not modify the approved architecture without asking.
3. Do not modify ERD unless explicitly requested.
4. Reuse existing components when possible.
5. Keep code simple and maintainable.
6. Every feature must include error handling.
7. Every API must have clear request/response contracts.
8. Do not create unnecessary abstractions.
9. Before changing existing code, inspect related files first.
10. After implementation, report:
   - files changed
   - what was implemented
   - assumptions made
   - remaining issues

## Change Control

Any change to one of the following must be explicitly approved before implementation:

- Functional requirements
- Use Cases
- Database schema / ERD
- Component architecture
- Deployment architecture
- Public API contract
- Technology stack
- Core project structure

The agent must stop and request approval instead of silently changing them.