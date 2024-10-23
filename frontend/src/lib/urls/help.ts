// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
/**
 * Help URLs
 */
type HelpTopic = "billing" | "keyboard-shortcuts";
export function helpUrl(topic: HelpTopic) {
    return `/help/${topic}`;
}
