// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import type { Meta, StoryObj } from "@storybook/svelte";

import {
    workspace,
    customer,
    makeStorybookSelect,
    trialCustomer,
    user1,
    customCustomer,
} from "$lib/storybook";
import type { Customer } from "$lib/types/corporate";
import type { User } from "$lib/types/user";
import type { Workspace } from "$lib/types/workspace";
import Billing from "$routes/(platform)/dashboard/workspace/[workspaceUuid]/settings/billing/+page.svelte";

// XXX duplicated because we can't import ./$types
interface PageData {
    user: User;
    workspace: Workspace;
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
