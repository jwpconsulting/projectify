function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
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
): Promise<unknown> {
    let uploadRequest = null;
    if (!imageFile) {
        return new Promise((resolve) => {
            resolve(null);
        });
    }

    if (uploadRequest) {
        uploadRequest.abort();
    }

    const formData = new FormData();
    formData.append("file", imageFile);
    uploadRequest = new XMLHttpRequest();
    uploadRequest.withCredentials = true;
    uploadRequest.open("POST", url);

    const csrftoken = getCookie("csrftoken");
    if (csrftoken) {
        uploadRequest.setRequestHeader("X-CSRFToken", csrftoken);
    }

    uploadRequest.send(formData);

    const promise = new Promise((resolve, reject) => {
        uploadRequest.onload = () => {
            if (uploadRequest.status === 200 || uploadRequest.status === 204) {
                resolve(uploadRequest.response);
            } else {
                reject(Error(uploadRequest.statusText));
            }
        };
    });
    return promise;
}
