// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TopBar from "$lib/figma/screens/task/TopBar.svelte";
import { task, section, project } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TopBar> = {
    component: TopBar,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<TopBar>;

export const Default: Story = {
    args: {
        breadcrumb: {
            task,
            section: {
                ...section,
                project: project,
            },
        },
    },
};

export const NoTask: Story = {
    args: {
        breadcrumb: {
            section: {
                ...section,
                project: project,
            },
        },
    },
};
