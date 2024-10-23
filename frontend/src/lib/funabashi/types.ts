// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import type { IconSource } from "@steeze-ui/svelte-icon";

export type AnchorSize = "normal" | "large";

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
    | {
          kind: "tertiary";
          icon?: { position: "right" | "left"; icon: IconSource };
      };
export type ButtonColor = "blue" | "red";
export type ButtonSize = "medium";

// For buttons/CircleIcon.svelte
export type CircleIconSize = "medium";
// TODO rename CircleIcon
export type CircleIconIcon =
    | "ellipsis"
    | "edit"
    | "delete"
    | "up"
    | "down"
    | "close";

// For buttons/SquovalIcon.svelte
export type SquovalIcon =
    // TODO rename project
    | "board"
    | "teamMember"
    | "label"
    | "bulk"
    | "move"
    | "filterTeamMember"
    | "delete"
    | "ellipsis"
    | "plus"
    | "edit"
    | "dotsVertical"
    | "help";
export type SquovalState = "inactive" | "disabled" | "active";

// For input-fields/InputField.svelte
// TODO rename to InputFieldKind Justus 2022-09-22
// TODO we need to instead support "search", "erasable", and field
// subTask should use erasable
export type InputFieldStyle =
    | { inputType: "search" | "text" | "password" | "email" | "date" }
    | { inputType: "numeric"; min?: number; max?: number };
export interface InputFieldAnchor {
    href: string;
    label: string;
}
export type InputFieldValidation =
    | { ok: true; result: string }
    | { ok: false; error: string };

// This is a big TODO, will be refactored later
export function toValid(
    error: string | undefined,
    result: string,
): InputFieldValidation {
    if (error) {
        return { ok: false, error };
    } else {
        return { ok: true, result };
    }
}
