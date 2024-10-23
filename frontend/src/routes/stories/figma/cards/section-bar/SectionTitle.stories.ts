// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
import { mobileParameters, project, section } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SectionTitle> = {
    component: SectionTitle,
    argTypes: {
        open: {
            control: "boolean",
        },
    },
    args: {
        project,
        section,
        open: true,
    },
};
export default meta;

type Story = StoryObj<SectionTitle>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
