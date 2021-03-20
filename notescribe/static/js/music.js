/**
 * Get json url from page url
 * @returns {string} 
 */
const setup = () => {
	const jsonUrl = new URLSearchParams(window.location.search).get('url')
	return jsonUrl;
}

/**
 * Fetches data from s3
 * @param {string} jsonUrl
 */
const getData = (jsonUrl) => {
	fetch(jsonUrl)
	.then((res) => res.json())
	.then((data) => {
		document.getElementById("loading").remove();
		console.log(data.image_urls)
		
		const musicDiv = document.getElementById('music');
		for (let i = 0; i < data.image_urls.length; i++) {
			const img = document.createElement('img');
			img.src = data.image_urls[i];
			img.id = i;
			musicDiv.appendChild(img)
			musicDiv.appendChild(document.createElement('hr'))
		}
	})
}

/**
 * Main method that runs when page is loaded
 */
const loadMusic = () => {
	jsonUrl = setup();
	getData(jsonUrl)
}

loadMusic();
