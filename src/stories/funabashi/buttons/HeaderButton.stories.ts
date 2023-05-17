import type { Meta, StoryObj } from "@storybook/svelte";

import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
import { headerButtonTypes } from "$lib/funabashi/types";

const meta: Meta<HeaderButton> = {
    component: HeaderButton,
    argTypes: {
        type: {
            control: "radio",
            options: headerButtonTypes,
        },
        open: {
            control: "boolean",
        },
        label: {
            control: "text",
        },
    },
    args: {
        label: "Button",
        open: true,
    },
};

export default meta;

type Story = StoryObj<HeaderButton>;

export const Button: Story = {
    args: {
        type: "button",
    },
};

export const Dropdown: Story = {
    args: {
        type: "dropdown",
    },
};
