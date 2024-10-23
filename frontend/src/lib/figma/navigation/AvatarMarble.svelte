<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<!-- SPDX-FileCopyrightText: 2023 paolotiu -->
<script lang="ts" context="module">
    function getNumber(name: string): number {
        const charactersArray = Array.from(name);
        let charactersCodesSum = 0;

        charactersArray.forEach((charactersArrayItem) => {
            return (charactersCodesSum += charactersArrayItem.charCodeAt(0));
        });

        return charactersCodesSum;
    }

    function getDigit(number: number, ntn: number): number {
        return Math.floor((number / Math.pow(10, ntn)) % 10);
    }

    function getUnit(number: number, range: number, index?: number): number {
        const value = number % range;

        if (index && getDigit(number, index) % 2 === 0) {
            return -value;
        } else return value;
    }

    function getRandomColor(
        number: number,
        colors: string[],
        range: number,
    ): string {
        const color = colors[number % range];
        if (color === undefined) {
            throw new Error("Expected color");
        }
        return color;
    }

    // Source
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random#getting_a_random_integer_between_two_values
    function getRandomInt(min: number, max: number): number {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min) + min); // The maximum is exclusive and the minimum is inclusive
    }

    function getRandomId(): string {
        const array: unknown[] = [...Array<unknown>(8)];
        const ints = array.map(() => getRandomInt(0, 255));
        return ints.toString();
    }
</script>

<script lang="ts">
    const SIZE = 80;

    interface Color {
        color: string;
        translateX: number;
        translateY: number;
        scale: number;
        rotate: number;
    }
    function generateColors(
        name: string,
        colors: string[],
    ): [Color, Color, Color] {
        const makeColor = (i: number): Color => {
            return {
                color: getRandomColor(numFromName + i, colors, range),
                translateX: getUnit(numFromName * (i + 1), SIZE / 10, 1),
                translateY: getUnit(numFromName * (i + 1), SIZE / 10, 2),
                scale: 1.2 + getUnit(numFromName * (i + 1), SIZE / 20) / 10,
                rotate: getUnit(numFromName * (i + 1), 360, 1),
            };
        };
        const numFromName = getNumber(name);
        const range = colors.length;

        return [makeColor(0), makeColor(1), makeColor(2)];
    }

    export let size: number;
    export let name: string;
    export let square = false;
    export let colors = [
        "#92A1C6",
        "#146A7C",
        "#F0AB3D",
        "#C271B4",
        "#C20D90",
    ];

    $: properties = generateColors(name, colors);

    $: maskId = `mask__marble${getRandomId()}`;
    $: filterId = `prefix__filter0_f${getRandomId()}`;
</script>

<svg
    viewBox="0 0 {SIZE} {SIZE}"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    data-testid="avatar-marble"
>
    <title>{name}</title>
    <mask
        id={maskId}
        maskUnits="userSpaceOnUse"
        x={0}
        y={0}
        width={SIZE}
        height={SIZE}
    >
        <rect
            width={SIZE}
            height={SIZE}
            rx={square ? undefined : SIZE * 2}
            fill="white"
        />
    </mask>
    <g mask="url(#{maskId})">
        <rect width={SIZE} height={SIZE} rx="2" fill={properties[0].color} />
        <path
            filter="url(#{filterId})"
            style="mix-blend-mode: overlay;"
            d="M32.414 59.35L50.376 70.5H72.5v-71H33.728L26.5 13.381l19.057 27.08L32.414 59.35z"
            fill={properties[1].color}
            transform="translate({properties[1].translateX}  {properties[1]
                .translateY}) rotate({properties[1].rotate} {SIZE / 2} {SIZE /
                2}) scale({properties[2].scale})"
        />
        <path
            filter="url(#{filterId})"
            d="M22.216 24L0 46.75l14.108 38.129L78 86l-3.081-59.276-22.378 4.005 12.972 20.186-23.35 27.395L22.215 24z"
            fill={properties[2].color}
            transform="translate({properties[2].translateX} {properties[2]
                .translateY}) rotate({properties[2].rotate} {SIZE / 2} {SIZE /
                2}) scale({properties[2].scale})"
        />
    </g>
    <defs>
        <filter
            id={filterId}
            filterUnits="userSpaceOnUse"
            color-interpolation-filters="sRGB"
        >
            <feFlood flood-opacity={0} result="BackgroundImageFix" />
            <feBlend
                in="SourceGraphic"
                in2="BackgroundImageFix"
                result="shape"
            />
            <feGaussianBlur stdDeviation={7} result="effect1_foregroundBlur" />
        </filter>
    </defs>
</svg>
