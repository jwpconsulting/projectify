// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TabBar from "$lib/figma/screens/workspace-settings/TabBar.svelte";
import { workspace } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

import { activeSetting } from "./config";

const meta: Meta<TabBar> = {
    component: TabBar,
    argTypes: { activeSetting },
    args: { workspace, activeSetting: "index" },
};
export default meta;

type Story = StoryObj<TabBar>;

export const Default: Story = {};
