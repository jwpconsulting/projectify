import type { Meta, StoryObj } from "@storybook/svelte";

import SideNav from "$lib/figma/navigation/SideNav.svelte";

import {
    labelSearchModule,
    mobileParameters,
    sideNavModule,
    workspaceBoardSearchModule,
    workspaceUserSearchModule,
} from "$lib/storybook";

const meta: Meta<SideNav> = {
    component: SideNav,
    argTypes: {
        open: {
            control: "boolean",
        },
    },
    args: {
        workspaceBoardSearchModule,
        workspaceUserSearchModule,
        labelSearchModule,
        sideNavModule,
        open: true,
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<SideNav>;

export const Default: Story = {};

export const Closed: Story = {
    args: {
        open: false,
    },
};

export const Mobile: Story = {
    parameters: mobileParameters,
};
