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
