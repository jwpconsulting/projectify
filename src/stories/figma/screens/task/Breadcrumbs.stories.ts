import type { Meta, StoryObj } from "@storybook/svelte";

import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";

const meta: Meta<Breadcrumbs> = {
    component: Breadcrumbs,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Breadcrumbs>;

export const Default: Story = {};
