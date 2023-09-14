import type { Meta, StoryObj } from "@storybook/svelte";

import FocusLock from "./FocusLock.svelte";

const meta: Meta<FocusLock> = {
    component: FocusLock,
};
export default meta;

type Story = StoryObj<FocusLock>;

export const Default: Story = {};
