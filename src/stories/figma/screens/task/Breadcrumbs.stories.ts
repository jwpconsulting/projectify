import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";

import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";

// TODO
const choices = {
    "All links": [
        { label: "This is a label, it is long, and informative", href: "#" },
        {
            label: "This here is a label, it is long, and informative",
            href: "#",
        },
        { label: "This too a label, it is long, and informative", href: "#" },
        {
            label: "Now, this is a label, it is long, and informative",
            href: "#",
        },
    ],
    "A few labels": [
        { label: "This is a label, it is long, and informative", href: "#" },
        { label: "This here is a label, it is long, and informative" },
        { label: "This too a label, it is long, and informative", href: "#" },
        { label: "Now, this is a label, it is long, and informative" },
        { label: "The revolution will not be televised" },
    ],
    // Add more labels, wayyyyy more XXX
    "Only labels": [
        { label: "I am a label" },
        { label: "I too am a label" },
        { label: "Plug in, turn on, and cop out" },
        { label: "lowercase on purpose, hello, I am a crumb" },
        { label: "Applepie crumb" },
        { label: "Crumblicious" },
    ],
    "Empty": [],
};

const meta: Meta<Breadcrumbs> = {
    component: Breadcrumbs,
    argTypes: {
        crumbs: makeStorybookSelect(choices),
    },
};
export default meta;

type Story = StoryObj<Breadcrumbs>;

export const Default: Story = {
    args: { crumbs: "all-links" },
};

export const AFewLabels: Story = {
    args: { crumbs: "a-few-labels" },
};

export const OnlyLabels: Story = {
    args: { crumbs: "only-labels" },
};

export const Empty: Story = {
    args: { crumbs: "empty" },
};
