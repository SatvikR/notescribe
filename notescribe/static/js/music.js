// setup
const jsonUrl = new URLSearchParams(window.location.search).get('url')
let isLoading = true;

// get data
fetch(jsonUrl)
	.then((res) => res.json())
	.then((data) => {
		isLoading = false;
		console.log(data.image_urls)
		
		const musicDiv = document.getElementById('music');
		// data.image_urls.foreach((e, i) => {
		// 	const img = document.createElement('img')
		// 	img.src = e;
		// 	img.id = i;
		// 	musicDiv.appendChild(img)
		// })
		for (let i = 0; i < data.image_urls.length; i++) {
			const img = document.createElement('img');
			img.src = data.image_urls[i];
			img.id = i;
			musicDiv.appendChild(img)
		}
	})
