import type { WorkspaceUserRole } from "$lib/types/workspaceUserRole";
import { workspaceUserRoles } from "$lib/types/workspaceUserRole";

export function getMessageNameForRole(
    $_: (id: string) => string,
    role: string,
) {
    // This casting should be done further upstream
    // TODO Justus 2022-09-29
    if (!workspaceUserRoles.includes(role as WorkspaceUserRole)) {
        throw new Error(`Expected valid role, got ${role}`);
    }
    return {
        OBSERVER: $_("roles.observer"),
        MEMBER: $_("roles.member"),
        MAINTAINER: $_("roles.maintainer"),
        OWNER: $_("roles.owner"),
    }[role as WorkspaceUserRole];
}
