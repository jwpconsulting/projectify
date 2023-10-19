import { Briefcase } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

import Filter from "$lib/figma/dropdown/Filter.svelte";
import { mobileParameters } from "$lib/storybook";

const meta: Meta<Filter> = {
    component: Filter,
    argTypes: {
        label: { control: "text" },
        open: { control: "boolean" },
    },
    args: {
        label: "This is a verrrrrrryyyyyyyyyy long label omGGGGGGG ITS SO LOOOONG",
        icon: Briefcase,
        open: true,
    },
};
export default meta;

type Story = StoryObj<Filter>;

export const Default: Story = {};

export const Mobile: Story = { parameters: mobileParameters };
