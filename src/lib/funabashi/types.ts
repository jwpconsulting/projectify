import type { IconSource } from "@steeze-ui/svelte-icon/types";

const anchorSizes = ["extraSmall", "small", "normal", "large"] as const;
export type AnchorSize = (typeof anchorSizes)[number];

// For all buttons
// Using an additional onInteract property, we can catch clicking on an anchor
// and close a menu in time. Not guaranteed to be supported by all components.
export type ButtonAction =
    | { kind: "a"; href: string; onInteract?: () => void }
    | { kind: "button"; form?: string; action: () => void; disabled?: boolean }
    // For the case that a disabled button is disabled because no callback is
    // present
    | { kind: "button"; form?: string; action?: undefined; disabled: true }
    | { kind: "submit"; form?: string; disabled?: boolean };

// For buttons/Button.svelte
export type ButtonStyle =
    | { kind: "primary" }
    | { kind: "secondary" }
    // TODO make this icon? instead Justus 2023-08-28
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
    // TODO rename workspaceBoard
    "board",
    "workspaceUser",
    "label",
    "bulk",
    "move",
    "filterWorkspaceUser",
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

// For input-fields/InputField.svelte
// TODO rename to InputFieldKind Justus 2022-09-22
// TODO we need to instead support "search", "erasable", and field
// subTask should use erasable
export type InputFieldStyle =
    | { kind: "search" }
    // TODO make me "erasable"
    | { kind: "subTask" }
    | { kind: "field"; inputType: "text" | "password" | "email" | "date" };
const inputFieldSizes = ["extraSmall", "small", "normal"] as const;
export type InputFieldSize = (typeof inputFieldSizes)[number];
export interface InputFieldAnchor {
    href: string;
    label: string;
}
export type InputFieldValidation =
    | { ok: true; result: string }
    | { ok: false; error: string };
