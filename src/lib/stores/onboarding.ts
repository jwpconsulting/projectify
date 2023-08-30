import { writable } from "svelte/store";

const seatUnit = 1;
const seatMax = 999;

export const seats = writable<number>(10);
export function seatMinus() {
    seats.update((n) => n - seatUnit);
}
export function seatAdd() {
    seats.update((n) => n + seatUnit);
}
// TODO can we make this a derivation or just fix seatAdd? Justus 2023-08-30
seats.subscribe((n) => {
    if (n > seatMax) {
        seats.set(seatMax);
    }
});

export const numSteps = 5;
const firstStep = 0;
export const currentStep = writable<number>(firstStep);
export function gotoStep(step: number) {
    currentStep.set(step);
}
