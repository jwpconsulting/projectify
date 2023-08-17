import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";

import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
import type { HeaderButtonType } from "$lib/funabashi/types";

const type = makeStorybookSelect<HeaderButtonType>({
    "Dropdown Closed": {
        kind: "dropdown",
        open: false,
    },
    "Dropdown Opened": {
        kind: "dropdown",
        open: true,
    },
    "Button": {
        kind: "button",
    },
});

const meta: Meta<HeaderButton> = {
    component: HeaderButton,
    argTypes: {
        type,
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
