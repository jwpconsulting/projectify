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

const floatingActionButtonIcons = ["plus", "close"] as const;
export type FloatingActionButtonIcon =
    (typeof floatingActionButtonIcons)[number];
