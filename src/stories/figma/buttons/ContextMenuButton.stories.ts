import { Search } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
import type { MenuButtonColor, MenuButtonState } from "$lib/figma/types";
import { makeStorybookSelect } from "$lib/storybook";

const states = makeStorybookSelect<MenuButtonState>({
    Normal: "normal",
    Accordion: "accordion",
});

const colors = makeStorybookSelect<MenuButtonColor>({
    Base: "base",
    Primary: "primary",
    Destructive: "destructive",
});

const meta: Meta<ContextMenuButton> = {
    component: ContextMenuButton,
    argTypes: {
        label: { control: "text" },
        state: states,
        color: colors,
    },
    args: {
        label: "Hello world",
        icon: Search,
        state: "normal",
        kind: { kind: "a", href: "#" },
        color: "base",
    },
};
export default meta;

type Story = StoryObj<ContextMenuButton>;

export const Default: Story = {};
