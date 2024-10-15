// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
const settingKinds = ["index", "team-members", "billing", "quota"] as const;
export type SettingKind = (typeof settingKinds)[number];
