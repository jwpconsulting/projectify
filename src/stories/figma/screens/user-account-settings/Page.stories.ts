import type { Meta, StoryObj } from "@storybook/svelte";

import Page from "$lib/figma/screens/user-account-settings/Page.svelte";
import { user1 } from "$lib/storybook";

const meta: Meta<Page> = {
    component: Page,
    args: { user: user1 },
};
export default meta;

type Story = StoryObj<Page>;

export const Default: Story = {};
