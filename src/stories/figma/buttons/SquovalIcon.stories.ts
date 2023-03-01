import SquovalIcon from "$lib/figma/buttons/SquovalIcon.svelte";

import type { Meta, StoryObj } from "@storybook/svelte";

import { squovalIcons, squovalStates } from "$lib/figma/types";

const meta: Meta<SquovalIcon> = {
    component: SquovalIcon,
    argTypes: {
        icon: {
            options: squovalIcons,
            control: {
                type: "radio",
            },
        },
        state: {
            options: squovalStates,
            control: {
                type: "radio",
            },
        },
    },
};
export default meta;

type Story = StoryObj<SquovalIcon>;

export const Default: Story = {
    args: {
        icon: "plus",
        state: "active",
        active: false,
    },
};

export const Active: Story = {
    args: {
        icon: "plus",
        state: "active",
        active: true,
    },
};
