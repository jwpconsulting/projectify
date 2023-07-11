import type { IconSource } from "@steeze-ui/svelte-icon/types";

// For all buttons
export type ButtonAction =
    | { kind: "a"; href: string }
    | { kind: "button"; action: () => void }
    | { kind: "submit" };

// For buttons/Button.svelte
export type ButtonStyle =
    | { kind: "primary" }
    | { kind: "secondary" }
    | { kind: "tertiary"; icon: { position: "left"; icon: IconSource } }
    | { kind: "tertiary"; icon: { position: "right"; icon: IconSource } }
    | { kind: "tertiary"; icon: null };
export const buttonColors = ["blue", "red"] as const;
export type ButtonColor = (typeof buttonColors)[number];
export const buttonSizes = ["medium", "small", "extra-small"] as const;
export type ButtonSize = (typeof buttonSizes)[number];

// For buttons/CircleIcon.svelte
export const circleIconSizes = ["small", "medium"] as const;
export type CircleIconSize = (typeof circleIconSizes)[number];
// TODO rename circleIcons
export const circleIconIcons = [
    "ellipsis",
    "edit",
    "delete",
    "up",
    "down",
    "close",
] as const;
// TODO rename CircleIcon
export type CircleIconIcon = (typeof circleIconIcons)[number];

// For buttons/SquovalIcon.svelte
export const squovalIcons = [
    "board",
    "member",
    "label",
    "bulk",
    "move",
    "filter-member",
    "delete",
    "ellipsis",
    "plus",
    "edit",
    "dotsVertical",
    "help",
] as const;
export type SquovalIcon = (typeof squovalIcons)[number];
export const squovalStates = ["inactive", "disabled", "active"] as const;
export type SquovalState = (typeof squovalStates)[number];

// For buttons/HeaderButton.svelte
export type HeaderButtonType =
    | { kind: "dropdown"; open: boolean }
    | { kind: "button" };
export const headerButtonTypes: HeaderButtonType[] = [
    { kind: "dropdown", open: false },
    { kind: "dropdown", open: true },
    { kind: "button" },
];

// For input-fields/InputField.svelte
// TODO rename to InputFieldKind Justus 2022-09-22
// TODO we need to instead support "search", "erasable", and field
// subTask should use erasable
export type InputFieldStyle =
    | { kind: "search" }
    // TODO make me "erasable"
    | { kind: "subTask" }
    | { kind: "field"; inputType: "text" | "password" | "email" | "date" };
export const inputFieldSizes = ["extraSmall", "small", "normal"] as const;
export type InputFieldSize = (typeof inputFieldSizes)[number];
export interface InputFieldAnchor {
    href: string;
    label: string;
}
