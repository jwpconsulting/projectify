declare module "@sveltejs/kit" {
    function error(code: number, extra?: string | Record<str, unknown>): Error;
    function redirect(code: number, url: string): Error;
}
