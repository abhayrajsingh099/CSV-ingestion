import { useState } from "react";
import { Input } from "./ui/input";
import { uploadDocument } from "@/services/documentService";
import { Button } from "./ui/button";

function UploadCsv({ onUploadSuccess }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [file, setFile] = useState(null);

    async function handleUpload() {
        if(!file){
            setError("Please select a CSV file.")
            return;
        }

        setError("");
        setLoading(true);
        setSuccess("");

        try{
            const data = await uploadDocument(file);

            setSuccess("CSV uploaded successfully.");
            setFile(null);

            await onUploadSuccess();
        }
        catch (e) {
            setError(e.message);
        }
        finally {
            setLoading(false);
        }

    }

    return (
        <>
            <Input
                type="file"
                accept=".csv"
                onChange={(e) => {
                    setFile(e.target.files[0]);
                }}
            />

            {error && <p className="text-sm text-red-500">{error}</p>}

            {success && <p className="text-sm text-green-600">{success}</p>}

            <Button onClick={handleUpload} disabled={loading}>
                {loading ? "Uploading..." : "Upload CSV"}
            </Button>

        </>
    )
}

export default UploadCsv;