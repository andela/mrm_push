
const subTable = document.getElementById('subscribers-table')
function deleteSubscriber(e) {
	const subscriberKey = e.target.value;
	const jsonBody = {
		key: subscriberKey
	}
	fetch('http://127.0.0.1:5000/delete_subscribers', 
			{
				method: 'DELETE',
				headers:{
					"content-type": "application/json",
				},
				body: JSON.stringify(jsonBody),
			})
			.then(res => res.json())
			.then(data => {
				const msgDiv = document.getElementById('responseMsg')
				msgDiv.innerText= data.message
				for(let i = 0; i < subTable.rows.length; i++){
					const row = subTable.rows[i]
					if(row.id === `row-${subscriberKey}`){
						subTable.deleteRow(i)
					}
				};
			})
}
let subscriberInfo = {};
const modal = document.getElementById('editModal');
const span = document.getElementsByClassName("close")[0]; 
function modalOpener(item) {
	const subscriptionInfo = JSON.parse(item.subscription_info);
	subscriberInfo = item;
	subscriberInfo.subscription_info = subscriptionInfo;
  const selectOptions = ["android", "graphql", "rest", "web"]
  const selectOptionIndex = selectOptions.findIndex(option => option === item.platform)
  modal.style.display = "block";
  document.getElementById('platform').selectedIndex = selectOptionIndex;
  document.getElementById('subscription_info').value = subscriptionInfo.endpoint || subscriptionInfo.firebase_token;
}
span.onclick = function() {
  modal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


function handleEditChange(e){
	if (e.target.name === 'subscription_info') {
		if (subscriberInfo.subscription_info.endpoint) subscriberInfo.subscription_info.endpoint = e.target.value;
		if (subscriberInfo.subscription_info.firebase_token) subscriberInfo.subscription_info.firebase_token = e.target.value;
	} else {
		subscriberInfo[e.target.name] = e.target.value
	}

}

function editSubscriber(e) {
	e.preventDefault();
	const jsonBody = {
		subscriber_info: subscriberInfo
	}
	var key = subscriberInfo.subscriber_key
		fetch(`http://127.0.0.1:5000/edit_subscribers?key=${key}`, 
		{
			method: 'PUT',
			headers:{
				"content-type": "application/json",
			},
			body: JSON.stringify(jsonBody),
		})
		.then(res => res.json()
		)
		.then(data => {
			modal.style.display = "none";
			window.location.reload()
		})
}
