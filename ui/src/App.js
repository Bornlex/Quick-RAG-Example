import './App.css';
import Login from './Login';
import axios from 'axios';
import React, {useState} from "react";
import userEvent from "@testing-library/user-event";


function App() {
    const [searchTerm, setSearchTerm] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'))
    const [searchStarted, setSearchStarted] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(
                '/api/search', {
                    "query": searchTerm
                }, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    }
                }
            );
            setSearchResults(response.data.results);
        } catch (error) {
            console.error('Erreur lors de la requête:', error);
        }
    };

    const onLoginSuccess = () => {
        setIsAuthenticated(true);
    }

    const logout = () => {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
    }

    const navigateTo = (url) => {
        window.location.href = url;
    }

    const navigateToHome = () => {
        navigateTo('/');
    }

    return (
        <div className="container">
            {!isAuthenticated ? (
                <Login onLoginSuccess={onLoginSuccess} />
            ) : (
                <>
                <button onClick={logout}>Logout</button>
                <h1 className="mainHeading" onClick={navigateToHome} style={{cursor: 'pointer'}}>Trouvez votre prochain
                    contrat.</h1>
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
                    <span className="tag">projets informatiques dans l'Aisne</span>
                    <span className="tag">entretien d'ascenseurs</span>
                    <span className="tag">logiciels à moins de 5000€</span>
                    <span className="tag">restauration historique</span>
                    <span className="tag">intelligence artificielle</span>
                </div>

                <div className="searchResults">
                    {searchResults.length === 0 && searchStarted ? (
                        <div>No results found.</div>
                    ) : (
                        searchResults.map((result, index) => (
                            <div className="resultItem">
                                <div className="natureIndicator">{result.nature}</div>
                                <div className="contractDetails">
                                    <h3 className="contractObject">{result.objet}</h3>
                                    <p className="contractDuration">Duration: {result.dureeMois} months</p>
                                </div>
                                <div className="contractPrice">€{result.montant}</div>
                            </div>
                        ))
                    )}
                </div>
                </>
            )}
        </div>
    );
}

export default App;
