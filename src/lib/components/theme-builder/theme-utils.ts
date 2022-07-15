import colorStyleVars from "daisyui/colors/colorNames.js";
import hex2hsl from "daisyui/colors/hex2hsl.js";

export type Theme = {
    [key: string]: string;
};

export type ThemeItem = {
    name: string;
    value: string;
};

export function getThemeFromDom(): Theme {
    const styles = getComputedStyle(document.documentElement);

    const theme = new Map<string, string>();
    const node = document.createElement("div");
    Object.entries(colorStyleVars).forEach(([key, val]) => {
        let value = styles.getPropertyValue(val as string);
        node.style.setProperty("color", `hsla(${value})`);
        value = node.style.getPropertyValue("color");
        value = rgb2hex(value);
        theme.set(key, value);
    });

    return Object.fromEntries(theme);
}

export function rgb2hex(rgb: string): string {
    function hex(x: string) {
        return ("0" + parseInt(x).toString(16)).slice(-2);
    }
    const rgbRex = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    if (!rgbRex) {
        throw new Error("Expected rgbRex");
    }
    const [_a, r, g, b] = rgbRex;

    return "#" + hex(r) + hex(g) + hex(b);
}

export function themeToArray(theme: Theme): ThemeItem[] {
    if (!theme) {
        return [];
    }
    return Object.entries(theme).map(([key, val]) => {
        return {
            name: key,
            value: val,
        };
    });
}

export function arrayToTheme(arr: ThemeItem[]): Theme {
    const themeMap = new Map<string, string>();
    arr.forEach((v) => themeMap.set(v.name, v.value));
    return Object.fromEntries(themeMap);
}

export function dumpTheme(themeArray: ThemeItem[]): void {
    const th = arrayToTheme(themeArray);
    const thStr = JSON.stringify(th, null, 4);
    console.log(thStr);
    navigator.clipboard.writeText(thStr);
}

export function getStyleFor(themeArray: ThemeItem[]): string {
    const stylesVars = themeArray.map(({ name, value }) => {
        const varName = colorStyleVars[name];
        const hsv = hex2hsl(value);
        return `${varName}: ${hsv};`;
    });

    return stylesVars.join("");
}
