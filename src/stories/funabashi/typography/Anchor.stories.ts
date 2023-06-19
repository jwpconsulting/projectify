import type { Meta, StoryObj } from "@storybook/svelte";

import Anchor from "$lib/funabashi/typography/Anchor.svelte";

const meta: Meta<Anchor> = {
    component: Anchor,
    args: {
        label: "This is a label",
        href: "#",
        size: "normal",
    },
};
export default meta;

type Story = StoryObj<Anchor>;

export const Default: Story = {};
