// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import SubTaskLine from "$lib/figma/screens/task/SubTaskLine.svelte";
import { subTask } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SubTaskLine> = {
    component: SubTaskLine,
};
export default meta;

type Story = StoryObj<SubTaskLine>;

export const Default: Story = {
    args: {
        subTask,
    },
};
