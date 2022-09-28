// TODO remove labels Justus 2022-09-28
export const settingKinds = [
    "index",
    "labels",
    "team-members",
    "billing",
] as const;
export type SettingKind = typeof settingKinds[number];
