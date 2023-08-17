import type { Meta, StoryObj } from "@storybook/svelte";

import {
    makeStorybookSelect,
    mobileParameters,
    workspaceUserSelectionInputs,
} from "$lib/storybook";

import FilterUser from "$lib/figma/select-controls/FilterUser.svelte";
import type { WorkspaceUserSelectionInput } from "$lib/types/ui";

const meta: Meta<FilterUser> = {
    component: FilterUser,
    argTypes: {
        workspaceUserSelectionInput:
            makeStorybookSelect<WorkspaceUserSelectionInput>({
                "Unassigned": workspaceUserSelectionInputs[0],
                "All workspace users": workspaceUserSelectionInputs[1],
                "Workspace user": workspaceUserSelectionInputs[2],
            }),
        count: {
            control: "number",
        },
        active: {
            control: "boolean",
        },
    },
    args: {
        active: true,
        count: 20,
        workspaceUserSelectionInput: workspaceUserSelectionInputs[2],
    },
};
export default meta;

type Story = StoryObj<FilterUser>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
