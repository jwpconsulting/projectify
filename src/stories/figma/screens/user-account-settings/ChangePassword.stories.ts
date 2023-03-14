import type { Meta, StoryObj } from "@storybook/svelte";

import ChangePassword from "$lib/figma/screens/user-account-settings/ChangePassword.svelte";

const meta: Meta<ChangePassword> = {
    component: ChangePassword,
    argTypes: {},
};
export default meta;

type Story = StoryObj<ChangePassword>;

export const Default: Story = {};
