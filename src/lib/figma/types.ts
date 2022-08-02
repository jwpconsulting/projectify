import type { IconSource } from "@steeze-ui/svelte-icon/types";

export const buttonStyles = ["primary", "secondary", "tertiary"] as const;
export type ButtonStyle = typeof buttonStyles[number];
export const buttonColors = ["blue", "red", "black"] as const;
export type ButtonColor = typeof buttonColors[number];
export const buttonSizes = ["medium", "small", "extra-small"] as const;
export type ButtonSize = typeof buttonSizes[number];
export type ButtonIcon =
    | { position: "left"; icon: IconSource }
    | { position: "right"; icon: IconSource }
    | null;
