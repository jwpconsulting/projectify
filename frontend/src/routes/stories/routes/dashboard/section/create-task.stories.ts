// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import { section } from "$lib-stories/storybook";
import CreateTask from "$routes/(platform)/dashboard/section/[sectionUuid]/create-task/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<CreateTask> = {
    component: CreateTask,
    args: {
        data: {
            section,
        },
    },
};
export default meta;

type Story = StoryObj<CreateTask>;

export const Default: Story = {};
