import type { Meta, StoryObj } from "@storybook/svelte";

import Billing from "$lib/figma/screens/workspace-settings/Billing.svelte";
import {
    workspace,
    customer,
    makeStorybookSelect,
    trialCustomer,
} from "$lib/storybook";
import type { Customer } from "$lib/types/corporate";

const customers = makeStorybookSelect<Customer>({
    "Paid customer": customer,
    "Trial customer": trialCustomer,
});

const meta: Meta<Billing> = {
    component: Billing,
    argTypes: { customer: customers },
    args: { workspace, customer: "paid-customer" },
};
export default meta;

type Story = StoryObj<Billing>;

export const Default: Story = { args: { customer: "trial-customer" } };

export const Paid: Story = {};
