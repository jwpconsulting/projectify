// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import type { IconSource } from "@steeze-ui/svelte-icon/types";

// TODO remove small
const anchorSizes = ["small", "normal", "large"] as const;
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
    | {
          kind: "tertiary";
          icon?: { position: "right" | "left"; icon: IconSource };
      };
export const buttonColors = ["blue", "red"] as const;
export type ButtonColor = (typeof buttonColors)[number];
// TODO remove small
export const buttonSizes = ["medium", "small"] as const;
export type ButtonSize = (typeof buttonSizes)[number];

// For buttons/CircleIcon.svelte
// TODO remove small
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
    | { inputType: "text" | "password" | "email" | "date" }
    | { inputType: "numeric"; min?: number; max?: number };
export interface InputFieldAnchor {
    href: string;
    label: string;
}
export type InputFieldValidation =
    | { ok: true; result: string }
    | { ok: false; error: string };
