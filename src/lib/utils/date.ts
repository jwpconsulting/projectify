import { browser } from "$app/environment";

export function dateStringToLocal(dateStr: string, time = false): string {
    const date = new Date(dateStr);
    const lang: string = browser ? navigator.language : "en";

    if (isNaN(date.getTime())) {
        throw new Error(`Invalid date: ${dateStr}`);
    }

    const year = String(date.getFullYear()).padStart(4, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const fDate = `${year}-${month}-${day}`;

    if (time) {
        return `${fDate} ${date.toLocaleTimeString(lang)}`;
    } else {
        return fDate;
    }
}
