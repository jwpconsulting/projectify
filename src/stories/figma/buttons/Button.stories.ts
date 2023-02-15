import { Plus } from "@steeze-ui/heroicons";

import type { ButtonStyle } from "$lib/figma/types";

import Button from "./Button.svelte";

export default {
    component: Button,
};

export const Primary = () => ({
    Component: Button,
    props: {
        style: { kind: "primary" },
    },
});

export const Secondary = () => ({
    Component: Button,
    props: {
        style: {
            kind: "secondary",
        },
    },
});

export const TertiaryNoIcon = () => ({
    Component: Button,
    props: {
        style: { kind: "tertiary", icon: null },
    },
});
export const TertiaryIconLeft = () => ({
    Component: Button,
    props: {
        style: {
            kind: "tertiary",
            icon: { position: "left", icon: Plus },
        },
    },
});
export const TertiaryIconRight = () => ({
    Component: Button,
    props: {
        style: {
            kind: "tertiary",
            icon: {
                position: "right",
                icon: Plus,
            },
        },
    },
});
