// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import SentEmailConfirmation from "$routes/(storefront)/user/sent-email-confirmation-link/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SentEmailConfirmation> = {
    component: SentEmailConfirmation,
};
export default meta;

type Story = StoryObj<SentEmailConfirmation>;

export const Default: Story = {};
