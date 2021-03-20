// globals
let currentImg = 0;
let imgs = [];

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
		document.getElementById('pdf').setAttribute('href', data.pdf_url)
		document.getElementById('midi').setAttribute('href', data.midi_url)
		imgs = data.image_urls;		
		updateImage()
	})
}

/**
 * Main method that runs when page is loaded
 */
const loadMusic = () => {
	jsonUrl = setup();
	getData(jsonUrl)
}

const previousPage = () => {
	if (currentImg > 0) {
		currentImg--;
	}
	updateImage()
}

const nextPage = () => {
	if (currentImg < imgs.length - 1) {
		currentImg++;
	}
	updateImage()

}

const updateImage = () => {
	if (!document.getElementById('current')) {
		const current = document.createElement('img')
		current.id = 'current'
		document.getElementById('music').appendChild(current)
	}
	const imageUrl = imgs[currentImg]
	document.getElementById('current').setAttribute('src', imageUrl)
}

loadMusic();
