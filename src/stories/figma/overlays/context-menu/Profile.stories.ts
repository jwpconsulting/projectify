import type { Meta, StoryObj } from "@storybook/svelte";

import Profile from "$lib/figma/overlays/context-menu/Profile.svelte";

const meta: Meta<Profile> = {
    component: Profile,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Profile>;

export const Default: Story = {};
