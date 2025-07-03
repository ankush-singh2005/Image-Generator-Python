import React, { useState } from 'react';
import axios from 'axios';
// import './App.css';

const categories = ["Nature", "Mountains", "Cats", "Dogs", "City", "Flowers", "Beach", "Food", "Space", "Anime", "Custom"];

function App() {
  const [query, setQuery] = useState(categories[0]);
  const [customQuery, setCustomQuery] = useState('');
  const [images, setImages] = useState([]);
  const [index, setIndex] = useState(0);

  const fetchImages = async () => {
    const actualQuery = query === "Custom" ? customQuery : query;
    if (!actualQuery) return;

    try {
      const response = await axios.get(`http://localhost:5000/api/search?query=${actualQuery}`);
      setImages(response.data);
      setIndex(0);
    } catch (err) {
      alert("Error fetching images");
    }
  };

  const handleNext = () => {
    setIndex((prev) => (prev + 1) % images.length);
  };

  const handleDownload = () => {
    if (!images[index]) return;
    const link = document.createElement('a');
    link.href = images[index];
    link.download = `${query}_${index + 1}.jpg`;
    link.click();
  };

  return (
    <div className="App">
      <h1>React Image Generator</h1>
      <select value={query} onChange={(e) => setQuery(e.target.value)}>
        {categories.map((cat) => <option key={cat}>{cat}</option>)}
      </select>
      {query === 'Custom' && (
        <input
          type="text"
          placeholder="Enter keyword"
          value={customQuery}
          onChange={(e) => setCustomQuery(e.target.value)}
        />
      )}
      <button onClick={fetchImages}>Search</button>
      <button onClick={handleNext} disabled={images.length === 0}>Next</button>
      <button onClick={handleDownload} disabled={images.length === 0}>Download</button>

      <div className="image-container">
        {images.length > 0 && <img src={images[index]} alt="Result" />}
      </div>
    </div>
  );
}

export default App;
