// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK

import type { AnchorSize } from "$lib/funabashi/types";
import Anchor from "$lib/funabashi/typography/Anchor.svelte";
import { makeStorybookSelect } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Anchor> = {
    component: Anchor,
    args: {
        label: "This is a label",
        href: "#",
        size: "normal",
        openBlank: false,
    },
    argTypes: {
        size: makeStorybookSelect({
            Normal: "normal",
            Large: "large",
        } satisfies Record<string, AnchorSize>),
        href: { control: "text" },
        label: { control: "text" },
        openBlan: { control: "boolean" },
    },
};
export default meta;

type Story = StoryObj<Anchor>;

export const Default: Story = {};
export const OpenBlank: Story = {
    args: {
        openBlank: true,
    },
};
