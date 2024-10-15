// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import TabElement from "$lib/figma/buttons/TabElement.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TabElement> = {
    component: TabElement,
    argTypes: {
        active: {
            control: "boolean",
        },
        href: {
            control: "text",
        },
        label: {
            control: "text",
        },
    },
};
export default meta;

type Story = StoryObj<TabElement>;

export const Default: Story = {
    args: {
        href: "/",
        label: "Team members",
        active: true,
    },
};
