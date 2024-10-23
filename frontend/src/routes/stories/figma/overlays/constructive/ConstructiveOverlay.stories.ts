// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

import { constructiveOverlays } from "../config";

const meta: Meta<ConstructiveOverlay> = {
    component: ConstructiveOverlay,
    argTypes: {
        target: constructiveOverlays,
    },
    args: {
        target: "update-project",
    },
};
export default meta;

type Story = StoryObj<ConstructiveOverlay>;

export const Default: Story = {};
