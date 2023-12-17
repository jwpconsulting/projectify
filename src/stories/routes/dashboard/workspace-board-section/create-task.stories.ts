import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoard, workspaceBoardSection } from "$lib/storybook";
import type { WorkspaceBoardSectionDetail } from "$lib/types/workspace";
import CreateTask from "$routes/(platform)/dashboard/workspace-board-section/[workspaceBoardSectionUuid]/create-task/+page.svelte";

const meta: Meta<CreateTask> = {
    component: CreateTask,
    args: {
        data: {
            workspaceBoardSection: {
                ...workspaceBoardSection,
                workspace_board: workspaceBoard,
            } satisfies WorkspaceBoardSectionDetail,
        },
    },
};
export default meta;

type Story = StoryObj<CreateTask>;

export const Default: Story = {};
