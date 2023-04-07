import { browser } from "$app/environment";

export const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
];

export const weekDays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
];

export function dateStringToLocal(dateStr: string, time = false): string {
    const date = new Date(dateStr);
    let lang: string;

    if (browser) {
        lang = navigator.language;
    } else {
        lang = "en";
    }

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

export function getMonths(lang: string | undefined = undefined): string[] {
    const objDate = new Date();
    objDate.setDate(1);

    const months: string[] = [];
    for (let i = 0; i < 12; i++) {
        objDate.setMonth(i);
        const locale = lang;
        const month = objDate.toLocaleString(locale, { month: "long" });
        months.push(month);
    }

    return months;
}

export function getWeekDays(lang: string | undefined = undefined): string[] {
    const objDate = new Date();
    objDate.setDate(1);

    const weekDays: string[] = [];
    for (let i = 0; i < 7; i++) {
        objDate.setDate(i);
        const locale = lang;
        const weekDay = objDate.toLocaleString(locale, { weekday: "long" });
        weekDays.push(weekDay);
    }

    return weekDays;
}

export type Calendar = {
    year: number;
    month: number;
    days: {
        inx: number;
        moff: number;
        date: Date;
    }[];
};

export function getCalendar(year: number, month: number): Calendar {
    const objDate = new Date();
    objDate.setDate(1);
    objDate.setFullYear(year);
    objDate.setMonth(month);

    const calendar: Calendar = {
        year: year,
        month: month,
        days: [],
    };

    const firstDay = (objDate.getDay() + 6) % 7;
    const lastDay = new Date(year, month + 1, 0).getDate();
    const lastMonth = month === 0 ? 11 : month - 1;
    const lastYear = month === 0 ? year - 1 : year;
    const lastMonthLastDay = new Date(lastYear, lastMonth + 1, 0).getDate();

    for (let i = 0; i < 42; i++) {
        let day = i - firstDay + 1;
        let moff = 0;
        if (day <= 0) {
            moff = -1;
            day = lastMonthLastDay + day;
        } else if (day > lastDay) {
            moff = 1;
            day = day - lastDay;
        }

        const date = new Date(year, month, day);
        date.setMonth(month + moff);
        calendar.days.push({
            date: date,
            inx: day,
            moff,
        });
    }

    return calendar;
}
