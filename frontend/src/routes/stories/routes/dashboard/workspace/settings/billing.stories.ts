// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import {
    workspace,
    customer,
    makeStorybookSelect,
    trialCustomer,
    user1,
    customCustomer,
} from "$lib-stories/storybook";
import type { Customer } from "$lib/types/corporate";
import type { User } from "$lib/types/user";
import type { WorkspaceDetail } from "$lib/types/workspace";
import Billing from "$routes/(platform)/dashboard/workspace/[workspaceUuid]/settings/billing/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

// XXX duplicated because we can't import ./$types
interface PageData {
    user: User;
    workspace: WorkspaceDetail;
    customer: Customer;
}

const data = makeStorybookSelect<PageData>({
    "Paid customer": {
        user: user1,
        workspace,
        customer,
    },
    "Trial customer": {
        user: user1,
        workspace,
        customer: trialCustomer,
    },
    "Custom customer": {
        user: user1,
        workspace,
        customer: customCustomer,
    },
});

const meta: Meta<Billing> = {
    component: Billing,
    argTypes: { data },
    args: { data: "paid-customer" },
};
export default meta;

type Story = StoryObj<Billing>;

export const Trial: Story = { args: { data: "trial-customer" } };

export const Paid: Story = { args: { data: "paid-customer" } };

export const Custom: Story = { args: { data: "custom-customer" } };
