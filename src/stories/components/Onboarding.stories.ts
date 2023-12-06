import type { Meta, StoryObj } from "@storybook/svelte";

import Onboarding from "$lib/components/Onboarding.svelte";

const meta: Meta<Onboarding> = {
    component: Onboarding,
    argTypes: {
        title: {
            control: "text",
        },
        prompt: {
            control: "text",
        },
        nextLabel: {
            control: "text",
        },
        stepCount: {
            control: { type: "range", min: 1, max: 9999 },
        },
        step: {
            control: { type: "range", min: 1, max: 9999 },
        },
    },
    args: {
        title: "Hello world",
        prompt: "Choose your destiny",
        nextLabel: "Continue now",
        nextAction: { kind: "a", href: "#" },
        stepCount: 9999,
        step: 1337,
    },
};
export default meta;

type Story = StoryObj<Onboarding>;

export const Default: Story = {};
