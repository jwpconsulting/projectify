// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import LogOut from "$routes/(storefront)/user/log-out/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<LogOut> = {
    component: LogOut,
};
export default meta;

type Story = StoryObj<LogOut>;

export const Default: Story = {};
