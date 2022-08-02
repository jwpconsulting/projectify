import { writable } from "svelte/store";

const seatUnit = 1;
const seatMax = 999;

export let seats = writable<number>(10);
export function seatMinus() {
    seats.update((n) => n - seatUnit);
}
export function seatAdd() {
    seats.update((n) => n + seatUnit);
}
seats.subscribe((n) => {
    if (n > seatMax) {
        seats.set(seatMax);
    }
});
