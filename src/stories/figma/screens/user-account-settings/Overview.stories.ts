import type { Meta, StoryObj } from "@storybook/svelte";

import Overview from "$lib/figma/screens/user-account-settings/Overview.svelte";
import { user1 } from "$lib/storybook";

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
