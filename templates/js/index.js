let responseDiv = document.querySelector('#responseDiv');
	const clearMessage = () => {
		responseDiv.innerHTML = ''
	}
	let  form = document.getElementById("subscriber");
	form.addEventListener("submit", addSubscriber);
    function addSubscriber(e) {
		e.preventDefault();

		let subscription_data = {
			subscriber_info: {
				platform: form.platform.value,
				subscription_info: form.subscription_info.value,
				calender_ids: [form.calender_ids.value]
			}
		}
		fetch('http://127.0.0.1:5000/subscription', 
			{
				method: 'POST',
				headers:{
					"content-type": "application/json",
				},
                body: JSON.stringify(subscription_data),
			})
			.then(res => res.json())
			.then(data => {
				if(data === 'We currently do not support this platform'){
					responseDiv.classList.remove('responseSuccess');
					responseDiv.classList.add('responseError');
					responseDiv.innerHTML = data;
				}else{
					responseDiv.classList.remove('responseError');
					responseDiv.classList.add('responseSuccess');
					responseDiv.innerHTML = 'Subscriber successfully added :-)';
				}
				setTimeout(clearMessage, 5000)
			})
			form.reset()
	}
