import type { Meta, StoryObj } from "@storybook/svelte";

import ArchiveWorkspaceBoard from "$lib/figma/cards/ArchiveWorkspaceBoard.svelte";
import { workspaceBoard, mobileParameters } from "$lib/storybook";

const meta: Meta<ArchiveWorkspaceBoard> = {
    component: ArchiveWorkspaceBoard,
    args: {
        workspaceBoard,
    },
};
export default meta;

type Story = StoryObj<ArchiveWorkspaceBoard>;

export const Default: Story = {};

export const Mobile: Story = { parameters: mobileParameters };
