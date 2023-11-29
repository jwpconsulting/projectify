import { getCookie } from "./cookie";

// TODO refactor me together with the other repository util functions
export async function uploadImage(
    imageFile: File,
    url: string
): Promise<void> {
    const formData = new FormData();
    formData.append("file", imageFile);
    const csrftoken = getCookie("csrftoken");
    const response = await fetch(url, {
        method: "POST",
        credentials: "include",
        headers: csrftoken ? { "X-CSRFToken": csrftoken } : {},
        body: formData,
    });
    await response.text();
}
