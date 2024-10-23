// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
/**
 * Repository functions for sections
 */
import { openApiClient } from "$lib/repository/util";
import type { SectionDetail } from "$lib/types/workspace";

// Read
export async function getSection(
    section_uuid: string,
): Promise<SectionDetail | undefined> {
    const { error, data } = await openApiClient.GET(
        "/workspace/section/{section_uuid}",
        { params: { path: { section_uuid } } },
    );
    if (error?.code === 404) {
        return undefined;
    }
    if (data) {
        return data;
    }
    console.error(error);
    throw new Error("Could not fetch section");
}
