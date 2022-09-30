import type { IconSource } from "@steeze-ui/svelte-icon/types";
import type { User } from "$lib/types/user";
import type { Label } from "$lib/types/workspace";

export type ButtonStyle =
    | { kind: "primary" }
    | { kind: "secondary" }
    | { kind: "tertiary"; icon: { position: "left"; icon: IconSource } }
    | { kind: "tertiary"; icon: { position: "right"; icon: IconSource } }
    | { kind: "tertiary"; icon: null };
export const buttonColors = ["blue", "red"] as const;
export type ButtonColor = typeof buttonColors[number];
export const buttonSizes = ["medium", "small", "extra-small"] as const;
export type ButtonSize = typeof buttonSizes[number];

export const sideMenuCreateSizes = ["extraSmall", "small"] as const;
export type SideMenuCreateSize = typeof sideMenuCreateSizes[number];

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

export const menuButtonStates = ["normal", "accordion"] as const;
export type MenuButtonState = typeof menuButtonStates[number];
export const menuButtonColors = ["base", "primary", "destructive"] as const;
export type MenuButtonColor = typeof menuButtonColors[number];
export type MenuButtonKind = { kind: "a"; href: string } | { kind: "button" };

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

export const avatarV3Sizes = ["small", "medium", "hoverable"] as const;
export type AvatarV3Size = typeof avatarV3Sizes[number];

export const avatarV5Sizes = ["small", "medium", "hoverable"] as const;
export type AvatarV5Size = typeof avatarV5Sizes[number];
export type AvatarV5Content =
    | { kind: "assign"; users: [User | null, User | null] }
    | { kind: "multiple"; users: (User | null)[] };

export type LabelLabel =
    | { kind: "applyLabel" }
    | { kind: "label"; label: Label };
export type SelectLabel =
    | { kind: "allLabels" }
    | { kind: "noLabel" }
    | { kind: "label"; label: Label };

export const filterLabelMenuStates = ["list", "create"] as const;
export type FilterLabelMenuState = typeof filterLabelMenuStates[number];

// TODO rename to InputFieldKind Justus 2022-09-22
export type InputFieldStyle =
    | { kind: "search" }
    | { kind: "subTask" }
    | { kind: "field"; inputType: "text" | "password" };
export const inputFieldSizes = ["extraSmall", "small", "normal"] as const;
export type InputFieldSize = typeof inputFieldSizes[number];
export type InputFieldAnchor = { href: string; label: string };

export const anchorSizes = ["extraSmall", "normal"] as const;
export type AnchorSize = typeof anchorSizes[number];
