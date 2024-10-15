// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TaskDescription> = {
    component: TaskDescription,
    argTypes: {
        description: { control: "text" },
        readonly: { control: "boolean" },
    },
    args: {
        description: "This is a description",
        readonly: false,
    },
};
export default meta;

type Story = StoryObj<TaskDescription>;

export const Default: Story = {};
