import type { Meta, StoryObj } from "@storybook/svelte";

// Now that's what I call lateral movement
import { makeStorybookSelect, mobileParameters } from "$lib/storybook";

import { contextMenus } from "./config";
import ContextMenuTest from "./ContextMenuTest.svelte";

const meta: Meta<ContextMenuTest> = {
    component: ContextMenuTest,
    argTypes: {
        type: makeStorybookSelect(contextMenus),
    },
    args: {
        type: "profile",
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<ContextMenuTest>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
