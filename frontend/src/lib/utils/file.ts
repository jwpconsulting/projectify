// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { getCookie } from "./cookie";

// TODO refactor me together with the other repository util functions
export async function uploadImage(
    imageFile: File | undefined,
    url: string,
): Promise<void> {
    const formData = new FormData();
    if (imageFile) {
        formData.append("file", imageFile);
    }
    const csrftoken = getCookie("csrftoken");
    const response = await fetch(url, {
        method: "POST",
        credentials: "include",
        headers: csrftoken ? { "X-CSRFToken": csrftoken } : {},
        body: formData,
    });
    await response.text();
}
