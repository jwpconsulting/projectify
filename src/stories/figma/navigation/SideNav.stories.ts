import type { Meta, StoryObj } from "@storybook/svelte";

import SideNav from "$lib/figma/navigation/SideNav.svelte";

import {
    workspace,
    labelSearchModule,
    mobileParameters,
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
        workspace,
        workspaceUserSearchModule,
        labelSearchModule,
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
