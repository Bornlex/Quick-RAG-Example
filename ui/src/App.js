import './App.css';
import axios from 'axios';
import React, {useState} from "react";

function App() {
    const [searchTerm, setSearchTerm] = useState('');

    const handleSubmit = async (event) => {
        console.log('Search term:', searchTerm);
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:3000/search', { "query": searchTerm });
            console.log(response.data);
        } catch (error) {
            console.error('Erreur lors de la requête:', error);
        }
    };

    return (
        <div className="container">
            <h1 className="mainHeading">Find your next bid.</h1>
            <form id="searchbar" className="searchBox" onSubmit={handleSubmit}>
                <input
                  className="searchInput"
                  type="text"
                  placeholder="Search anything"
                  value={searchTerm.value}
                  onChange={event => setSearchTerm(event.target.value)}
                />
                <button type="submit" form="searchbar" className="searchButton">→</button>
            </form>
            <h2 className="subHeading">Discover contracts for...</h2>
            <div className="tags">
                <span className="tag">construction projects in new york</span>
                <span className="tag">janitorial services on the east coast</span>
                <span className="tag">software license renewal</span>
                <span className="tag">historical building restoration</span>
                <span className="tag">artificial intelligence</span>
            </div>
        </div>
    );
}

export default App;
