import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import Access from "$lib/figma/navigation/header/Access.svelte";

const meta: Meta<Access> = {
    component: Access,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<Access>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
