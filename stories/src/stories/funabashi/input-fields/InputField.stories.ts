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

import InputField from "$lib/funabashi/input-fields/InputField.svelte";
import type { InputFieldStyle } from "$lib/funabashi/types";
import { makeStorybookSelect } from "$lib/storybook";

const style = makeStorybookSelect<InputFieldStyle>({
    "Text": {
        inputType: "text",
    },
    "Password": {
        inputType: "password",
    },
    "Email": {
        inputType: "email",
    },
    "Date": {
        inputType: "date",
    },
    "Numeric": {
        inputType: "numeric",
    },
    "Numeric, 0 to 100": {
        inputType: "numeric",
        min: 0,
        max: 100,
    },
});

const meta: Meta<InputField> = {
    component: InputField,
    argTypes: {
        style,
        value: {
            control: "text",
        },
        placeholder: {
            control: "text",
        },
        name: {
            control: "text",
        },
        label: {
            control: "text",
        },
        readonly: {
            control: "boolean",
        },
    },
};
export default meta;

type Story = StoryObj<InputField>;

export const Text: Story = {
    args: {
        placeholder: "This is a placeholder for your text",
        name: "text",
        style: "text",
        label: "This is a label",
        value: undefined,
        anchorTop: {
            href: "#",
            label: "I am the anchor on the top",
        },
        anchorBottom: {
            href: "#",
            label: "I am the anchor on the bottom",
        },
        readonly: false,
    },
};

export const Password: Story = {
    args: {
        placeholder: "Enter a password. It will look password-y",
        name: "password",
        style: "password",
        label: "This is a label",
        value: "",
        anchorTop: {
            href: "#",
            label: "I am the anchor on the top",
        },
        anchorBottom: {
            href: "#",
            label: "I am the anchor on the bottom",
        },
        readonly: false,
    },
};

export const Date: Story = {
    args: {
        placeholder: "A date comes here",
        name: "date",
        style: "date",
        label: "Date for when the thing happens",
        value: "",
        anchorTop: {
            href: "#",
            label: "I am the anchor on the top",
        },
        anchorBottom: {
            href: "#",
            label: "I am the anchor on the bottom",
        },
        readonly: false,
    },
};

export const Numeric: Story = {
    args: {
        placeholder: "Number goes here",
        name: "date",
        style: "numeric",
        label: "Enter a number",
        value: "0",
        anchorTop: {
            href: "#",
            label: "I am the anchor on the top",
        },
        anchorBottom: {
            href: "#",
            label: "I am the anchor on the bottom",
        },
        readonly: false,
    },
};

export const Readonly: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "date",
        style: { inputType: "date" },
        label: "A date, but it's readonly",
        value: "2012-12-31",
        anchorTop: {
            href: "#",
            label: "I am the anchor on the top",
        },
        anchorBottom: {
            href: "#",
            label: "I am the anchor on the bottom",
        },
        readonly: true,
    },
};

export const LabelOnly: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "date",
        style: { inputType: "date" },
        label: "A date, but it's readonly",
        value: "2012-12-31",
    },
};

export const AnchorTopOnly: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "date",
        style: { inputType: "date" },
        value: "2012-12-31",
        anchorTop: {
            href: "#",
            label: "I am the anchor on the top",
        },
    },
};

export const Error: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "email",
        style: { inputType: "email" },
        value: "hello@example.com",
        anchorBottom: {
            href: "#",
            label: "I am the anchor on the bottom",
        },
        validation: {
            ok: false,
            error: "This email address is too awesome",
        },
    },
};

export const Ok: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "email",
        style: "email",
        value: "hello@example.com",
        anchorBottom: {
            href: "#",
            label: "I am the anchor on the bottom",
        },
        validation: {
            ok: true,
            result: "Your email address is the right amount of awesome",
        },
    },
};

export const OkNoAnchors: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "email",
        style: { inputType: "email" },
        value: "hello@example.com",
        validation: {
            ok: true,
            result: "Your email address is the right amount of awesome",
        },
    },
};
