// TODO remove labels Justus 2022-09-28
const settingKinds = [
    "index",
    "labels",
    "workspace-users",
    "billing",
] as const;
export type SettingKind = (typeof settingKinds)[number];
