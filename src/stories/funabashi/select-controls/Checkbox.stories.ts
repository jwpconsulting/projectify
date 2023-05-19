import type { Meta, StoryObj } from "@storybook/svelte";

import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";

const meta: Meta<Checkbox> = {
    component: Checkbox,
    argTypes: {
        checked: {
            control: "boolean",
        },
        disabled: {
            control: "boolean",
        },
    },
    args: {
        checked: false,
        contained: false,
        disabled: false,
    },
};
export default meta;

type Story = StoryObj<Checkbox>;

export const Default: Story = {};
