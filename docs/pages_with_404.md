<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# 404 pages

Here are all the pages that could throw a 404 since they accept a [uuid] of
some sort:

- `onboarding/assign-task/<uuid:task_uuid>`
- `onboarding/new-label/<uuid:task_uuid>`
- `onboarding/new-task/<uuid:project_uuid>`
- `onboarding/new-project/<uuid:workspace_uuid>`
- `dashboard/task/<uuid:task_uuid>`
- `dashboard/workspace/<uuid:workspace_uuid>`
- `dashboard/project/<uuid:project_uuid>`
- `dashboard/section/<uuid:sectino_uuid>`

Here are some test links:

```
http://localhost:8000/onboarding/assign-task/does-not-exist
http://localhost:8000/onboarding/new-label/does-not-exist
http://localhost:8000/onboarding/new-task/does-not-exist
http://localhost:8000/onboarding/new-project/does-not-exist
http://localhost:8000/dashboard/task/does-not-exist
http://localhost:8000/dashboard/workspace/does-not-exist
http://localhost:8000/dashboard/project/does-not-exist
http://localhost:8000/dashboard/section/does-not-exist
```

The same domains using the production domain:

```
https://www.projectifyapp.com/onboarding/assign-task/does-not-exist
https://www.projectifyapp.com/onboarding/new-label/does-not-exist
https://www.projectifyapp.com/onboarding/new-task/does-not-exist
https://www.projectifyapp.com/onboarding/new-workspace-board/does-not-exist
https://www.projectifyapp.com/dashboard/task/does-not-exist
https://www.projectifyapp.com/dashboard/workspace/does-not-exist
https://www.projectifyapp.com/dashboard/workspace-board/does-not-exist
https://www.projectifyapp.com/dashboard/workspace-board-section/does-not-exist
```
