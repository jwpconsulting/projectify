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
const labelColorTypes = [
    "bg",
    "bgHover",
    "border",
    "focusBorder",
    "text",
    "textBg",
    "textHoverBg",
] as const;
type LabelColorType = (typeof labelColorTypes)[number];
export const labelColors = [
    "orange",
    "pink",
    "blue",
    "purple",
    "yellow",
    "red",
    "green",
] as const;
export type LabelColor = (typeof labelColors)[number];
// TODO return undefined instead
export function getLabelColorFromIndex(index: number): LabelColor | null {
    const color = labelColors[index];
    if (color === undefined) {
        console.error(`Expected color for ${index.toString()}`);
        return null;
    }
    return color;
}
export function getIndexFromLabelColor(color: LabelColor): number {
    const index = labelColors.indexOf(color);
    if (index == -1) {
        throw new Error("Expected index");
    }
    return index;
}

const colors = {
    bg: {
        orange: "bg-label-orange",
        pink: "bg-label-pink",
        blue: "bg-label-blue",
        purple: "bg-label-purple",
        yellow: "bg-label-yellow",
        red: "bg-label-red",
        green: "bg-label-green",
    },
    bgHover: {
        orange: "hover:bg-label-hover-orange group-hover:bg-label-hover-orange",
        pink: "hover:bg-label-hover-pink group-hover:bg-label-hover-pink",
        blue: "hover:bg-label-hover-blue group-hover:bg-label-hover-blue",
        purple: "hover:bg-label-hover-purple group-hover:bg-label-hover-purple",
        yellow: "hover:bg-label-hover-yellow group-hover:bg-label-hover-yellow",
        red: "hover:bg-label-hover-red group-hover:bg-label-hover-red",
        green: "hover:bg-label-hover-green group-hover:bg-label-hover-green",
    },
    border: {
        orange: "border-label-text-orange",
        pink: "border-label-text-pink",
        blue: "border-label-text-blue",
        purple: "border-label-text-purple",
        yellow: "border-label-text-yellow",
        red: "border-label-text-red",
        green: "border-label-text-green",
    },
    text: {
        orange: "text-label-text-orange",
        pink: "text-label-text-pink",
        blue: "text-label-text-blue",
        purple: "text-label-text-purple",
        yellow: "text-label-text-yellow",
        red: "text-label-text-red",
        green: "text-label-text-green",
    },
    textBg: {
        orange: "text-label-orange",
        pink: "text-label-pink",
        blue: "text-label-blue",
        purple: "text-label-purple",
        yellow: "text-label-yellow",
        red: "text-label-red",
        green: "text-label-green",
    },
    textHoverBg: {
        orange: "group-hover:text-label-hover-orange",
        pink: "group-hover:text-label-hover-pink",
        blue: "group-hover:text-label-hover-blue",
        purple: "group-hover:text-label-hover-purple",
        yellow: "group-hover:text-label-hover-yellow",
        red: "group-hover:text-label-hover-red",
        green: "group-hover:text-label-hover-green",
    },
    focusBorder: {
        orange: "focus:border-label-text-orange",
        pink: "focus:border-label-text-pink",
        blue: "focus:border-label-text-blue",
        purple: "focus:border-label-text-purple",
        yellow: "focus:border-label-text-yellow",
        red: "focus:border-label-text-red",
        green: "focus:border-label-text-green",
    },
};
export function getLabelColorClass(
    colorType: LabelColorType,
    color: LabelColor,
): string {
    return colors[colorType][color];
}
