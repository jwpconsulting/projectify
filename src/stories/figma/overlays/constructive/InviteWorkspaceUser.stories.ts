import type { Meta, StoryObj } from "@storybook/svelte";

import InviteWorkspaceUser from "$lib/figma/overlays/constructive/InviteWorkspaceUser.svelte";
import { workspace } from "$lib/storybook";

const meta: Meta<InviteWorkspaceUser> = {
    component: InviteWorkspaceUser,
    args: { workspace },
};
export default meta;

type Story = StoryObj<InviteWorkspaceUser>;

export const Default: Story = {};
