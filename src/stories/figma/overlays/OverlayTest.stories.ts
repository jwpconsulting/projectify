import type { Meta, StoryObj } from "@storybook/svelte";

import OverlayTest from "./OverlayTest.svelte";

const meta: Meta<OverlayTest> = {
    component: OverlayTest,
};
export default meta;

type Story = StoryObj<OverlayTest>;

export const Default: Story = {};
