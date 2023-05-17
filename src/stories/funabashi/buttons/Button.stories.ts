import type { Meta, StoryObj } from "@storybook/svelte";

import { Plus } from "@steeze-ui/heroicons";

import Button from "./Button.svelte";
import { buttonColors } from "$lib/funabashi/types";
import type { ButtonAction, ButtonStyle } from "$lib/funabashi/types";

const styles: Record<string, ButtonStyle> = {
    primary: {
        kind: "primary",
    },
    secondary: {
        kind: "secondary",
    },
    tertiaryNoIcon: {
        kind: "tertiary",
        icon: null,
    },
    tertiaryIconLeft: {
        kind: "tertiary",
        icon: { position: "left", icon: Plus },
    },
    tertiaryIconRight: {
        kind: "tertiary",
        icon: { position: "right", icon: Plus },
    },
};

const actions: Record<string, ButtonAction> = {
    button: {
        kind: "button",
        action: () => console.log("Hello, World! I am a button."),
    },
    anchor: { kind: "a", href: "#" },
};

const meta: Meta<Button> = {
    component: Button,
    args: {
        label: "Behold, for I am a label",
        color: "blue",
    },
    argTypes: {
        label: {
            control: "text",
        },
        color: {
            control: "radio",
            options: buttonColors,
        },
        style: {
            defaultValue: "primary",
            options: Object.keys(styles),
            mapping: styles,
            control: {
                type: "radio",
                labels: {
                    primary: "Primary",
                    secondary: "Secondary",
                    tertiaryNoIcon: "Tertiary",
                    tertiaryIconLeft: "Tertiary Icon Left",
                    tertiaryIconRight: "Tertiary Icon Right",
                },
            },
        },
        action: {
            defaultValue: "button",
            options: Object.keys(actions),
            mapping: actions,
            control: {
                type: "radio",
                labels: {
                    button: "Button",
                    anchor: "Anchor",
                },
            },
        },
    },
};

export default meta;

export const Primary: StoryObj = {
    args: { action: "button", style: "primary" },
};

export const Secondary: StoryObj = {
    args: { action: "button", style: "secondary" },
};

export const TertiaryNoIcon: StoryObj = {
    args: { action: "button", style: "tertiaryNoIcon" },
};

export const TertiaryIconLeft: StoryObj = {
    args: { action: "button", style: "tertiaryIconLeft" },
};
export const TertiaryIconRight: StoryObj = {
    args: { action: "button", style: "tertiaryIconRight" },
};
