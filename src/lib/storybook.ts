import { Plus } from "@steeze-ui/heroicons";
import type {
    User,
    Label,
    WorkspaceUser,
    WorkspaceUserSelectionInput,
} from "$lib/types";
import { labelColors, getIndexFromLabelColor } from "$lib/utils/colors";
import type { LabelColor } from "$lib/utils/colors";
import type { ButtonStyle, LabelLabel, SelectLabel } from "$lib/figma/types";

export const fr = "flex flex-row flex-wrap gap-2";
export const fc = "flex flex-col flex-wrap gap-2";
export const trueFalse = [true, false];
export const falseTrue = [false, true];

export const buttonStyles: ButtonStyle[] = [
    { kind: "primary" },
    { kind: "secondary" },
    { kind: "tertiary", icon: { position: "left", icon: Plus } },
    { kind: "tertiary", icon: { position: "right", icon: Plus } },
    { kind: "tertiary", icon: null },
];

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

const mappedLabels: Label[] = labelColors.map((labelColor: LabelColor) => {
    return {
        name: labelColor,
        color: getIndexFromLabelColor(labelColor),
        uuid: "",
    };
});

export const labels: LabelLabel[] = [
    ...mappedLabels.map((label: Label) => {
        return {
            kind: "label" as const,
            label,
        };
    }),
    { kind: "applyLabel" },
];
export const selectLabels: SelectLabel[] = [
    ...mappedLabels.map((label: Label) => {
        return {
            kind: "label" as const,
            label,
        };
    }),
    { kind: "allLabels" },
    { kind: "noLabel" },
];

const workspaceUser: WorkspaceUser = {
    user: user1,
    uuid: "helloWorld",
    role: "OWNER",
    created: "",
    modified: "",
};
export const workspaceUserSelectionInputs: WorkspaceUserSelectionInput[] = [
    { kind: "unassigned" },
    { kind: "allWorkspaceUsers" },
    { kind: "workspaceUser", workspaceUser },
];
