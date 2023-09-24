import type { Meta, StoryObj } from "@storybook/svelte";

import { task, workspaceBoardSection, workspaceBoard } from "$lib/storybook";

import TopBar from "$lib/figma/screens/task/TopBar.svelte";

const meta: Meta<TopBar> = {
    component: TopBar,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<TopBar>;

export const Default: Story = {
    args: {
        breadcrumb: {
            task,
            workspaceBoardSection: {
                ...workspaceBoardSection,
                workspace_board: workspaceBoard,
            },
        },
    },
};

export const NoTask: Story = {
    args: {
        breadcrumb: {
            workspaceBoardSection: {
                ...workspaceBoardSection,
                workspace_board: workspaceBoard,
            },
        },
    },
};
