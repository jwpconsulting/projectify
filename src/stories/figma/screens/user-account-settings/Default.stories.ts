import type { Meta, StoryObj } from "@storybook/svelte";

import DefaultC from "$lib/figma/screens/user-account-settings/Default.svelte";

import { user1 } from "$lib/storybook";

const meta: Meta<DefaultC> = {
    component: DefaultC,
    argTypes: {},
};
export default meta;

type Story = StoryObj<DefaultC>;

export const Default: Story = {
    args: {
        user: user1,
    },
};
