// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<UploadAvatar> = {
    component: UploadAvatar,
    args: {
        fileSelected: console.log,
    },
};
export default meta;

type Story = StoryObj<UploadAvatar>;

export const Default: Story = {};
