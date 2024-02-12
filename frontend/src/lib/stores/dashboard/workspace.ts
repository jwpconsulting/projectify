// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { getWorkspace, getWorkspaces } from "$lib/repository/workspace";
import { createHttpStore } from "$lib/stores/httpSubscription";
import { createWsStore } from "$lib/stores/wsSubscription";
import type { Workspace } from "$lib/types/workspace";

export const currentWorkspace = createWsStore("workspace", getWorkspace);

export const currentWorkspaces = createHttpStore<Workspace[]>(getWorkspaces);
