import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceBoardSection from "$lib/figma/cards/WorkspaceBoardSection.svelte";
import {
    mobileParameters,
    workspaceBoard,
    workspaceBoardSection,
} from "$lib/storybook";

const meta: Meta<WorkspaceBoardSection> = {
    component: WorkspaceBoardSection,
    argTypes: {},
    args: {
        workspaceBoard,
        workspaceBoardSection,
    },
};
export default meta;

type Story = StoryObj<WorkspaceBoardSection>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
