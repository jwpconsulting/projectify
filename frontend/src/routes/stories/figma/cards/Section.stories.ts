// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Section from "$lib/figma/cards/Section.svelte";
import { mobileParameters, project, section } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Section> = {
    component: Section,
    argTypes: {},
    args: {
        project,
        section,
    },
};
export default meta;

type Story = StoryObj<Section>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
