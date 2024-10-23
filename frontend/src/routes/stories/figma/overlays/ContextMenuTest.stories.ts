// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { makeStorybookSelect, mobileParameters } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

import { contextMenus } from "./config";
import ContextMenuTest from "./ContextMenuTest.svelte";

const meta: Meta<ContextMenuTest> = {
    component: ContextMenuTest,
    argTypes: {
        type: makeStorybookSelect(contextMenus),
    },
    args: {
        type: "profile",
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<ContextMenuTest>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
