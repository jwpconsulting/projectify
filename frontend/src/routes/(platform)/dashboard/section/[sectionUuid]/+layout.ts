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
import { error } from "@sveltejs/kit";

import { getSection } from "$lib/repository/workspace/section";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { SectionDetail } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { LayoutLoadEvent } from "./$types";
import { backOff } from "exponential-backoff";

interface Data {
    section: SectionDetail;
}

export async function load({
    params: { sectionUuid },
}: LayoutLoadEvent): Promise<Data> {
    const section = await backOff(() => getSection(sectionUuid));
    if (!section) {
        error(
            404,
            `The section with UUID '${sectionUuid}' could not be found`,
        );
    }
    const project = section.project;
    const { uuid: workspaceUuid } = unwrap(
        project.workspace,
        "Expected workspace",
    );
    currentWorkspace.loadUuid(workspaceUuid).catch((reason: unknown) => {
        console.error(
            "Tried to load currentWorkspace in background, but failed with",
            reason,
        );
    });
    return { section };
}

export const prerender = false;
// TODO Maybe we can set this to true at some point and have SSR support
export const ssr = false;
