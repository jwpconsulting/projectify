import type { Meta, StoryObj } from "@storybook/svelte";

import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
import {
    circleIconSizes,
    circleIconIcons,
    type ButtonAction,
} from "$lib/funabashi/types";
import { makeStorybookSelect } from "$lib/storybook";

const action = makeStorybookSelect<ButtonAction>({
    "Button": {
        kind: "button",
        action: () => console.log("Hello, World! I am a button."),
    },
    "Button Enabled": {
        kind: "button",
        action: () => console.log("Hello, World! I am a button."),
        disabled: false,
    },
    "Button Disabled": {
        kind: "button",
        action: () => console.log("Hello, World! I am a button."),
        disabled: true,
    },
    "Anchor": { kind: "a", href: "#" },
});

const meta: Meta<CircleIcon> = {
    component: CircleIcon,
    argTypes: {
        action: action,
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
    },
    args: {
        icon: circleIconIcons[0],
        size: "medium",
        action: "button",
    },
};
export default meta;

type Story = StoryObj<CircleIcon>;

export const Default: Story = {};
