// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import SelectProject from "$lib/figma/navigation/side-nav/SelectProject.svelte";
import { project } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SelectProject> = {
    component: SelectProject,
    argTypes: {},
    args: {
        project,
    },
};
export default meta;

type Story = StoryObj<SelectProject>;

export const Default: Story = {};
