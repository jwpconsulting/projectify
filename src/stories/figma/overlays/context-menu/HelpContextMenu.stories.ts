import type { Meta, StoryObj } from "@storybook/svelte";

import HelpContextMenu from "$lib/figma/overlays/context-menu/HelpContextMenu.svelte";

const meta: Meta<HelpContextMenu> = {
    component: HelpContextMenu,
    argTypes: {},
};
export default meta;

type Story = StoryObj<HelpContextMenu>;

export const Default: Story = {};
