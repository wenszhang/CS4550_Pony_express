const api = (token) => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

    const headers = {
        "Content-Type": "application/json",
    };

    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    const handleResponse = (response) => {
        if (!response.ok) {
            return response.json().then((body) => {
                const error = new Error(`HTTP error! status: ${response.status}`);
                error.body = body;
                throw error;
            });
        }
        return response;
    };

    const get = (url) => (
        fetch(baseUrl + url, {method: "GET", headers,}).then(handleResponse)
    );

    const post = (url, body) => (
        fetch(baseUrl + url, {method: "POST", body: JSON.stringify(body), headers,},).then(handleResponse)
    );

    const postForm = (url, body) => (
        fetch(baseUrl + url,
            {
                method: "POST",
                body: new URLSearchParams(body),
                headers: {
                    ...headers,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            },
        ).then(handleResponse)
    );

    const put = (url, body) => (
        fetch(
            baseUrl + url,
            {
                method: "PUT",
                body: JSON.stringify(body),
                headers,
            },
        ).then(handleResponse)
    );

    return { get, post, postForm, put };
};

export default api;