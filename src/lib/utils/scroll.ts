/*
 * Block scrolling until the callback that is returned is called
 * This might not be compatible with other functions that change
 * document body style or scroll.
 */
export function blockScrolling(): () => void {
    const scrollOffset = window.scrollY;
    document.body.style.position = "fixed";
    document.body.scroll(0, scrollOffset);
    return () => {
        document.body.style.position = "";
        window.scrollTo(0, scrollOffset);
    };
}
