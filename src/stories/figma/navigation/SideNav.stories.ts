import type { Meta, StoryObj } from "@storybook/svelte";

import SideNav from "$lib/figma/navigation/SideNav.svelte";

import {
    workspaceSearchModule,
    workspaceBoardSearchModule,
    workspaceUserSearchModule,
    labelSearchModule,
    mobileParameters,
} from "$lib/storybook";

const meta: Meta<SideNav> = {
    component: SideNav,
    argTypes: {},
    args: {
        workspaceSearchModule,
        workspaceBoardSearchModule,
        workspaceUserSearchModule,
        labelSearchModule,
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<SideNav>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
