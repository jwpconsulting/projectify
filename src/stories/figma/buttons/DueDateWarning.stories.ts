import type { Meta, StoryObj } from "@storybook/svelte";

import DueDateWarning from "$lib/figma/buttons/DueDateWarning.svelte";

const meta: Meta<DueDateWarning> = {
    component: DueDateWarning,
    argTypes: {},
};
export default meta;

type Story = StoryObj<DueDateWarning>;

export const Default: Story = {};
