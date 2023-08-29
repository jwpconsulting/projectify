import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";

import type { AnchorSize } from "$lib/funabashi/types";
import Anchor from "$lib/funabashi/typography/Anchor.svelte";

const meta: Meta<Anchor> = {
    component: Anchor,
    args: {
        label: "This is a label",
        href: "#",
        size: "normal",
    },
    argTypes: {
        size: makeStorybookSelect({
            "Extra small": "extraSmall",
            "Small": "small",
            "Normal": "normal",
            "Large": "large",
        } satisfies Record<string, AnchorSize>),
        href: { control: "text" },
        label: { control: "text" },
    },
};
export default meta;

type Story = StoryObj<Anchor>;

export const Default: Story = {};
