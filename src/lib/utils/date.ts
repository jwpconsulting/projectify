export function dateStringToLocal(dateStr: string): string {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) {
        throw new Error(`Invalid date: ${dateStr}`);
    }

    return date.toLocaleDateString();
}
