import type { Meta, StoryObj } from "@storybook/svelte";

import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";

const meta: Meta<UploadAvatar> = {
    component: UploadAvatar,
    args: {
        fileSelected: console.log,
    },
};
export default meta;

type Story = StoryObj<UploadAvatar>;

export const Default: Story = {};
