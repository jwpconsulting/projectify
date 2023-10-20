/*
 * Types used for repository methods
 */
export type ClientError =
    | { kind: "list"; errors: string[] }
    // If we have nested errors, we might need to change this
    // Perhaps we can make the fields depend on T
    | { kind: "dict"; dict: Record<string, string> };

export type ApiResponse<T> =
    | { kind: "ok"; ok: true; data: T }
    | { kind: "badRequest"; ok: false; error: ClientError } // 400
    | { kind: "forbidden"; ok: false; error: ClientError } // 403
    | { kind: "notFound"; ok: false; error: ClientError } // 404
    | { kind: "error"; ok: false; error: Error }; // Any other error
