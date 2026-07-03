import { useState } from "react";
import { useEffect } from "react";
import { getDocuments } from "@/services/documentService";
import Navbar from "@/components/NavBar";


function Dashboard() {
    const [count, setCount] = useState(0);
    const [documents, setDocuments] = useState([]);

    useEffect(() => {

        async function fetchDocuments() {
            const data = await getDocuments();
            setDocuments(data);
        }

        fetchDocuments();

    }, [])


    return (
        <>
            <Navbar />

            <h1>Dashboard</h1>
            <p>{count}</p>
            {
                documents.map((document) => <div><p>{document.id}</p> <p>{document.file_path}</p></div>)
            }

            <button onClick={() => setCount(count + 1)}>
                click
            </button>
        </>
    )
}

export default Dashboard;