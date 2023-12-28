import type { Meta, StoryObj } from "@storybook/svelte";

import SignUp from "$routes/(storefront)/(auth)/user/sign-up/+page.svelte";

const meta: Meta<SignUp> = { component: SignUp };
export default meta;

type Story = StoryObj<SignUp>;

export const Default: Story = {};
