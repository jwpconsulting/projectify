// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { mobileParameters } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

import { constructiveOverlays } from "./config";
import ConstructiveOverlayTest from "./ConstructiveOverlayTest.svelte";

const meta: Meta<ConstructiveOverlayTest> = {
    component: ConstructiveOverlayTest,
    argTypes: {
        target: constructiveOverlays,
    },
    args: {
        target: "update-project",
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<ConstructiveOverlayTest>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
