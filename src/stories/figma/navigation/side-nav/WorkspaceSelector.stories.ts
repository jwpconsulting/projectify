import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
import { workspace, mobileParameters } from "$lib/storybook";

const meta: Meta<WorkspaceSelector> = {
    component: WorkspaceSelector,
    args: {
        workspace,
        workspaces: [workspace],
        open: true,
    },
    parameters: mobileParameters,
};
export default meta;

type Story = StoryObj<WorkspaceSelector>;

export const Open: Story = {};

export const Closed: Story = { args: { open: false } };
