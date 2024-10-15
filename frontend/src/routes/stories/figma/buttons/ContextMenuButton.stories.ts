// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
import type { MenuButtonColor } from "$lib/figma/types";
import { makeStorybookSelect } from "$lib-stories/storybook";
import { Search } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

const colors = makeStorybookSelect<MenuButtonColor>({
    Base: "base",
    Primary: "primary",
    Destructive: "destructive",
});

const iconSelect = makeStorybookSelect({
    "With icon": Search,
    "No icon": undefined,
});

const kinds = makeStorybookSelect({
    Button: { kind: "button", action: console.error },
    Anchor: { kind: "a", href: "#" },
});

const meta: Meta<ContextMenuButton> = {
    component: ContextMenuButton,
    argTypes: {
        label: { control: "text" },
        color: colors,
        icon: iconSelect,
        iconRight: iconSelect,
        kind: kinds,
        closeOnInteract: { control: "boolean" },
    },
    args: {
        label: "Hello world",
        icon: "with-icon",
        iconRight: "with-icon",
        kind: "anchor",
        color: "base",
        closeOnInteract: false,
    },
};
export default meta;

type Story = StoryObj<ContextMenuButton>;

export const Default: Story = {};
