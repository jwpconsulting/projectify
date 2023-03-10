import type { Meta, StoryObj } from "@storybook/svelte";

import InputField from "$lib/figma/input-fields/InputField.svelte";

const meta: Meta<InputField> = {
    component: InputField,
    argTypes: {
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
