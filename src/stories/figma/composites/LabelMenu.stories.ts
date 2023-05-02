import type { Meta, StoryObj } from "@storybook/svelte";

import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";

import { labelSearchModule } from "$lib/storybook";
import { filterLabelMenuStates } from "$lib/figma/types";

const meta: Meta<LabelMenu> = {
    component: LabelMenu,
    argTypes: {
        state: {
            control: "radio",
            options: filterLabelMenuStates,
        },
    },
    args: {
        labelSearchModule,
        cancelCreate: () => console.log("Cancelling creation"),
        savedLabel: () => console.log("Label was saved"),
    },
};
export default meta;

type Story = StoryObj<LabelMenu>;

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
