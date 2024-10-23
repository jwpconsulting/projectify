// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
export interface Customer {
    seats: number;
    uuid: string;
    subscription_status: "UNPAID" | "CUSTOM" | "ACTIVE" | "CANCELLED";
}
