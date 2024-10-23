// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Project from "$lib/figma/overlays/context-menu/Project.svelte";
import { project } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Project> = {
    component: Project,
    argTypes: {},
    args: { project },
};
export default meta;

type Story = StoryObj<Project>;

export const Default: Story = {};
