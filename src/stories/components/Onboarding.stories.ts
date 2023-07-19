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
        nextMessage: {
            control: "text",
        },
        stepCount: {
            control: { type: "range", min: 1, max: 9999 },
        },
        step: {
            control: { type: "range", min: 1, max: 9999 },
        },
        hasContentPadding: {
            control: "boolean",
        },
        nextBtnDisabled: {
            control: "boolean",
        },
    },
    args: {
        title: "Hello world",
        prompt: "Choose your destiny",
        nextLabel: "Continue now",
        stepCount: 9999,
        step: 1337,
        nextMessage: "It is perfectly safe to continue",
        hasContentPadding: false,
        nextBtnDisabled: false,
    },
};
export default meta;

type Story = StoryObj<Onboarding>;

export const Default: Story = {};
