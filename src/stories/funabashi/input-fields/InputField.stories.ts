import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";

import InputField from "$lib/funabashi/input-fields/InputField.svelte";
import type { InputFieldStyle } from "$lib/funabashi/types";

const style = makeStorybookSelect<InputFieldStyle>({
    "Search": {
        kind: "search",
    },
    "Sub Task": {
        kind: "subTask",
    },
    "Text": {
        kind: "field",
        inputType: "text",
    },
    "Password": {
        kind: "field",
        inputType: "password",
    },
    "Email": {
        kind: "field",
        inputType: "email",
    },
    "Date": {
        kind: "field",
        inputType: "date",
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

export const Search: Story = {
    args: {
        placeholder: "Enter something to search for",
        name: "search",
        style: { kind: "search" },
        label: "This is a label for the search",
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

export const SubTask: Story = {
    args: {
        placeholder: "Enter the name of a sub task",
        name: "sub-task",
        style: { kind: "subTask" },
        label: "Your sub task",
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

export const Text: Story = {
    args: {
        placeholder: "This is a placeholder for your text",
        name: "text",
        style: { kind: "field", inputType: "text" },
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
        style: { kind: "field", inputType: "text" },
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
        style: { kind: "field", inputType: "date" },
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

export const Readonly: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "date",
        style: { kind: "field", inputType: "date" },
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
        style: { kind: "field", inputType: "date" },
        label: "A date, but it's readonly",
        value: "2012-12-31",
    },
};

export const AnchorTopOnly: Story = {
    args: {
        placeholder: "This will never be shown",
        name: "date",
        style: { kind: "field", inputType: "date" },
        value: "2012-12-31",
        anchorTop: {
            href: "#",
            label: "I am the anchor on the top",
        },
    },
};
