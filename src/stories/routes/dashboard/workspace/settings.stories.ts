import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace, makeStorybookSelect, user1 } from "$lib/storybook";
import type { User } from "$lib/types/user";
import type { Workspace } from "$lib/types/workspace";
import Settings from "$routes/(platform)/dashboard/workspace/[workspaceUuid]/settings/+page.svelte";

// XXX duplicated because we can't import ./$types
interface PageData {
    user: User;
    workspace: Workspace;
}

const data = makeStorybookSelect<PageData>({
    Workspace: {
        user: user1,
        workspace,
    },
});

const meta: Meta<Settings> = {
    component: Settings,
    argTypes: { data },
    args: { data: "workspace" },
};
export default meta;

type Story = StoryObj<Settings>;

export const Default: Story = {};
