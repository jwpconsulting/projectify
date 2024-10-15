// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import UpdateSubTasks from "$lib/figma/screens/task/UpdateSubTasks.svelte";
import { createSubTaskAssignment } from "$lib/stores/dashboard/subTaskAssignment";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<UpdateSubTasks> = {
    component: UpdateSubTasks,
    args: {
        subTaskAssignment: createSubTaskAssignment(),
    },
};
export default meta;

type Story = StoryObj<UpdateSubTasks>;

export const Default: Story = {};
