import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import SideNavContextMenu from "$lib/figma/overlays/context-menu/SideNavContextMenu.svelte";

const meta: Meta<SideNavContextMenu> = {
    component: SideNavContextMenu,
    argTypes: {},
    args: { workspace },
};
export default meta;

type Story = StoryObj<SideNavContextMenu>;

export const Default: Story = {};
