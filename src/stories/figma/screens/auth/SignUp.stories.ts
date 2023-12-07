import type { Meta, StoryObj } from "@storybook/svelte";

import SignUp from "$lib/figma/screens/auth/SignUp.svelte";

const meta: Meta<SignUp> = {
    component: SignUp,
};
export default meta;

type Story = StoryObj<SignUp>;

export const Default: Story = {};
