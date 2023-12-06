export interface Customer {
    seats_remaining: number;
    seats: number;
    uuid: string;
    subscription_status: "UNPAID" | "CUSTOM" | "ACTIVE";
}
