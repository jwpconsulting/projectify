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
import type { User } from "$lib/types/user";
import type { Label } from "$lib/types/workspace";

// TODO remove accordion
const menuButtonStates = ["normal", "accordion"] as const;
export type MenuButtonState = (typeof menuButtonStates)[number];
const menuButtonColors = ["base", "primary", "destructive"] as const;
export type MenuButtonColor = (typeof menuButtonColors)[number];

const borderedIconTypes = ["workspace", "filter"] as const;
export type BorderedIconType = (typeof borderedIconTypes)[number];

export const avatarStateSizes = [
    // Maybe remove?
    "small",
    "medium",
    // Maybe remove?
    "large",
    // TODO remove
    "hoverable",
] as const;
export type AvatarStateSize = (typeof avatarStateSizes)[number];

export interface AvatarVariantContent {
    kind: "single";
    user?: User;
}

// TODO rename me LabelContent Justus 2023-03-07
export type LabelLabel =
    | { kind: "applyLabel" }
    | { kind: "label"; label: Label };
export type SelectLabel =
    | { kind: "allLabels" }
    | { kind: "noLabel" }
    | { kind: "label"; label: Label };

export type FilterLabelMenuState =
    | { kind: "list" }
    | { kind: "create" }
    | { kind: "update"; label: Label };
