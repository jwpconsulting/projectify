export async function copyToClipboard(value: string) {
    await navigator.clipboard.writeText(value);
}
