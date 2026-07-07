import api from "./api";

export async function getDocuments() {
    const response = await api.get('/csv/documents/')

    return response.data
}

export async function uploadDocument(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post("/csv/upload/", formData);

    return response.data;
}
