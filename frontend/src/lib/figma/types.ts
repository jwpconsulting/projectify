// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import type { User } from "$lib/types/user";
import type { Label } from "$lib/types/workspace";

export type MenuButtonColor = "base" | "primary" | "destructive";

export type BorderedIconType = "workspace" | "filter";

export type AvatarStateSize = "medium" | "large";

export interface AvatarVariantContent {
    kind: "single";
    user?: Pick<User, "email" | "preferred_name" | "profile_picture">;
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
