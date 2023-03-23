import type { Meta, StoryObj } from "@storybook/svelte";

import ProfileContextMenu from "$lib/figma/overlays/context-menu/ProfileContextMenu.svelte";

const meta: Meta<ProfileContextMenu> = {
    component: ProfileContextMenu,
    argTypes: {},
};
export default meta;

type Story = StoryObj<ProfileContextMenu>;

export const Default: Story = {};
