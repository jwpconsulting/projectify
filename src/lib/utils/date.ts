export function dateStringToLocal(dateStr: string, time = false): string {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) {
        throw new Error(`Invalid date: ${dateStr}`);
    }
    if (time) {
        return date.toLocaleDateString() + " " + date.toLocaleTimeString();
    } else {
        return date.toLocaleDateString();
    }
}
