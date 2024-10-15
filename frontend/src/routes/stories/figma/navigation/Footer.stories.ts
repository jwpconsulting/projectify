// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Footer from "$lib/figma/navigation/Footer.svelte";
import { mobileParameters } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Footer> = {
    component: Footer,
};
export default meta;

type Story = StoryObj<Footer>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
        // TODO consider if we don't want this in all our mobileParameters
        // This makes it easier to see if we have any unnecessary padding
        layout: "fullscreen",
    },
};
