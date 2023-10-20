/*
 * Types used for repository methods
 */
export type ApiResponse<T, E> =
    | { kind: "ok"; ok: true; data: T }
    | { kind: "badRequest"; ok: false; error: E } // 400
    | { kind: "forbidden"; ok: false; error: E } // 403
    | { kind: "notFound"; ok: false; error: E } // 404
    | { kind: "error"; ok: false; error: Error }; // Any other error
