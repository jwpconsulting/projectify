import type { Meta, StoryObj } from "@storybook/svelte";

import TabElement from "$lib/figma/buttons/TabElement.svelte";

const meta: Meta<TabElement> = {
    component: TabElement,
    argTypes: {
        active: {
            control: "boolean",
        },
        href: {
            control: "text",
        },
        label: {
            control: "text",
        },
    },
};
export default meta;

type Story = StoryObj<TabElement>;

export const Default: Story = {
    args: {
        href: "/",
        label: "Members",
        active: true,
    },
};
