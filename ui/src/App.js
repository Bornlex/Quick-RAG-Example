import './App.css';
import axios from 'axios';
import React, {useState} from "react";

function App() {
    const [searchTerm, setSearchTerm] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('/api/search', { "query": searchTerm });
            console.log(response.data.results);
            setSearchResults(response.data.results);
        } catch (error) {
            console.error('Erreur lors de la requête:', error);
        }
    };

    const navigateTo = (url) => {
        window.location.href = url;
    }

    const navigateToHome = () => {
        navigateTo('/');
    }

    return (
        <div className="container">
            <h1 className="mainHeading" onClick={navigateToHome} style={{cursor: 'pointer'}}>Trouvez votre prochain contrat.</h1>
            <form id="searchbar" className="searchBox" onSubmit={handleSubmit}>
                <input
                    className="searchInput"
                    type="text"
                    placeholder="Recherche..."
                    value={searchTerm.value}
                    onChange={event => setSearchTerm(event.target.value)}
                />
                <button type="submit" form="searchbar" className="searchButton">→</button>
            </form>
            <h2 className="subHeading">Trouvez des contrats pour...</h2>
            <div className="tags">
                <span className="tag">construction projects in new york</span>
                <span className="tag">janitorial services on the east coast</span>
                <span className="tag">software license renewal</span>
                <span className="tag">historical building restoration</span>
                <span className="tag">artificial intelligence</span>
            </div>

            <div className="searchResults">
                {searchResults.length > 0 ? (
                    searchResults.map((result, index) => (
                        <div key={index} className="resultItem">
                            <h3>{result.objet}</h3>
                            <p>Code CPV: {result.codeCPV}</p>
                            <p>Date of Notification: {result.dateNotification}</p>
                            <p>Duration (Months): {result.dureeMois}</p>
                            <p>Price Form: {result.formePrix}</p>
                            <p>Amount: €{result.montant}</p>
                            <p>Nature: {result.nature}</p>
                            <p>Procedure: {result.procedure}</p>
                            <p>Execution Location: {result.lieuExecution.nom}</p>
                            <p>Contractor: {result.titulaires.map(titulaire => titulaire.denominationSociale).join(', ')}</p>
                        </div>
                    ))
                ) : (
                    <div>No results found.</div>
                )}
            </div>
        </div>
    );
}

export default App;
