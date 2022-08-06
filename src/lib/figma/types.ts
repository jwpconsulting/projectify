import type { IconSource } from "@steeze-ui/svelte-icon/types";
import type { User } from "$lib/types";

export const buttonStyles = ["primary", "secondary", "tertiary"] as const;
export type ButtonStyle = typeof buttonStyles[number];
export const buttonColors = ["blue", "red"] as const;
export type ButtonColor = typeof buttonColors[number];
export const buttonSizes = ["medium", "small", "extra-small"] as const;
export type ButtonSize = typeof buttonSizes[number];
export type ButtonIcon =
    | { position: "left"; icon: IconSource }
    | { position: "right"; icon: IconSource }
    | null;

export const circleIconSizes = ["small", "medium"] as const;
export type CircleIconSize = typeof circleIconSizes[number];
export const circleIconIcons = [
    "ellipsis",
    "edit",
    "delete",
    "up",
    "down",
    "close",
] as const;
export type CircleIconIcon = typeof circleIconIcons[number];

export const menuButtonStates = ["normal", "selected", "accordion"] as const;
export type MenuButtonState = typeof menuButtonStates[number];

export const stepperPositions = ["not-last", "last"] as const;
export type StepperPosition = typeof stepperPositions[number];
export const stepperActiveStates = ["inactive", "this", "next"] as const;
export type StepperActiveState = typeof stepperActiveStates[number];

export const sideNavMainTypes = ["workspace", "filter"] as const;
export type SideNavMainType = typeof sideNavMainTypes[number];

export const boardButtonStates = ["inactive", "disabled", "active"] as const;
export type BoardButtonState = typeof boardButtonStates[number];

export const squovalIcons = [
    "board",
    "member",
    "label",
    "bulk",
    "move",
    "filter-member",
    "delete",
    "ellipsis",
] as const;
export type SquovalIcon = typeof squovalIcons[number];
export const squovalStates = ["inactive", "disabled", "active"] as const;
export type SquovalState = typeof squovalStates[number];

export const avatarV3Sizes = ["small", "medium"] as const;
export type AvatarV3Size = typeof avatarV3Sizes[number];

export const avatarV5Sizes = ["small", "medium"] as const;
export type AvatarV5Size = typeof avatarV5Sizes[number];
export type AvatarV5Content =
    | { kind: "assign"; users: [User | null, User | null] }
    | { kind: "multiple"; users: (User | null)[] };
