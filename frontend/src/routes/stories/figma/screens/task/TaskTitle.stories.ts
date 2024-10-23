// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TaskTitle> = {
    component: TaskTitle,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskTitle>;

export const Default: Story = {};
