// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
export const teamMemberRoles = [
    "OBSERVER",
    "CONTRIBUTOR",
    "MAINTAINER",
    "OWNER",
] as const;
// TODO duplicated from types/workspace.ts
export type TeamMemberRole = (typeof teamMemberRoles)[number];
