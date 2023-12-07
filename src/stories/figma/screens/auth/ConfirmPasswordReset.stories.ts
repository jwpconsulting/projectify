import type { Meta, StoryObj } from "@storybook/svelte";

import ConfirmPasswordReset from "$lib/figma/screens/auth/ConfirmPasswordReset.svelte";

const meta: Meta<ConfirmPasswordReset> = {
    component: ConfirmPasswordReset,
    args: {
        email: "",
        token: "",
        newPassword1: "",
        newPassword2: "",
    },
};
export default meta;

type Story = StoryObj<ConfirmPasswordReset>;

export const Default: Story = {};
