import type { Meta, StoryObj } from "@storybook/svelte";

import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";

const meta: Meta<ConnectionStatus> = {
    component: ConnectionStatus,
};
export default meta;

type Story = StoryObj<ConnectionStatus>;

export const Default: Story = {};
