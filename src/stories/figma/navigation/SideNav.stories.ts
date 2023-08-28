import type { Meta, StoryObj } from "@storybook/svelte";

import {
    workspace,
    mobileParameters,
    workspaceUserSearchModule,
} from "$lib/storybook";

import SideNav from "$lib/figma/navigation/SideNav.svelte";

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
