// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import type { Meta, StoryObj } from "@storybook/svelte";

import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";

const meta: Meta<HeaderButton> = {
    component: HeaderButton,
    argTypes: {
        label: {
            control: "text",
        },
    },
    args: {
        label: "Button",
        action: { kind: "a", href: "/" },
    },
};

export default meta;

type Story = StoryObj<HeaderButton>;

export const Button: Story = {
    args: {
        type: { kind: "button" },
    },
};

export const Dropdown: Story = {
    args: {
        type: { kind: "dropdown", open: false },
    },
};
