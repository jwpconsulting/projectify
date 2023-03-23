import type { Meta, StoryObj } from "@storybook/svelte";

import PermissionsContextMenu from "$lib/figma/overlays/context-menu/PermissionsContextMenu.svelte";

const meta: Meta<PermissionsContextMenu> = {
    component: PermissionsContextMenu,
    argTypes: {},
};
export default meta;

type Story = StoryObj<PermissionsContextMenu>;

export const Default: Story = {};
