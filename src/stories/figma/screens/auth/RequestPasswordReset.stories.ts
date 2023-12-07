import type { Meta, StoryObj } from "@storybook/svelte";

import RequestPasswordReset from "$lib/figma/screens/auth/RequestPasswordReset.svelte";

const meta: Meta<RequestPasswordReset> = {
    component: RequestPasswordReset,
};
export default meta;

type Story = StoryObj<RequestPasswordReset>;

export const Default: Story = {};
