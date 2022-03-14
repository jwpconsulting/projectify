const hueSteps = 20;

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

export const paletteA = interpolateCosine(
    [0.8, 0.5, 0.4],
    [0.2, 0.4, 0.2],
    [2.0, 1.0, 1.0],
    [0.0, 0.25, 0.25]
);

export const paletteB = interpolateCosine(
    [0.5, 0.5, 0.5],
    [0.5, 0.5, 0.5],
    [2.0, 1.0, 0.0],
    [0.5, 0.2, 0.25]
);
export const paletteC = interpolateCosine(
    [0.5, 0.5, 0.5],
    [0.5, 0.5, 0.5],
    [1.0, 1.0, 1.0],
    [0.0, 0.33, 0.67]
);

export function getColorFromInx(inx: number): {
    h: number;
    s: number;
    l: number;
    br: boolean;
    style: string;
} {
    const i = inx / hueSteps;
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
