// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { getProject } from "$lib/repository/workspace/project";
import { createWsStore } from "$lib/stores/wsSubscription";

export const currentProject = createWsStore("project", getProject);
