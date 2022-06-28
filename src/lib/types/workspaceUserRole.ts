export const workspaceUserRoles = [
    "OBSERVER",
    "MEMBER",
    "MAINTAINER",
    "OWNER",
] as const;
export type WorkspaceUserRole = typeof workspaceUserRoles;
