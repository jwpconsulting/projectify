import type { Meta, StoryObj } from "@storybook/svelte";

import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";

const meta: Meta<HeaderButton> = {
    component: HeaderButton,
    argTypes: {
        label: {
            control: "text",
        },
    },
    args: {
        label: "Button",
        action: { kind: "a", href: "/" },
    },
};

export default meta;

type Story = StoryObj<HeaderButton>;

export const Button: Story = {
    args: {
        type: { kind: "button" },
    },
};

export const Dropdown: Story = {
    args: {
        type: { kind: "dropdown", open: false },
    },
};
