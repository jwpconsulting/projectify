function getCookie(name: string) {
    let cookieValue: string | null = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (const cookieUntrimmed of cookies) {
            const cookie = cookieUntrimmed.trim();
            // Does this cookie string begin with the name we want?
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

export async function uploadImage(
    imageFile: File,
    url: string
): Promise<null> {
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
    return null;
}
