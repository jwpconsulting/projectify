/*
 * Call a callback on every window resize until this function's return value
 * is called
 */
export function onResize(callback: () => void): () => void {
    addEventListener("resize", callback);
    return () => removeEventListener("resize", callback);
}
