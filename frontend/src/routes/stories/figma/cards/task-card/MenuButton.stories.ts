// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import MenuButton from "$lib/figma/cards/task-card/MenuButton.svelte";
import { task, section } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<MenuButton> = {
    component: MenuButton,
    args: {
        task,
        section,
    },
};
export default meta;

type Story = StoryObj<MenuButton>;

export const Default: Story = {};
