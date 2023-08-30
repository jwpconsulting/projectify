declare module "@sveltejs/kit" {
    function redirect(code: number, url: string): Error;
}
