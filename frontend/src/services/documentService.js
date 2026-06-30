import api from "./api";

export async function getDocuments() {
    const response = await api.get('/csv/documents/')

    return response.data
}
