import { formatISO, parseISO } from "date-fns";

export function formatIsoDate(date: Date): string {
    return formatISO(date, { representation: "date" });
}

export function coerceIsoDate(date: string): string {
    return formatIsoDate(parseISO(date));
}
