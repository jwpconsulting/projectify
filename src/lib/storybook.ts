import type { User, Label } from "$lib/types";
import { labelColors, getIndexFromLabelColor } from "$lib/utils/colors";
import type { LabelColor } from "$lib/utils/colors";

export const fr = "flex flex-row flex-wrap gap-2";
export const fc = "flex flex-col flex-wrap gap-2";
export const trueFalse = [true, false];
export const falseTrue = [false, true];

export const user1: User = {
    email: "hello@example.com",
    full_name: undefined,
    profile_picture: undefined,
};
export const user2: User = {
    email: "john@example.com",
    full_name: undefined,
    profile_picture: undefined,
};
export const users = [user1, user2, null];

export const selectLabels: ("allLabels" | "noLabel" | LabelColor)[] = [
    ...labelColors,
    "allLabels",
    "noLabel",
];
export const labels: (
    | { kind: "applyLabel"; label: "applyLabel" }
    | { kind: LabelColor; label: Label }
)[] = [
    ...labelColors.map((labelColor: LabelColor) => {
        return {
            kind: labelColor,
            label: {
                name: "label",
                color: getIndexFromLabelColor(labelColor),
                uuid: "",
            },
        };
    }),
    { kind: "applyLabel", label: "applyLabel" },
];
