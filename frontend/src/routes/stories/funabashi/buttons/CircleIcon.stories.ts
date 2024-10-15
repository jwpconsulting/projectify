// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
import type {
    CircleIconIcon,
    CircleIconSize,
    ButtonAction,
} from "$lib/funabashi/types";
import { makeStorybookSelect } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

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
        icon: makeStorybookSelect<CircleIconIcon>({
            Ellipsis: "ellipsis",
            Edit: "edit",
            Delete: "delete",
            Up: "up",
            Down: "down",
            Close: "close",
        }),
        size: makeStorybookSelect<CircleIconSize>({
            Medium: "medium",
        }),
    },
    args: {
        icon: "ellipsis",
        size: "medium",
        action: "button",
    },
};
export default meta;

type Story = StoryObj<CircleIcon>;

export const Default: Story = {};
