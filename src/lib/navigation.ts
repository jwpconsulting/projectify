export async function goto(url: string) {
    const { goto } = await import("$app/navigation");
    await goto(url);
}
