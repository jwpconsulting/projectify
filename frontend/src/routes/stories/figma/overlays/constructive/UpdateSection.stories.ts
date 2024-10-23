// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import UpdateSection from "$lib/figma/overlays/constructive/UpdateSection.svelte";
import { section } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<UpdateSection> = {
    component: UpdateSection,
    args: { section },
};
export default meta;

type Story = StoryObj<UpdateSection>;

export const Default: Story = {};
