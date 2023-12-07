import type { Meta, StoryObj } from "@storybook/svelte";

import LogIn from "$lib/figma/screens/auth/LogIn.svelte";

const meta: Meta<LogIn> = {
    component: LogIn,
};
export default meta;

type Story = StoryObj<LogIn>;

export const Default: Story = {};
