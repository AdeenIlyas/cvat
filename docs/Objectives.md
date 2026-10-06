# Objectives

## ID: MO-1
**Field** | **Entry**
---|---
**What is measured** | Response time of the new `/api/tasks/{id}/annotation_counts` API endpoint.
**How** | Network tab in browser developer tools measuring the time to fetch the counts data for a typical task.
**Target** | Median of 5 runs at or below **250 ms**.
**Conditions** | Chrome, cache disabled, local Docker stack, sample COCO 2017 validation data loaded, nothing else running.
**Not included** | Time to render the graph on the frontend.

**Justification:** 250ms is a standard benchmark for snappy API responses that don't block the UI thread unnecessarily. Given that counting annotations might involve scanning large database tables for complex tasks, an optimized query using `COUNT` and `GROUP BY` at the database level should easily clear this for small/medium datasets, but it's a tight enough constraint to ensure I don't write an N+1 query.
