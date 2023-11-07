import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceBoardSections from "$lib/components/dashboard/WorkspaceBoardSections.svelte";
import {
    workspaceBoard,
    workspaceBoardSection,
    mobileParameters,
} from "$lib/storybook";

const meta: Meta<WorkspaceBoardSections> = {
    component: WorkspaceBoardSections,
    args: {
        workspaceBoard: {
            ...workspaceBoard,
            workspace_board_sections: [workspaceBoardSection],
        },
    },
};
export default meta;

type Story = StoryObj<WorkspaceBoardSections>;

export const Default: Story = {};
export const Mobile: Story = { parameters: mobileParameters };
