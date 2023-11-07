import type { Meta, StoryObj } from "@storybook/svelte";

import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
import {
    mobileParameters,
    workspaceBoard,
    workspaceBoardSection,
} from "$lib/storybook";

const meta: Meta<Dashboard> = {
    component: Dashboard,
    args: {
        workspaceBoard: {
            ...workspaceBoard,
            workspace_board_sections: [workspaceBoardSection],
        },
    },
};
export default meta;

type Story = StoryObj<Dashboard>;

export const Default: Story = {};
export const Mobile: Story = { parameters: mobileParameters };
