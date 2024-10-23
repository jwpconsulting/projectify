// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Label from "$lib/figma/overlays/context-menu/Label.svelte";
import { labelAssignment } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Label> = {
    component: Label,
    args: { labelAssignment },
};
export default meta;

type Story = StoryObj<Label>;

export const Default: Story = {};
