// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

import { destructiveOverlays } from "./config";

const meta: Meta<DestructiveOverlay> = {
    component: DestructiveOverlay,
    argTypes: { target: destructiveOverlays },
    args: { target: "delete-project" },
};
export default meta;

type Story = StoryObj<DestructiveOverlay>;

export const Default: Story = {};
