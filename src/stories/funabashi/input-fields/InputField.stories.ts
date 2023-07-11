import type { Meta, StoryObj } from "@storybook/svelte";

import InputField from "$lib/funabashi/input-fields/InputField.svelte";

import { makeStorybookSelect } from "$lib/storybook";
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
    },
};
export default meta;

type Story = StoryObj<InputField>;

export const Default: Story = {
    args: {
        placeholder: "This is a placeholder",
        name: "input-field",
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
    },
};
