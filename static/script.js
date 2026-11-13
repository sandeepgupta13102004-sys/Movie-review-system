const API_URL = "https://movie-review-system-6.onrender.com";

// Load Top Rated Movies
async function LoadTopRatedMovies() {

    const container = document.getElementById("movies-list");

    if (!container) {
        console.error("Movies list container not found!");
        return;
    }

    container.innerHTML = "<p>Loading top-rated movies...</p>";

    try {

        // Call the backend API
        const response = await fetch(
            `${API_URL}/api/movies/top-rated`
        );

        // Check API response
        if (!response.ok) {
            throw new Error(
                'HTTP error! Status: ${response.status}'
            );
        }

        // Convert response into JSON
        const data = await response.json();
        // Get top-rated movies
        const movies = data.top_rated_movies || [];

        // Check if movies are available
        if (movies.length === 0) {
            container.innerHTML = "<p>No movies found.</p>";
            return;
        }

        // Clear previous movies
        container.innerHTML = "";

        // Display movies
        movies.forEach(movie => {

            const movieElement = document.createElement("div");

            movieElement.className = "movie-card";

            const title = document.createElement("h2");
            title.textContent = movie.title || "Untitled Movie";

            const rating = document.createElement("p");
            rating.textContent =
                'Rating: ${movie.average_rating ?? "Not available"}';

            movieElement.appendChild(title);
            movieElement.appendChild(rating);

            container.appendChild(movieElement);

        });

    } catch (error) {

        console.error("Error loading movies:", error);

        container.innerHTML =
            "<p>Error loading movies. Please try again later.</p>";

    }
}

 LoadTopRatedMovies();