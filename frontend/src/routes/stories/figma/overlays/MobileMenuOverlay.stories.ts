// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
import { makeStorybookSelect, mobileParameters } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const target = makeStorybookSelect({
    Landing: { kind: "landing" },
    Dashboard: { kind: "dashboard" },
    Continue: { kind: "continue" },
});

const meta: Meta<MobileMenuOverlay> = {
    component: MobileMenuOverlay,
    argTypes: {
        target,
    },
    args: {
        target: "landing",
    },
};
export default meta;

type Story = StoryObj<MobileMenuOverlay>;

export const Default: Story = {};

export const Mobile: Story = { parameters: mobileParameters };
