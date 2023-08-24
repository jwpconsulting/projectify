import type { Meta, StoryObj } from "@storybook/svelte";

import { user1 } from "$lib/storybook";

import Overview from "$lib/figma/screens/user-account-settings/Overview.svelte";

const meta: Meta<Overview> = {
    component: Overview,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Overview>;

export const Default: Story = {
    args: {
        user: user1,
    },
};
