# Plan: Annotation Analytics Assessment

## Goal
Add annotation analytics to CVAT, providing class-level counts for a specific task and presenting them as a graph.

## Approach
The work will be done in the `test` Django app on the backend, and integrated into the CVAT UI on the frontend.

### Order of Work & Estimated Time (Total 8 Hours)
1. **Setup & Documentation (1 hour)**
   - Initial review of the codebase to locate where endpoints should live and where the frontend components are structured.
   - Setup Django app `test`.
   - Write and commit the initial `Plan.md`, `Objectives.md`, and `Definition_of_Done.md`.
2. **Backend: API Endpoint (2 hours) (Req 1, 5, 6, 7)**
   - Determine how annotations are stored (models: `LabeledShape`, `LabeledTrack`, `LabeledImage`, `Task`, `Label`).
   - Create a new endpoint `/api/tasks/{id}/annotation_counts` inside `test` app, properly integrated with CVAT router.
   - Ensure the endpoint enforces CVAT authentication and permissions (Req 5).
   - Implement the grouping/counting logic. Add an optional grouping beyond plain count (e.g., shape type: rectangle vs polygon) (Req 7).
   - Profile/measure the endpoint performance to meet the target (Req 6).
3. **Frontend: UI Integration (2 hours) (Req 2, 3)**
   - Find the task details page component (likely React based).
   - Add a new tab or section for "Analytics".
   - Create a React component that fetches data from the new endpoint.
   - Use a charting library (like ECharts or Chart.js, which might already be in CVAT) to render a bar chart of class counts.
4. **Frontend: Error Handling & Edge Cases (1 hour) (Req 4)**
   - Implement empty state rendering when there are no annotations.
   - Implement error boundary/message if the API request fails.
5. **Real-time Updates & Resilience (1.5 hours) (Req 8, 9)** *[To be attempted if time permits]*
   - Look into CVAT's existing WebSocket or SSE infrastructure.
   - Try to pipe annotation change events to the analytics component.
6. **Final Review & Decision Record (0.5 hour) (Req 10)**
   - Clean up code.
   - Complete the Decision Record section in this Plan document.

## Decision Record
- **Backend Architecture**: Decided to use `TaskViewSet`'s `check_object_permissions` to handle the permission checks manually within a Functional Based View (FBV) in the `test` app. This allows reusing CVAT's robust OPA-based security without requiring complex rule additions or monkey-patching DRF routers.
- **Data Grouping**: Opted to add an extra dimension of grouping by `type` (e.g., polygon, rectangle, track, tag) in addition to just `label__name`. This provides richer analytics and satisfies the optional requirement for an extra level of grouping.
- **Frontend Charting**: Selected `react-chartjs-2` since `chart.js` is already present in `cvat-ui`'s `package.json`, avoiding the need to add new dependencies and ensuring UI consistency.
- **Development Workflow**: Due to the limitations of `docker-compose.yml` which pulls prebuilt images, used `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build` to compile both backend and frontend changes locally.

## What is omitted
- Advanced WebSocket real-time updates for the graph (to save time, focusing on REST API instead).
- Extra UI polish beyond `antd` standard components and `chart.js` default styling.
