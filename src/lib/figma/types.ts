import type { User } from "$lib/types/user";
import type { Label } from "$lib/types/workspace";

const menuButtonStates = ["normal", "accordion"] as const;
export type MenuButtonState = (typeof menuButtonStates)[number];
const menuButtonColors = ["base", "primary", "destructive"] as const;
export type MenuButtonColor = (typeof menuButtonColors)[number];

const borderedIconTypes = ["workspace", "filter"] as const;
export type BorderedIconType = (typeof borderedIconTypes)[number];

export const avatarStateSizes = [
    "small",
    "medium",
    "large",
    "hoverable",
] as const;
export type AvatarStateSize = (typeof avatarStateSizes)[number];

export const avatarVariantSizes = [
    "small",
    "medium",
    "large",
    "hoverable",
] as const;
export type AvatarVariantSize = (typeof avatarVariantSizes)[number];
export type AvatarVariantContent =
    | { kind: "single"; user: User | null }
    | { kind: "assign"; users: [User | null, User | null] }
    | { kind: "multiple"; users: (User | null)[] };

// TODO rename me LabelContent Justus 2023-03-07
export type LabelLabel =
    | { kind: "applyLabel" }
    | { kind: "label"; label: Label };
export type SelectLabel =
    | { kind: "allLabels" }
    | { kind: "noLabel" }
    | { kind: "label"; label: Label };

export const filterLabelMenuStates = ["list", "create"] as const;
export type FilterLabelMenuState = (typeof filterLabelMenuStates)[number];

export const taskUpdateBarKinds = ["mobile", "desktop"] as const;
export type TaskUpdateBarKind = (typeof taskUpdateBarKinds)[number];
export const taskUpdateBarStates = ["task", "updates"] as const;
export type TaskUpdateBarState = (typeof taskUpdateBarStates)[number];

const floatingActionButtonIcons = ["plus", "close"] as const;
export type FloatingActionButtonIcon =
    (typeof floatingActionButtonIcons)[number];
