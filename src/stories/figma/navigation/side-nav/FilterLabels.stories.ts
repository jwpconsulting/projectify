import type { Meta, StoryObj } from "@storybook/svelte";

import FilterLabels from "$lib/figma/navigation/side-nav/FilterLabels.svelte";
import type { FilterLabelMenuState } from "$lib/figma/types";
import { makeStorybookSelect } from "$lib/storybook";

const states = makeStorybookSelect<FilterLabelMenuState>({
    List: "list",
    Create: "create",
});

const meta: Meta<FilterLabels> = {
    component: FilterLabels,
    argTypes: {
        state: states,
    },
};
export default meta;

type Story = StoryObj<FilterLabels>;

export const List: Story = {
    args: {
        state: "list",
    },
};
export const Create: Story = {
    args: {
        state: "create",
    },
};
