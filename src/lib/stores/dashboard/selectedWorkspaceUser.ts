import { internallyWritable } from "../util";

import type { WorkspaceUserSelection } from "$lib/types/ui";

const { priv: _selectedWorkspaceUser, pub: selectedWorkspaceUser } =
    internallyWritable<WorkspaceUserSelection>({
        kind: "allWorkspaceUsers",
    });
export { _selectedWorkspaceUser, selectedWorkspaceUser };
