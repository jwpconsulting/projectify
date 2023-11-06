import type { Meta, StoryObj } from "@storybook/svelte";

import ArchivedWorkspaceBoard from "$lib/figma/cards/ArchivedWorkspaceBoard.svelte";
import { workspaceBoard, mobileParameters } from "$lib/storybook";

const meta: Meta<ArchivedWorkspaceBoard> = {
    component: ArchivedWorkspaceBoard,
    args: {
        workspaceBoard,
    },
};
export default meta;

type Story = StoryObj<ArchivedWorkspaceBoard>;

export const Default: Story = {};

export const Mobile: Story = { parameters: mobileParameters };
