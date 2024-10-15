// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import SignUp from "$routes/(storefront)/user/(auth)/sign-up/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SignUp> = { component: SignUp };
export default meta;

type Story = StoryObj<SignUp>;

export const Default: Story = {};
