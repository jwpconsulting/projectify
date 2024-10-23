// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import LabelRadio from "$lib/figma/navigation/side-nav/filter-labels/LabelRadio.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<LabelRadio> = {
    component: LabelRadio,
    argTypes: {},
};
export default meta;

type Story = StoryObj<LabelRadio>;

export const Default: Story = {};
