import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateEmail from "$lib/figma/screens/user-account-settings/UpdateEmail.svelte";

const meta: Meta<UpdateEmail> = {
    component: UpdateEmail,
    argTypes: {},
};
export default meta;

type Story = StoryObj<UpdateEmail>;

export const Default: Story = {};
