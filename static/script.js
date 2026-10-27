async function LoadTopRatedMovies() {
    const container = document.getElementById('movies-list');
    container.innerHTML = '<p>Loading top-rated movies...</p>';

    try {
        const response = await fetch('/api/movies/top-rated');
        const movies = await response.json();

    if (movies.length === 0) { 
        container.innerHTML = '<p>No movies found.</p>';
        return;
    }
    // loop through the movies and create HTML elements for each movie
    container.innerHTML = ''; // Clear the loading message

    movies.forEach(movie => {
        const movieElement = document.createElement('div');
        movieElement.className = 'movie-card';
        movieElement.innerHTML = `
            <h2>${movie.title}</h2>
            <p>Rating: ${movie.rating}</p>
        `;
        container.appendChild(movieElement);
    });
 } catch (error) {
    console.error('Error loading movies:', error);
    container.innerHTML = '<p>Error loading movies. Please try again later.</p>';
  }
}

LoadTopRatedMovies();

