import type { WorkspaceUserRole } from "$lib/types/workspaceUserRole";
import { workspaceUserRoles } from "$lib/types/workspaceUserRole";

export function getMessageNameForRole(role: string) {
    // This casting should be done further upstream
    // TODO Justus 2022-09-29
    if (!workspaceUserRoles.includes(role as WorkspaceUserRole)) {
        throw new Error(`Expected valid role, got ${role}`);
    }
    return {
        OBSERVER: "roles.observer",
        MEMBER: "roles.member",
        MAINTAINER: "roles.maintainer",
        OWNER: "roles.owner",
    }[role as WorkspaceUserRole];
}
