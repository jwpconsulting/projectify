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
        count: makeStorybookSelect({
            "Unknown tasks assigned": undefined,
            "0 tasks assigned": 0,
            "1 task assigned": 209,
            "4909012 tasks assigned": 4909012,
        }),
        active: {
            control: "boolean",
        },
    },
    args: {
        active: true,
        count: "no-tasks-assigned",
        workspaceUserSelectionInput: workspaceUserSelectionInputs[2],
        onSelect: console.error,
        onDeselect: console.error,
    },
};
export default meta;

type Story = StoryObj<FilterUser>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
