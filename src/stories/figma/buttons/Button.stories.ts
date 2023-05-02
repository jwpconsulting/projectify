import type { Meta, StoryObj } from "@storybook/svelte";

import { Plus } from "@steeze-ui/heroicons";

import Button from "./Button.svelte";
import { buttonColors } from "$lib/figma/types";

const meta: Meta<Button> = {
    component: Button,
    args: {
        label: "Behold, for I am a label",
        color: "blue",
        action: () => console.log("Hello, World! I am a button."),
    },
    argTypes: {
        label: {
            control: "text",
        },
        color: {
            control: "radio",
            options: buttonColors,
        },
    },
};
export default meta;

export const Primary: StoryObj = {
    args: {
        style: { kind: "primary" },
    },
};

export const Secondary: StoryObj = {
    args: {
        style: {
            kind: "secondary",
        },
    },
};

export const TertiaryNoIcon: StoryObj = {
    args: {
        style: { kind: "tertiary", icon: null },
    },
};
export const TertiaryIconLeft: StoryObj = {
    args: {
        style: {
            kind: "tertiary",
            icon: { position: "left", icon: Plus },
        },
    },
};
export const TertiaryIconRight: StoryObj = {
    args: {
        style: {
            kind: "tertiary",
            icon: {
                position: "right",
                icon: Plus,
            },
        },
    },
};
