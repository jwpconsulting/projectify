import type { Meta, StoryObj } from "@storybook/svelte";

import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";

import { circleIconSizes, circleIconIcons } from "$lib/figma/types";

const meta: Meta<CircleIcon> = {
    component: CircleIcon,
    argTypes: {
        icon: {
            options: circleIconIcons,
            control: {
                type: "radio",
            },
        },
        size: {
            options: circleIconSizes,
            control: {
                type: "radio",
            },
        },
        disabled: {
            control: "boolean",
        },
    },
    args: {
        icon: circleIconIcons[0],
        size: "medium",
        disabled: false,
        action: {
            kind: "button",
            action: console.error,
        },
    },
};
export default meta;

type Story = StoryObj<CircleIcon>;

export const Default: Story = {};
