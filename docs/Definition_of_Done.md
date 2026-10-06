# Definition of Done

- [ ] All three required documents (Plan, Objectives, Definition of Done) are created and committed.
- [ ] Backend Django app `test` is created and integrated.
- [ ] Endpoint `/api/tasks/{id}/annotation_counts` returns correct counts per class, checked against the sample task.
- [ ] Endpoint enforces CVAT login and task-level permissions.
- [ ] The "Analytics" tab/section renders a graph showing the annotation counts per class.
- [ ] The page handles the "no data" case cleanly (displays a specific empty state).
- [ ] The page handles failed requests cleanly (displays an error message).
- [ ] Objective MO-1 is measured with 5 runs, raw output saved in docs.
- [ ] Target for MO-1 is met, or if missed, the reason is written down.
- [ ] Added grouping feature beyond plain count (e.g., shape type) is functional.
- [ ] (Optional) Graph updates live via WebSocket.
- [ ] (Optional) Page recovers smoothly from connection drops.
- [ ] Decision record is written inside `Plan.md`.
- [ ] All code changes are committed incrementally with clear messages.
- [ ] Everything I did not finish is explicitly listed here or in the Plan.
