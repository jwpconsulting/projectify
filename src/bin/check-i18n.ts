/*
 * Check the contents of our translation. Ensure that we use the strings
 */
import fs from "fs/promises";
import path from "path";

import messages from "$messages/en";
import type { Message, MessageCollection } from "$messages/types";

// TODO support multiple languages
// TODO check if all languages have all strings
/*
 * Extract messages from our message file
 */
function buildMessageStrings(collection: MessageCollection): string[] {
    const concatenateStrings = (parent: string, msg: Message): string[] => {
        if (typeof msg === "string") {
            return [`${parent}`];
        } else if (Array.isArray(msg)) {
            return [`${parent}`];
        } else {
            return Object.entries(msg).flatMap(([subParent, v]) =>
                concatenateStrings(`${parent}.${subParent}`, v)
            );
        }
    };
    return Object.entries(collection).flatMap(([k, v]) =>
        concatenateStrings(k, v)
    );
}

interface MessageString {
    path: string;
    message: string;
}

const EXTENSIONS = [".ts", ".svelte"];

// Hehe, node has no globbing support like Python... hehe...
async function walk(dir: string): Promise<string[]> {
    const files = await fs.readdir(dir);
    const promises = await Promise.all(
        files.map(async (basename) => {
            const f = path.join(dir, basename);
            const stat = await fs.stat(f);
            if (stat.isDirectory()) {
                return await walk(f);
            } else if (EXTENSIONS.includes(path.extname(f))) {
                return [f];
            } else {
                return [];
            }
        })
    );
    return promises.flat();
}

// Should match
// 1) Simple case
// $  _("simple-case")
// 2) Multiple lines
// $_(
// "i-am-on-multiple-lines"
// )
// 3) Options in the end
// $_(
// "i-am-on-multiple-lines", {options: "yep"}
// )
// 4) Numbers
// deleteBoard: $_("overlay.destructive.delete-board.title"),
const MESSAGE_RE = /\$_\(\s*?"(?<message>[a-z0-9.-]+)".*?\)/gs;

/*
 * Extract message strings from ts and svelte files
 */
async function extractMessageStrings(): Promise<MessageString[]> {
    const paths = await walk("src");
    // TODO maybe make this async?
    const promises: MessageString[][] = await Promise.all(
        paths.map(async (path) => {
            const contents = await fs.readFile(path, { encoding: "utf-8" });
            const matches = [...contents.matchAll(MESSAGE_RE)];
            return matches.flatMap(({ groups }) => {
                if (groups === undefined) {
                    throw new Error("No groups were matched");
                }
                const { message } = groups;
                return [
                    {
                        path,
                        message,
                    },
                ];
            });
        })
    );
    return promises.flat();
}

// Python has it, JS not :(
/*
 * Return all items from setA that are not in setB
 */
function difference<T>(setA: Set<T>, setB: Set<T>) {
    const result = new Set(setA);
    setB.forEach((el) => result.delete(el));
    return result;
}

function printUnused(unused: Set<string>) {
    console.warn("Warning: There were unused strings:");
    const lst = [...unused];
    lst.forEach((s, index) => console.warn(index, "String not used:", s));
}

function printNotFound(notFound: MessageString[]) {
    console.error("Error: There were strings not found:");
    notFound.forEach((s, index) => console.error(index, "Not found:", s));
}

async function check() {
    const defined = new Set(buildMessageStrings(messages));
    const messageStrings = await extractMessageStrings();

    const stringsUsed = new Set(messageStrings.map((m) => m.message));
    const unused = difference(defined, stringsUsed);
    if (unused.size > 0) {
        printUnused(unused);
        console.warn();
    }
    const notFound = messageStrings.filter(
        (string) => !defined.has(string.message)
    );
    if (notFound.length > 0) {
        printNotFound(notFound);
    }

    if (unused.size > 0 || notFound.length > 0) {
        process.exit(1);
    }
}

await check();
