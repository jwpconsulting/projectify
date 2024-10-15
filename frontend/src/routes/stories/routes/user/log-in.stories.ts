// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK

import { makeStorybookSelect } from "$lib-stories/storybook";
import LogIn from "$routes/(storefront)/user/(auth)/log-in/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const data = makeStorybookSelect({
    "With redirect": {
        redirectTo: "a/nested/url?yo",
    },
    "Without redirect": {
        redirectTo: undefined,
    },
});

const meta: Meta<LogIn> = {
    component: LogIn,
    argTypes: { data },
};
export default meta;

type Story = StoryObj<LogIn>;

export const Default: Story = {
    args: { data: { redirectTo: "with-redirect" } },
};

export const WithoutRedirect: Story = {
    args: { data: { redirectTo: "without-redirect" } },
};
