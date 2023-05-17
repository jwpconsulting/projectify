import type { Meta, StoryObj } from "@storybook/svelte";
import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";

import { squovalIcons, squovalStates } from "$lib/funabashi/types";

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
    args: {
        action: { kind: "button", action: console.log },
        state: "active",
        icon: "plus",
    },
};
export default meta;

type Story = StoryObj<SquovalIcon>;

export const Default: Story = {
    args: {
        active: false,
    },
};

export const Active: Story = {
    args: {
        active: true,
    },
};
