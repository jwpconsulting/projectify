import type { Meta, StoryObj } from "@storybook/svelte";

import Workspace from "$lib/figma/overlays/context-menu/Workspace.svelte";
import { workspace } from "$lib/storybook";

const meta: Meta<Workspace> = {
    component: Workspace,
    argTypes: {},
    args: { workspaces: [workspace] },
};
export default meta;

type Story = StoryObj<Workspace>;

export const Default: Story = {};
