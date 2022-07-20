import type { Color } from "$lib/types";
export const paletteSize = 24;

export function interpolateCosine(
    [ar, ag, ab]: number[],
    [br, bg, bb]: number[],
    [cr, cg, cb]: number[],
    [dr, dg, db]: number[]
) {
    return (t: number): string =>
        [
            ar + br * Math.cos(2 * Math.PI * (cr * t + dr)),
            ag + bg * Math.cos(2 * Math.PI * (cg * t + dg)),
            ab + bb * Math.cos(2 * Math.PI * (cb * t + db)),
        ]
            .map((v) => Math.floor(Math.max(0, Math.min(1, v)) * 255))
            .join(" ");
}

export const paletteVals = [
    [0.77, 0.63, 0.79],
    [0.56, -0.12, 0.61],
    [4, 2.44, 0.56],
    [1.39, 3.59, -0.86],
];

export const paletteA = interpolateCosine(
    paletteVals[0],
    paletteVals[1],
    paletteVals[2],
    paletteVals[3]
);

export function getColorFromInx(inx: number): Color {
    const i = (inx % paletteSize) / paletteSize;
    const h = Math.floor(i * 360) % 360;
    const s = 80;
    const l = 70;
    const br = true;

    return {
        h,
        s,
        l,
        br,
        style: paletteA(i),
    };
}

export function getColorFromInxWithPalette(
    inx: number,
    palette: number[][]
): {
    h: number;
    s: number;
    l: number;
    br: boolean;
    style: string;
} {
    const i = (inx % paletteSize) / paletteSize;
    const h = Math.floor(i * 360) % 360;
    const s = 80;
    const l = 70;
    const br = true;

    const intPal = interpolateCosine(
        palette[0],
        palette[1],
        palette[2],
        palette[3]
    );

    return {
        h,
        s,
        l,
        br,
        style: intPal(i),
    };
}

// Generate with
// #!/usr/bin/env python3
// import subprocess
// while True:
//     color = input(">")[1:]
//     r = int(color[:2], 16)
//     g = int(color[2:4], 16)
//     b = int(color[4:], 16)
//     cp = f"""\
//             r: {r},
//             b: {b},
//             g: {g},\n"""
//     subprocess.run("pbcopy", input=cp.encode())
//
export type LabelColorType =
    | "bg"
    | "bgHover"
    | "border"
    | "text"
    | "textBg"
    | "textHoverBg";
export const labelColors = [
    "orange",
    "pink",
    "blue",
    "purple",
    "yellow",
    "red",
    "green",
] as const;
export type LabelColor = typeof labelColors[number];
export function getLabelColorFromIndex(index: number): LabelColor | null {
    const color = labelColors[index];
    if (!color) {
        console.error(`Expected color for ${index}`);
        return null;
    }
    return color;
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
        orange: "hover:bg-label-hover-orange",
        pink: "hover:bg-label-hover-pink",
        blue: "hover:bg-label-hover-blue",
        purple: "hover:bg-label-hover-purple",
        yellow: "hover:bg-label-hover-yellow",
        red: "hover:bg-label-hover-red",
        green: "hover:bg-label-hover-green",
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
};
export function getLabelColorClass(
    colorType: LabelColorType,
    color: LabelColor
): string {
    return colors[colorType][color];
}
