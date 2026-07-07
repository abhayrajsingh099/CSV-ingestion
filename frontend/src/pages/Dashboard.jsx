import { useState } from "react";
import { useEffect } from "react";
import { getDocuments } from "@/services/documentService";
import Navbar from "@/components/NavBar";
import { Card } from "@/components/ui/card";
import UploadCsv from "@/components/UploadCsv";


function Dashboard() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [documents, setDocuments] = useState([]);

    async function fetchDocuments() {
        setError("");
        
        try{
            const data = await getDocuments();
            setDocuments(data);
        }
        catch (e) {
            setError(e.message);
        }
        finally{
            setLoading(false)
        }
    }


    useEffect(() => {

        fetchDocuments();

    }, [])

    if(loading){
        return <p>Fetching data...</p>
    }
    if(error){
        return <p>{error}</p>
    }


    return (
        <>
            <Navbar />

            <main className="mx-auto max-w-6xl p-6">
            <div className="mb-8">
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <p className="text-muted-foreground">
                    Manage your CSV documents.
                </p>
            </div>
            <div className="mb-8">
                <h1 className="text-3xl font-bold">Upload Csv</h1>
                <UploadCsv onUploadSuccess={fetchDocuments}/>
            </div>
            <h2 className="mb-4 text-xl font-semibold">
                Your Documents
            </h2>

            {
                documents.length === 0?
                <h5>
                    No documents yet.
                    Upload your first CSV to get started.
                </h5>
                :
                documents.map((document) => (
                    <Card
                        key={document.id}
                        className="mb-4 p-4"
                    >
                        <h3 className="font-semibold">
                            {document.file_path}
                        </h3>

                        <p className="text-sm text-muted-foreground">
                            Document ID: {document.id}
                        </p>
                        <p className="text-sm text-muted-foreground">
                            Date: {document.created_at}
                        </p>
                    </Card>
                ))
            }
            </main>

        </>
    )
}

export default Dashboard;