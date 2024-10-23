// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import {
    getWorkspace,
    getWorkspaces,
} from "$lib/repository/workspace/workspace";
import { createHttpStore } from "$lib/stores/httpSubscription";
import { createWsStore } from "$lib/stores/wsSubscription";

export const currentWorkspace = createWsStore("workspace", getWorkspace);

export const currentWorkspaces = createHttpStore(getWorkspaces);
