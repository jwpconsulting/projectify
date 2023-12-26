import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace, makeStorybookSelect, user1 } from "$lib/storybook";
import type { User } from "$lib/types/user";
import type { Workspace } from "$lib/types/workspace";
import WorkspaceUsers from "$routes/(platform)/dashboard/workspace/[workspaceUuid]/settings/workspace-users/+page.svelte";

// XXX duplicated because we can't import ./$types
interface PageData {
    user: User;
    workspace: Workspace;
}

const data = makeStorybookSelect<PageData>({
    "Regular workspace": {
        user: user1,
        workspace,
    },
});

const meta: Meta<WorkspaceUsers> = {
    component: WorkspaceUsers,
    argTypes: { data },
    args: { data: "regular-workspace" },
};
export default meta;

type Story = StoryObj<WorkspaceUsers>;

export const RegularWorkspace: Story = { args: { data: "regular-workspace" } };
